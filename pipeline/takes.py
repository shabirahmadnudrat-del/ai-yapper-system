#!/usr/bin/env python3
"""Generate the chained Omni takes for a yapper job.

  python3 takes.py <job_dir>              # all takes
  python3 takes.py <job_dir> --only t1    # specific takes (comma list)
  python3 takes.py <job_dir> --print t3   # print a take's prompt, generate nothing

Reads <job_dir>/job.yaml (playbook §7). Writes <job_dir>/takes/tN.mp4 + tN_last.png.
Resumable: a take whose mp4 exists is skipped; delete it to regenerate.
Chains that start fresh (on an angle image, playbook §8.4) run in parallel; takes inside a chain run in order.
"""
import argparse, os, re, sys, concurrent.futures as cf
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kie

LOCKED = (
    "Use the attached image as the exact opening frame: same person, same face, same clothes, same car, same light. "
    "Static, locked-off shot, no camera movement. {setting}. "
    "{P} stays seated, mouth moving naturally, direct eye contact, the camera never moves. "
    "In this take: {beats}. "
    "{say} "
    "{P} speaks with {voice}. {energy}. "
    "A very animated face: eyebrows up and down, glances to the window and back. "
    "Both hands gesture at chest height. {Pos} hands never touch {pos} face. "
    "One take, no jump cuts. No captions or on-screen text. No music."
)


def angle_of(take):
    return take.get("angle", "base")


def angle_entry(job, take):
    """The take's angle from actor.angles: a path, or {image, framing}. No angles = everything is base."""
    a = angle_of(take)
    entry = (job["actor"].get("angles") or {}).get(a)
    if entry is None:
        if a != "base":
            raise SystemExit(f"{take['id']}: angle '{a}' is not in actor.angles")
        entry = job["actor"]["approved_image"]
    return entry if isinstance(entry, dict) else {"image": entry}


def angle_image(job, take):
    return angle_entry(job, take)["image"]


def fresh(take):
    """Starts on its angle image rather than the previous take's last frame."""
    return take["starts_on"] in ("actor", "angle")


def prompt_for(job, take):
    beats = ", ".join(f"{a}-{b} s {d}" for a, b, d in take["beats"])
    if take.get("silent"):
        say = f"{job['pronoun']} does not speak in this take."
    elif job.get("pause_at_cuts"):
        # Real pauses at every cut mark give the editor a gap to cut in, so jump cuts don't make the body teleport.
        words = re.sub(r"[,.]?\s*/\s*", "... ", take["words"]).strip()
        say = (f'{job["pronoun"]} says: "{words}" {job["pronoun"]} stops talking for a clear one-second pause at every "...", '
               f'mouth closed, like a creator thinking before the next line, then carries on')
    else:
        words = re.sub(r"\s*/\s*", " ", take["words"]).strip()
        say = f'{job["pronoun"]} says: "{words}"'
    setting = job["setting"]["prompt"].rstrip(".")
    framing = angle_entry(job, take).get("framing")
    if framing:
        setting += ". " + framing.rstrip(".")
    return LOCKED.format(setting=setting, P=job["pronoun"], Pos=job["possessive"],
                         pos=job["possessive"].lower(), beats=beats, say=say, voice=job["voice"],
                         energy=job["energy"].rstrip("."))


def chains(takes):
    out, cur = [], []
    for t in takes:
        if fresh(t) and cur:
            out.append(cur); cur = []
        cur.append(t)
    if cur:
        out.append(cur)
    return out


def run_chain(job, chain, job_dir, only, logfile):
    tdir = os.path.join(job_dir, "takes")
    prev_png = None
    for t in chain:
        mp4 = os.path.join(tdir, f"{t['id']}.mp4")
        png = os.path.join(tdir, f"{t['id']}_last.png")
        if only and t["id"] not in only:
            prev_png = png if os.path.exists(png) else None
            continue
        if os.path.exists(mp4):
            kie.log(f"{t['id']}: exists, skip", logfile)
            prev_png = png
            continue
        if fresh(t):
            start_url = kie.upload(os.path.join(job_dir, angle_image(job, t)), f"yapper/{job['id']}")
        else:
            if not prev_png or not os.path.exists(prev_png):
                kie.log(f"{t['id']}: needs {t['starts_on']} frame first, stopping chain", logfile)
                return
            start_url = kie.upload(prev_png, f"yapper/{job['id']}")
        p = prompt_for(job, t)
        for attempt in range(1, 4):
            try:
                kie.log(f"{t['id']}: generating (attempt {attempt})", logfile)
                kie.omni_take(p, mp4, start_url, duration=t.get("duration_s", 8),
                              resolution=job["model"].get("resolution", "1080p"))
                kie.last_frame(mp4, png)
                kie.log(f"{t['id']}: done", logfile)
                break
            except Exception as e:
                kie.log(f"{t['id']}: {e}", logfile)
                if os.path.exists(mp4):
                    os.remove(mp4)
        else:
            kie.log(f"{t['id']}: FAILED 3x, stopping chain", logfile)
            return
        prev_png = png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_dir")
    ap.add_argument("--only", default="")
    ap.add_argument("--print", dest="show", default="")
    a = ap.parse_args()
    job = yaml.safe_load(open(os.path.join(a.job_dir, "job.yaml")))
    if a.show:
        print(prompt_for(job, next(t for t in job["takes"] if t["id"] == a.show)))
        return
    os.makedirs(os.path.join(a.job_dir, "takes"), exist_ok=True)
    logfile = os.path.join(a.job_dir, "takes", "takes.log")
    only = set(filter(None, a.only.split(",")))
    by_id = {t["id"]: t for t in job["takes"]}
    for t in job["takes"]:
        angle_entry(job, t)
        src = by_id.get(t["starts_on"].removesuffix("_last")) if not fresh(t) else None
        if src and angle_of(src) != angle_of(t):
            raise SystemExit(f"{t['id']}: chains from {src['id']} but changes angle; use starts_on: angle (playbook §8.4)")
    kie.log(f"credits before: {kie.credits()}", logfile)
    with cf.ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda c: run_chain(job, c, a.job_dir, only, logfile), chains(job["takes"])))
    kie.log(f"credits after: {kie.credits()}", logfile)


if __name__ == "__main__":
    main()
