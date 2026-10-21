#!/usr/bin/env python3
"""Cut a yapper job into a finished ad.

  python3 cut.py <job_dir>                         # main cut, all takes in order
  python3 cut.py <job_dir> --takes t1,t2,t7 --name test
  python3 cut.py <job_dir> --name cutdown_70s     # uses edit.yaml cutdowns.cutdown_70s

Steps (playbook §10-11):
  1. Whisper word timestamps per take (cached in takes/tN_words.json).
  2. Align transcript to the script words; jump cut at every "/" (pauses between phrases removed),
     anything Omni said after the last script word (filler) dropped.
  3. Per-take audio clean: denoise, high/low pass, level-matched to one loudness.
  4. Concat, pink room tone ~35 dB under the voice, master to -14 LUFS.
  5. Captions + stickers composited frame by frame from edit.yaml.
Output: <job_dir>/renders/<name>.mp4 and <name>.edl.json (the cut list, for a human trim pass).
"""
import argparse, difflib, json, os, re, subprocess, sys
import yaml
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 24
PRE, POST = 0.07, 0.13          # handles around each phrase (s)
TAKE_LUFS = -20.0
FONT_DIRS = [os.path.expanduser("~/Library/Fonts"), "/System/Library/Fonts/Supplemental", "/Library/Fonts"]


def font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def sh(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def words_json(mp4):
    out = mp4[:-4] + "_words.json"
    if not os.path.exists(out):
        sh(["mlx_whisper", mp4, "--model", "mlx-community/whisper-large-v3-turbo", "--word-timestamps", "True",
            "--language", "en", "--output-format", "json", "--output-dir", os.path.dirname(mp4) or ".",
            "--output-name", os.path.basename(out)[:-5]])
    d = json.load(open(out))
    return [{"w": x["word"].strip(), "s": x["start"], "e": x["end"]} for seg in d["segments"] for x in seg.get("words", [])]


def align(take, hyp):
    """Script tokens with times. Each token: text, phrase index, s, e."""
    toks = []
    # edit_words: what the take actually said that we keep (when Omni reorders/garbles, fix it in the edit)
    for pi, phrase in enumerate(take.get("edit_words", take["words"]).split("/")):
        for w in phrase.split():
            toks.append({"text": w, "p": pi})
    a = [norm(t["text"]) for t in toks]
    b = [norm(h["w"]) for h in hyp]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            toks[blk.a + k]["s"] = hyp[blk.b + k]["s"]
            toks[blk.a + k]["e"] = hyp[blk.b + k]["e"]
    # fuzzy-fill unmatched tokens from the next unused hypothesis word, else interpolate
    known = [i for i, t in enumerate(toks) if "s" in t]
    if not known:
        raise RuntimeError(f"{take['id']}: transcript does not match script")
    for i, t in enumerate(toks):
        if "s" in t:
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        s0 = toks[prev]["e"] if prev is not None else max(0.0, toks[nxt]["s"] - 0.3)
        s1 = toks[nxt]["s"] if nxt is not None else s0 + 0.3
        n_between = (nxt if nxt is not None else len(toks)) - (prev if prev is not None else -1) - 1
        j = i - (prev if prev is not None else -1) - 1
        step = (s1 - s0) / max(n_between, 1)
        t["s"], t["e"] = s0 + j * step, s0 + (j + 1) * step
    return toks


MERGE_GAP = 0.45     # a pause shorter than this is kept, not cut: tiny jump cuts read as glitches
SEARCH = 0.30        # how far past the words a cut frame may move to find the best pose match


def segments(take, toks, dur):
    """Phrases -> segments. Merges phrases split by a short pause, tags each token with its segment,
    and gives every segment the window its cut frames may move in (never into a word)."""
    phrases = []
    for pi in sorted({t["p"] for t in toks}):
        ts = [t for t in toks if t["p"] == pi]
        phrases.append({"toks": ts, "ws": ts[0]["s"], "we": ts[-1]["e"]})
    segs = []
    for ph in phrases:
        if segs and ph["ws"] - segs[-1]["we"] < MERGE_GAP:
            segs[-1]["toks"] += ph["toks"]; segs[-1]["we"] = ph["we"]
        else:
            segs.append(dict(ph))
    for i, sg in enumerate(segs):
        prev_we = segs[i - 1]["we"] if i else 0.0
        next_ws = segs[i + 1]["ws"] if i + 1 < len(segs) else dur
        sg["in_range"] = (max(prev_we + 0.02, sg["ws"] - SEARCH, 0.0), max(0.0, sg["ws"] - 0.04))
        sg["out_range"] = (min(sg["we"] + 0.03, dur), min(sg["we"] + SEARCH, next_ws - 0.02, dur))
        sg["in"] = min(max(sg["ws"] - PRE, sg["in_range"][0]), sg["in_range"][1])
        sg["out"] = max(min(sg["we"] + POST, sg["out_range"][1]), sg["out_range"][0])
        for t in sg["toks"]:
            t["seg"] = i
    return segs


_frames = {}


def small_frames(mp4):
    """All frames of a take, grey 90x160, for pose matching at cut points."""
    if mp4 not in _frames:
        import cv2
        cap, fr = cv2.VideoCapture(mp4), []
        while True:
            ok, f = cap.read()
            if not ok:
                break
            g = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(f, (90, 160)), cv2.COLOR_BGR2GRAY), (5, 5), 0)
            fr.append(g.astype(np.float32))
        _frames[mp4] = fr
    return _frames[mp4]


def frame_at(mp4, t):
    fr = small_frames(mp4)
    return fr[min(len(fr) - 1, max(0, int(round(t * FPS))))]


def join_cost(a, b):
    """Whole-frame difference plus extra weight on the hands/torso band."""
    return float(np.mean(np.abs(a - b)) + np.mean(np.abs(a[70:] - b[70:])))


def match_cuts(seq):
    """For each adjacent pair of segments pick the out-frame of A and in-frame of B whose poses match best."""
    step = 1.0 / FPS
    for A, B in zip(seq, seq[1:]):
        best = (join_cost(frame_at(A["mp4"], A["out"]), frame_at(B["mp4"], B["in"])), A["out"], B["in"])
        o = A["out_range"][0]
        while o <= A["out_range"][1] + 1e-6:
            fa = frame_at(A["mp4"], o)
            i = B["in_range"][0]
            while i <= B["in_range"][1] + 1e-6:
                c = join_cost(fa, frame_at(B["mp4"], i))
                if c < best[0]:
                    best = (c, o, i)
                i += step
            o += step
        A["out"], B["in"], B["join_cost"] = best[1], best[2], round(best[0], 2)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?\d+\.\d+) LUFS", r)
    return float(m[-1]) if m else TAKE_LUFS


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout.strip())


# ---------------- overlays ----------------

def rounded(img, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], r, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), m)
    return out


def text_box(text, size, fg, bg, pad=(34, 22), maxw=900, radius=26, fontname="Switzer-Extrabold.otf"):
    f = font(fontname, size)
    words, lines, cur = text.split(), [], ""
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw - 2 * pad[0] and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    lh = int(size * 1.18)
    tw = int(max(d.textlength(l, font=f) for l in lines))
    img = Image.new("RGBA", (tw + 2 * pad[0], lh * len(lines) + 2 * pad[1]), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius, fill=bg)
    for i, l in enumerate(lines):
        lw = dr.textlength(l, font=f)
        dr.text(((img.width - lw) / 2, pad[1] + i * lh - size * 0.05), l, font=f, fill=fg)
    return img


def shadow(img, blur=18, alpha=90):
    sh_ = Image.new("RGBA", (img.width + 60, img.height + 60), (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: v * alpha // 255)
    sh_.paste((0, 0, 0, 255), (30, 38), a)
    sh_ = sh_.filter(ImageFilter.GaussianBlur(blur))
    sh_.alpha_composite(img, (30, 30))
    return sh_


def caption_img(text):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    size = 74
    while True:                                   # shrink long chunks to fit the frame
        f = font("Switzer-Extrabold.otf", size)
        tw = int(d.textlength(text, font=f))
        if tw <= W - 140 or size <= 44:
            break
        size -= 4
    img = Image.new("RGBA", (tw + 40, 110), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((20, 10), text, font=f, fill="white", stroke_width=7, stroke_fill="black")
    return img


def sticker_img(st, job_dir):
    kind = st["type"]
    if kind == "hook_text":
        return shadow(text_box(st["text"], 62, "black", "white", maxw=940))
    if kind == "badge":
        return shadow(text_box(st["text"], st.get("size", 58), st.get("fg", "white"), st.get("bg", "#A40011"), maxw=900))
    if kind == "image_card":
        im = Image.open(os.path.join(job_dir, st["image"])).convert("RGBA")
        w = st.get("width", 620)
        im = im.resize((w, int(im.height * w / im.width)))
        if st.get("label"):
            lab = text_box(st["label"], 46, "white", "#50000B", radius=0, maxw=w, pad=(20, 16))
            card = Image.new("RGBA", (w, im.height + lab.height), "white")
            card.paste(im, (0, 0)); card.paste(lab, ((w - lab.width) // 2, im.height))
            im = card
        return shadow(rounded(im, 28))
    if kind == "fine_print":
        f = font("Switzer-Medium.otf", 26)
        txt = st["text"]
        d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        words, lines, cur = txt.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) > 980 and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        lines.append(cur)
        img = Image.new("RGBA", (1040, 34 * len(lines) + 24), (0, 0, 0, 140))
        dr = ImageDraw.Draw(img)
        for i, l in enumerate(lines):
            dr.text(((1040 - dr.textlength(l, font=f)) / 2, 12 + i * 34), l, font=f, fill=(255, 255, 255, 230))
        return img
    raise ValueError(kind)


POS = {"top": 230, "upper": 360, "center": 700, "lower": 1080, "bottom": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_dir")
    ap.add_argument("--takes", default="")
    ap.add_argument("--name", default="main")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="drop cached segment renders")
    a = ap.parse_args()
    jd = a.job_dir
    job = yaml.safe_load(open(os.path.join(jd, "job.yaml")))
    edit = yaml.safe_load(open(os.path.join(jd, "edit.yaml"))) if os.path.exists(os.path.join(jd, "edit.yaml")) else {}
    order = [t for t in job["takes"] if not a.takes or t["id"] in a.takes.split(",")]
    if a.name in edit.get("cutdowns", {}):        # cutdown = list of take ids, or {take: words-to-keep}
        by_id = {t["id"]: t for t in job["takes"]}
        order = []
        for item in edit["cutdowns"][a.name]:
            if isinstance(item, dict):
                (tid, words), = item.items()
                order.append(dict(by_id[tid], edit_words=words))
            else:
                order.append(by_id[item])
    work = os.path.abspath(os.path.join(jd, "renders", "_work_" + a.name))
    if a.fresh and os.path.isdir(work):
        import shutil; shutil.rmtree(work)
    os.makedirs(work, exist_ok=True)

    # 1-3: align, segment, match cut frames, clean audio per segment
    seq = []
    for t in order:
        mp4 = os.path.join(jd, "takes", f"{t['id']}.mp4")
        if not os.path.exists(mp4):
            print(f"missing {t['id']}, skipped", flush=True); continue
        toks = align(t, words_json(mp4))
        gain = TAKE_LUFS - loudness(mp4)
        segs = segments(t, toks, duration(mp4))
        for si, sg in enumerate(segs):
            sg.update(take=t["id"], mp4=mp4, si=si, gain=gain)
        seq += segs
        print(f"{t['id']}: {len(segs)} segments", flush=True)
    match_cuts(seq)

    edl, parts, gt, caps, word_times = [], [], 0.0, [], {}
    for sg in seq:
        s, e, mp4 = sg["in"], sg["out"], sg["mp4"]
        tag = f"{os.path.getmtime(mp4):.0f}_{s:.3f}_{e:.3f}"
        part = os.path.join(work, f"{sg['take']}_{sg['si']:02d}_{tag}.mp4")
        if not os.path.exists(part):
            af = (f"afftdn=nf=-28:tn=1,highpass=f=85,lowpass=f=11500,equalizer=f=3000:t=q:w=1.2:g=2,"
                  f"volume={sg['gain']:.2f}dB,afade=t=in:d=0.012,afade=t=out:st={e - s - 0.015:.3f}:d=0.015")
            sh(["ffmpeg", "-y", "-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", mp4,
                "-vf", f"scale={W}:{H},fps={FPS},format=yuv420p", "-af", af + ",aresample=48000",
                "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
                part.replace(".mp4", ".mov")])
            os.rename(part.replace(".mp4", ".mov"), part)
        pd = duration(part)
        edl.append({"take": sg["take"], "in": round(s, 3), "out": round(e, 3), "at": round(gt, 3),
                    "join_cost": sg.get("join_cost")})
        for k in sg["toks"]:
            gs = gt + max(0.0, k["s"] - s)
            ge = gt + min(pd, k["e"] - s)
            caps.append((gs, ge, k["text"]))
            word_times.setdefault(sg["take"], []).append((norm(k["text"]), gs, ge))
        parts.append(part); gt += pd
    json.dump(edl, open(os.path.join(jd, "renders", f"{a.name}.edl.json"), "w"), indent=1)

    # 4: concat + room tone + master
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    cat = os.path.join(work, "concat.mov")
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", cat])
    total = duration(cat)
    audio = os.path.join(work, "audio.wav")
    sh(["ffmpeg", "-y", "-i", cat, "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anoisesrc=color=pink:amplitude=0.0035:r=48000",
        "-filter_complex", "[1:a]lowpass=f=4000,aformat=channel_layouts=stereo[rt];[0:a][rt]amix=inputs=2:normalize=0,"
        "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", "48000", audio])

    # 5: overlays, frame by frame
    def word_time(tid, word, which="s"):
        for w, s, e in word_times.get(tid, []):
            if w == norm(word):
                return s if which == "s" else e
        raise KeyError(f"{tid}: '{word}' not found")

    overlays = []
    for st in edit.get("stickers", []):
        if st.get("takes_required") and not all(x in word_times for x in st["takes_required"]):
            continue
        try:
            if "at_end" in st:
                s, e = total - st["at_end"], total
            elif "full" in st:
                s, e = 0, total
            else:
                s = word_time(st["take"], st["word"]) - 0.05
                e = word_time(st.get("until_take", st["take"]), st["until_word"], "e") + 0.25 if "until_word" in st else s + st.get("hold", 2.5)
        except KeyError as err:
            print("sticker skipped:", err, flush=True); continue
        img = sticker_img(st, jd)
        y = H - img.height - 40 if st.get("pos") == "bottom" else st.get("y", POS.get(st.get("pos", "upper"), 360))
        overlays.append((s, e, img, ((W - img.width) // 2, y), st.get("hide_captions", False)))
    hook_windows = [(s, e) for s, e, _, _, hide in overlays if hide]

    chunks, cur = [], []
    for c in caps:                         # 1-3 words per caption, break on long gaps / punctuation
        cur.append(c)
        if len(cur) == 3 or re.search(r"[.,?!…]$", c[2]):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    cap_list = [(ch[0][0], ch[-1][1] if i == len(chunks) - 1 else max(ch[-1][1], chunks[i + 1][0][0]),
                 caption_img(re.sub(r'["“”]', "", " ".join(x[2] for x in ch)).strip(" ,").upper())) for i, ch in enumerate(chunks)]

    out = os.path.join(jd, "renders", f"{a.name}.mp4")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", cat, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                            "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    fs, n = W * H * 4, 0
    while True:
        buf = dec.stdout.read(fs)
        if len(buf) < fs:
            break
        tsec = n / FPS
        frame = Image.frombuffer("RGBA", (W, H), buf, "raw", "RGBA", 0, 1).copy()
        if not a.no_captions and not any(s <= tsec < e for s, e in hook_windows):
            for s, e, im in cap_list:
                if s <= tsec < e:
                    frame.alpha_composite(im, ((W - im.width) // 2, 1330)); break
        for s, e, im, xy, _ in overlays:
            if s <= tsec < e:
                frame.alpha_composite(im, (max(0, xy[0]), xy[1]))
        enc.stdin.write(frame.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"rendered {out} ({total:.1f}s, {n} frames)", flush=True)


if __name__ == "__main__":
    main()
