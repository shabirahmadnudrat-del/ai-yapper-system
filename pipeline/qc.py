#!/usr/bin/env python3
"""Yapper QC agent: find what looks or sounds wrong, fix it, re-cut, report.

  python3 qc.py <job_dir> lint [--fix]       # before generation: props in beats, face touches, word counts
  python3 qc.py <job_dir> takes              # Gemini watches + listens to every take -> qc/tN.json
  python3 qc.py <job_dir> review [--name main]   # Gemini watches the finished cut -> qc/review_<name>.json
  python3 qc.py <job_dir> fix [--max-regens 8]   # the full loop: takes QC -> regenerate bad takes -> re-cut -> review -> report

Judge: Gemini (video + audio understanding). Key: GEMINI_API_KEY env var or an `export GEMINI_API_KEY=` line in ~/.zshrc.
Only problems inside the frames the edit actually uses count (EDL in renders/<name>.edl.json).
"""
import argparse, json, os, re, shutil, subprocess, sys, time
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kie
import takes as takesmod

JUDGE = os.environ.get("YAPPER_QC_MODEL", "gemini-3.1-pro-preview")
FAST = os.environ.get("YAPPER_QC_FAST_MODEL", "gemini-3-flash-preview")

# Nouns that make Omni materialise an object when they appear in a gesture beat.
PROP_WORDS = r"\b(book|phone|glove|ball|cup|mug|coffee|bottle|spray|laptop|paper|pen|keys?|remote|scoop|sachet|powder|tub|glass|plate|bag|box|card|wallet|screen|notebook|tablet|can|drink|container|food)\b"
FACE_TOUCH = r"\b(rubs?|touch(es)?|scratch(es)?|cover(s)?|pinch(es)?)\b.*\b(eyes?|face|nose|forehead|chin|mouth|head|hair|temple)s?\b"


def gemini_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    for line in open(os.path.expanduser("~/.zshrc")):
        m = re.match(r'\s*export\s+GEMINI_API_KEY=["\']?([^"\'\s]+)', line)
        if m:
            return m.group(1)
    raise RuntimeError("GEMINI_API_KEY not found")


_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=gemini_key())
    return _client


def upload(path):
    f = client().files.upload(file=path)
    while getattr(f.state, "name", str(f.state)) == "PROCESSING":
        time.sleep(3)
        f = client().files.get(name=f.name)
    return f


def ask_json(model, parts, retries=3):
    from google.genai import types
    for i in range(retries):
        try:
            r = client().models.generate_content(model=model, contents=parts,
                                                 config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2))
            out = json.loads(r.text)
            if isinstance(out, list):            # models sometimes wrap the object in a list
                out = out[0] if out and isinstance(out[0], dict) else {"issues": out}
            return out
        except Exception as e:
            print(f"  gemini retry {i + 1}: {e}", flush=True)
            time.sleep(8)
    raise RuntimeError("gemini failed")


def load(jd):
    return yaml.safe_load(open(os.path.join(jd, "job.yaml")))


def save_job(jd, job):
    yaml.safe_dump(job, open(os.path.join(jd, "job.yaml"), "w"), sort_keys=False, allow_unicode=True, width=200)


def used_windows(jd, name="main"):
    p = os.path.join(jd, "renders", f"{name}.edl.json")
    if not os.path.exists(p):
        return {}
    w = {}
    for x in json.load(open(p)):
        w.setdefault(x["take"], []).append((x["in"], x["out"]))
    return w


def in_use(issue, windows):
    if windows is None:
        return True
    s, e = float(issue.get("start", 0)), float(issue.get("end", issue.get("start", 0)))
    return any(s <= b and e >= a for a, b in windows)


# ---------------- lint ----------------

def lint(jd, fix=False):
    job = load(jd)
    allowed = {p.lower() for t in job["takes"] for p in t.get("props_start", []) + t.get("props_end", [])}
    problems = []
    for t in job["takes"]:
        n = len(re.sub(r"/", " ", t.get("words", "")).split())
        lim = (18, 25) if t.get("duration_s", 8) == 8 else (24, 31)
        if job.get("pause_at_cuts"):                 # each ~0.5 s pause costs about 1.5 words
            k = t.get("words", "").count("/")
            lim = (lim[0] - int(1.5 * k), lim[1] - int(1.5 * k))
        if not t.get("silent") and not (lim[0] <= n <= lim[1]):
            problems.append((t["id"], "words", f"{n} words (want {lim[0]}-{lim[1]})"))
        for i, (a, b, d) in enumerate(t["beats"]):
            for m in re.finditer(PROP_WORDS, d, re.I):
                if not any(m.group(1).lower() in p for p in allowed):
                    problems.append((t["id"], "prop_in_beat", f"beat {i}: '{d}' names '{m.group(1)}', Omni will put one in his hands"))
            if re.search(FACE_TOUCH, d, re.I):
                problems.append((t["id"], "face_touch", f"beat {i}: '{d}' has a hand going to the face"))
    for p in problems:
        print(f"{p[0]:>4}  {p[1]:<13} {p[2]}")
    if fix:
        bad = sorted({p[0] for p in problems if p[1] in ("prop_in_beat", "face_touch")})
        for t in job["takes"]:
            if t["id"] in bad:
                t["beats"] = rewrite_beats(t)
                print(f"{t['id']} beats -> {[b[2] for b in t['beats']]}")
        if bad:
            save_job(jd, job)
    return problems


def rewrite_beats(t):
    r = ask_json(FAST, [
        "Rewrite these gesture beats for an AI video model. Rules: the person's hands are EMPTY; never name any object "
        "(no book, phone, glove, cup, etc.) and never say 'mimes' or 'as if holding'; describe only hand shapes, arm "
        "positions, face and body ("
        "e.g. 'both palms up, close together, eyes drooping'); hands never touch the face; keep the emotional intent "
        "and roughly the same energy. Return JSON {\"beats\": [string, string, string]} in the same order.\n\n"
        f"Spoken line: {t['words']}\nBeats: {json.dumps([b[2] for b in t['beats']])}"])
    return [[a, b, nd] for (a, b, _), nd in zip(t["beats"], r["beats"])]


# ---------------- take review ----------------

TAKE_PROMPT = """You are the QC reviewer for an AI-generated UGC "yapper" ad: one person talking to a phone camera.
Attached in order: (1) the approved actor image, (2) a reference clip of the approved voice, (3) the take to review.

The take should show: the same person as the actor image (face, hair, beard, build), the same outfit and white wired
earphones, the same car and light, a phone camera that never moves or zooms, no on-screen text, and these props only: {props}.
Expected spoken line: "{line}"
Planned gestures: {beats}

Watch the WHOLE take and listen to the audio. Report every problem a viewer would notice, with timestamps in seconds:
- prop: an object appears that is not in the allowed props list (book, phone, paper...), or a prop changes/vanishes
- identity: the face or body changes, looks like a different person, morphs
- outfit: clothes, earphones, accessories change or vanish
- hands: extra/missing/deformed fingers, hands merge with objects, hands touch the face, impossible poses
- camera: zoom, push-in, pan, shake
- text: captions, subtitles or any on-screen text
- voice: sounds like a different speaker than the reference clip (pitch, timbre, accent, age), robotic, glitchy, distorted
- lipsync: mouth does not match the words
- delivery: missing, wrong, garbled, extra or repeated words; long dead air; filler at the end
- continuity: anything else that breaks the illusion (lighting jump, background change, glitch frames)
Do not report the planned gestures being slightly different. Severity: high = a viewer would notice and it breaks
trust; medium = noticeable on a second look; low = nitpick.

Return JSON:
{{"voice_match": 1-5 (5 = clearly the same speaker as the reference),
  "identity_match": 1-5,
  "spoken_text": "what is actually said",
  "issues": [{{"start": s, "end": s, "category": "...", "severity": "high|medium|low", "description": "..."}}]}}"""


def review_take(jd, job, t, ref_voice, actor_file, force=False):
    qd = os.path.join(jd, "qc")
    os.makedirs(qd, exist_ok=True)
    out = os.path.join(qd, f"{t['id']}.json")
    mp4 = os.path.join(jd, "takes", f"{t['id']}.mp4")
    if os.path.exists(out) and not force and os.path.getmtime(out) > os.path.getmtime(mp4):
        return json.load(open(out))
    props = ", ".join(sorted(set(t.get("props_start", []) + t.get("props_end", [])))) or "NONE (hands must be empty)"
    beats = "; ".join(f"{a}-{b}s {d}" for a, b, d in t["beats"])
    r = ask_json(JUDGE, [actor_file, ref_voice, upload(mp4),
                         TAKE_PROMPT.format(props=props, line=re.sub(r"\s*/\s*", " ", t["words"]), beats=beats)])
    r["take"] = t["id"]
    json.dump(r, open(out, "w"), indent=1)
    return r


def ref_files(jd, job):
    ref_take = job.get("qc", {}).get("voice_reference", job["takes"][0]["id"])
    wav = os.path.join(jd, "qc", "voice_reference.wav")
    os.makedirs(os.path.dirname(wav), exist_ok=True)
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(jd, "takes", f"{ref_take}.mp4"), "-vn", "-ac", "1", wav], check=True)
    return upload(wav), upload(os.path.join(jd, job["actor"]["approved_image"]))


def blocking(r, windows, voice_min=3, identity_min=3):
    # Calibrated on the first pilot: Gemini scores a take 3/5 even against its own audio, so only <=2 is a real mismatch.
    """Issues that force a regenerate: high severity inside used frames, or a voice/identity mismatch."""
    out = [i for i in r.get("issues", []) if i.get("severity") == "high" and in_use(i, windows)]
    if r.get("voice_match", 5) < voice_min:
        out.append({"start": 0, "end": 8, "category": "voice", "severity": "high", "description": f"voice_match {r.get('voice_match')}"})
    if r.get("identity_match", 5) < identity_min:
        out.append({"start": 0, "end": 8, "category": "identity", "severity": "high", "description": f"identity_match {r.get('identity_match')}"})
    return out


def review_takes(jd, ids=None, force=False):
    job = load(jd)
    voice, actor = ref_files(jd, job)
    win = used_windows(jd)
    res = {}
    todo = [t for t in job["takes"] if (not ids or t["id"] in ids) and os.path.exists(os.path.join(jd, "takes", f"{t['id']}.mp4"))]
    import concurrent.futures as cf
    with cf.ThreadPoolExecutor(4) as ex:
        reviews = dict(zip([t["id"] for t in todo], ex.map(lambda t: review_take(jd, job, t, voice, actor, force), todo)))
    for t in todo:
        r = reviews[t["id"]]
        b = blocking(r, win.get(t["id"]) if win else None)
        res[t["id"]] = (r, b)
        flag = "FIX " if b else "ok  "
        print(f"{flag}{t['id']} voice={r.get('voice_match')} id={r.get('identity_match')} "
              + "; ".join(f"[{i['severity'][0]}] {i['category']} {i.get('start')}-{i.get('end')}s {i['description']}" for i in r.get("issues", [])), flush=True)
    return res


# ---------------- regenerate ----------------

PATCH = {
    "prop": "{P} hands are completely empty for the whole take, with nothing in them, on {pos} lap or on the steering wheel",
    "hands": "{P} hands stay relaxed and natural with five fingers each, always below {pos} chin, never touching {pos} face",
    "camera": "The phone is fixed to the dashboard: the frame never zooms, pans or shakes",
    "text": "The picture is clean video with no words, captions or graphics anywhere",
    "outfit": "{P} wears exactly the same clothes and white wired earphones as in the opening frame for the whole take",
}


def regenerate(jd, job, t, issues, attempt):
    cats = {i["category"] for i in issues}
    tdir = os.path.join(jd, "takes")
    mp4 = os.path.join(tdir, f"{t['id']}.mp4")
    keep = os.path.join(tdir, "_rejected")
    os.makedirs(keep, exist_ok=True)
    shutil.move(mp4, os.path.join(keep, f"{t['id']}_v{attempt}.mp4"))
    for ext in ("_last.png", "_words.json"):
        p = os.path.join(tdir, t["id"] + ext)
        if os.path.exists(p):
            os.remove(p)
    t2 = dict(t)
    if "prop" in cats or "face_touch" in cats or re.search(PROP_WORDS, " ".join(b[2] for b in t["beats"]), re.I):
        t2["beats"] = rewrite_beats(t)
    extra = [PATCH[c].format(P=job["possessive"], pos=job["possessive"].lower()) for c in cats if c in PATCH]
    # A problem already in the opening frame was inherited from the chain: restart from the take's angle image.
    from_actor = takesmod.fresh(t) or cats & {"identity", "outfit", "voice"} or any(float(i.get("start", 9)) < 0.5 for i in issues if i["category"] == "prop")
    prompt = takesmod.prompt_for(job, t2) + (" " + ". ".join(extra) + "." if extra else "")
    if from_actor:
        start = kie.upload(os.path.join(jd, takesmod.angle_image(job, t)), f"yapper/{job['id']}")
    else:
        prev = os.path.join(tdir, t["starts_on"] + ".png")
        start = kie.upload(prev, f"yapper/{job['id']}")
    kie.log(f"{t['id']}: regenerate #{attempt} ({', '.join(sorted(cats))}; start={'actor' if from_actor else t['starts_on']})",
            os.path.join(tdir, "takes.log"))
    kie.omni_take(prompt, mp4, start, duration=t.get("duration_s", 8), resolution=job["model"].get("resolution", "1080p"))
    kie.last_frame(mp4, os.path.join(tdir, f"{t['id']}_last.png"))
    if t2["beats"] != t["beats"]:
        t["beats"] = t2["beats"]
        save_job(jd, job)
    return {"take": t["id"], "attempt": attempt, "categories": sorted(cats), "from_actor": bool(from_actor),
            "issues": [i["description"] for i in issues]}


# ---------------- cut review ----------------

CUT_PROMPT = """You are the final QC reviewer for an AI-generated UGC "yapper" ad (one person talking to a phone, jump cuts).
Jump cuts are intentional. Watch and listen to the whole video and list only moments a viewer would find jarring or fake:
- a cut where the body/hands teleport in a way that looks like a glitch rather than a normal jump cut
- a cut inside a word, clipped or doubled audio, a sudden change in voice, loudness or room sound
- objects appearing/vanishing, the person or outfit changing, deformed hands, camera moving
- captions or stickers covering the face, wrong or misspelled caption words, text off screen
Return JSON {"overall": 1-10, "issues": [{"time": s, "category": "...", "severity": "high|medium|low", "description": "..."}]}"""


def review_cut(jd, name="main"):
    mp4 = os.path.join(jd, "renders", f"{name}.mp4")
    r = ask_json(JUDGE, [upload(mp4), CUT_PROMPT])
    edl = json.load(open(os.path.join(jd, "renders", f"{name}.edl.json")))
    for i in r.get("issues", []):
        seg = max((x for x in edl if x["at"] <= float(i.get("time", 0))), key=lambda x: x["at"], default=None)
        if seg:
            i["take"] = seg["take"]
    json.dump(r, open(os.path.join(jd, "qc", f"review_{name}.json"), "w"), indent=1)
    print(f"overall {r.get('overall')}/10")
    for i in r.get("issues", []):
        print(f"  [{i['severity'][0]}] {i.get('time')}s {i.get('take', '?')} {i['category']}: {i['description']}")
    return r


# ---------------- the loop ----------------

def run_cut(jd, name="main"):
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cut.py"), jd, "--name", name, "--fresh"], check=True)


def fix(jd, max_regens=8, max_attempts=2):
    os.makedirs(os.path.join(jd, "qc"), exist_ok=True)
    log = {"started": time.strftime("%Y-%m-%d %H:%M"), "credits_before": kie.credits(), "regens": []}
    lint(jd, fix=True)
    if not os.path.exists(os.path.join(jd, "renders", "main.edl.json")):
        run_cut(jd)                                      # need the EDL to know which frames are used
    attempts = {}
    for rnd in range(1, max_attempts + 1):
        res = review_takes(jd)
        bad = [(tid, b) for tid, (r, b) in res.items() if b]
        if not bad:
            break
        job = load(jd)
        by_id = {t["id"]: t for t in job["takes"]}
        for tid, issues in bad:                          # in take order, so a fixed take re-seeds its chained successor
            if len(log["regens"]) >= max_regens or attempts.get(tid, 0) >= max_attempts:
                continue
            attempts[tid] = attempts.get(tid, 0) + 1
            try:
                log["regens"].append(regenerate(jd, job, by_id[tid], issues, attempts[tid]))
            except Exception as e:
                log["regens"].append({"take": tid, "error": str(e)})
        run_cut(jd)
    review = review_cut(jd)
    remaining = {tid: b for tid, (r, b) in review_takes(jd).items() if b}
    log.update(credits_after=kie.credits(), remaining_take_issues=remaining, final_review=review)
    json.dump(log, open(os.path.join(jd, "qc", "qc_log.json"), "w"), indent=1)
    report(jd, log)


def report(jd, log):
    L = [f"# QC report — {load(jd)['id']}", "", f"Run {log['started']} · credits {log['credits_before']} → {log['credits_after']}", ""]
    L += ["## Regenerated takes", ""] + ([f"- **{r['take']}** #{r.get('attempt')}: {', '.join(r.get('categories', []))} "
                                         f"(start {'actor' if r.get('from_actor') else 'chain'}) — {'; '.join(r.get('issues', [])) or r.get('error', '')}"
                                         for r in log["regens"]] or ["- none"])
    L += ["", "## Still open after the loop (needs a human or another pass)", ""]
    L += [f"- **{tid}**: " + "; ".join(f"{i['category']} {i.get('start')}-{i.get('end')}s {i['description']}" for i in iss)
          for tid, iss in log["remaining_take_issues"].items()] or ["- none"]
    fr = log["final_review"]
    L += ["", f"## Final cut review: {fr.get('overall')}/10", ""]
    L += [f"- [{i['severity']}] {i.get('time')}s ({i.get('take', '?')}) {i['category']}: {i['description']}" for i in fr.get("issues", [])] or ["- none"]
    open(os.path.join(jd, "qc", "QC-REPORT.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_dir")
    ap.add_argument("cmd", choices=["lint", "takes", "review", "fix"])
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--name", default="main")
    ap.add_argument("--max-regens", type=int, default=8)
    a = ap.parse_args()
    if a.cmd == "lint":
        lint(a.job_dir, a.fix)
    elif a.cmd == "takes":
        review_takes(a.job_dir, set(filter(None, a.only.split(","))) or None, a.force)
    elif a.cmd == "review":
        review_cut(a.job_dir, a.name)
    else:
        fix(a.job_dir, a.max_regens)


if __name__ == "__main__":
    main()
