"""kie.ai helpers for the yapper pipeline: upload, createTask, poll, download, frame harvest.

Key: KIE_API_KEY env var, or a KIE_API_KEY=... line in ~/.roofus_kie.env (override with KIE_ENV_FILE).
Gotcha: the redpandaai upload/download hosts 403 Python's default User-Agent, so every request sends a curl UA.
"""
import base64, json, mimetypes, os, subprocess, time, urllib.error, urllib.request

CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
POLL_URL = "https://api.kie.ai/api/v1/jobs/recordInfo?taskId="
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-base64-upload"
CREDIT_URL = "https://api.kie.ai/api/v1/chat/credit"
UA = "curl/8.4.0"

OMNI = "gemini-omni-video"
NANO_BANANA = "nano-banana-2"


def _key():
    if os.environ.get("KIE_API_KEY"):
        return os.environ["KIE_API_KEY"].strip()
    path = os.path.expanduser(os.environ.get("KIE_ENV_FILE", "~/.roofus_kie.env"))
    for line in open(path):
        if line.startswith("KIE_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("KIE_API_KEY not found")


def log(msg, logfile=None):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if logfile:
        with open(logfile, "a") as f:
            f.write(line + "\n")


def api(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {_key()}", "Content-Type": "application/json", "User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  http retry {attempt + 1}: {e}", flush=True)
            time.sleep(10)
    raise RuntimeError(f"http gave up: {url}")


def upload(path, upload_path="yapper"):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    r = api(UPLOAD_URL, {"base64Data": f"data:{mime};base64,{b64}",
                         "uploadPath": upload_path, "fileName": os.path.basename(path)})
    url = (r.get("data") or {}).get("downloadUrl")
    if not url:
        raise RuntimeError(f"upload failed: {r}")
    return url


def create_task(model, inp):
    r = api(CREATE_URL, {"model": model, "input": inp})
    tid = (r.get("data") or {}).get("taskId")
    if not tid:
        raise RuntimeError(f"createTask failed: {r}")
    return tid


def poll(tid, timeout=1800, every=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        d = api(POLL_URL + tid).get("data") or {}
        state = d.get("state")
        if state == "success":
            rj = d.get("resultJson")
            rj = json.loads(rj) if isinstance(rj, str) else (rj or {})
            urls = rj.get("resultUrls") or []
            if not urls:
                raise RuntimeError(f"success but no urls: {d}")
            return urls[0]
        if state == "fail":
            raise RuntimeError(f"GENFAIL: {d.get('failMsg') or d.get('failCode') or d}")
        time.sleep(every)
    raise RuntimeError("poll timeout")


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r, open(path, "wb") as f:
        f.write(r.read())
    return path


def last_frame(mp4, png):
    subprocess.run(["ffmpeg", "-y", "-sseof", "-0.1", "-i", mp4, "-update", "1", "-q:v", "1", png],
                   check=True, capture_output=True)
    return png


def credits():
    try:
        return api(CREDIT_URL)["data"]
    except Exception:
        return "?"


def image(prompt, out, refs=(), aspect="9:16", resolution="2K"):
    """Nano Banana 2 image. refs = public URLs."""
    inp = {"prompt": prompt, "aspect_ratio": aspect, "resolution": resolution, "output_format": "png"}
    if refs:
        inp["image_input"] = list(refs)
    return download(poll(create_task(NANO_BANANA, inp)), out)


def omni_take(prompt, out, start_image_url=None, duration="8", aspect="9:16", resolution="1080p"):
    """One Omni take. start_image_url = public URL of the frame the take opens on."""
    inp = {"prompt": prompt, "duration": str(duration), "aspect_ratio": aspect, "resolution": resolution}
    if start_image_url:
        inp["image_urls"] = [start_image_url]
    return download(poll(create_task(OMNI, inp)), out)
