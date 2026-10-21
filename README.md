# AI Yapper System

Repeatable system for AI yapper ads: AI UGC videos of one person talking fast to a phone camera about a story they have.

- **The method:** [`YAPPER-PLAYBOOK.md`](YAPPER-PLAYBOOK.md) — living doc, read by every agent.
- **Agent instructions:** [`AGENTS.md`](AGENTS.md) (`CLAUDE.md` links to it).
- **Default stack:** kie.ai Omni (`gemini-omni-video`) for takes, Nano Banana Pro for actors, Whisper + ffmpeg for cut and sound.

Flow: brief → director sheet + job.yaml → approve → actor → chained takes → audio clean → rough cut → human trim → render → QA.

## Running the pipeline

Needs `ffmpeg`, `mlx_whisper` (Apple Silicon) and Python with `pyyaml`, `numpy`, `Pillow`. Key: `KIE_API_KEY` env var.

```bash
python3 pipeline/takes.py <job_dir> --only t1      # test one take
python3 pipeline/takes.py <job_dir>                # all takes (chains run in parallel, resumable)
python3 pipeline/cut.py <job_dir>                  # main cut -> <job_dir>/renders/main.mp4
python3 pipeline/cut.py <job_dir> --name cutdown_70s   # a cutdown defined in edit.yaml
```

A job dir holds `job.yaml` (playbook §7), `edit.yaml` (stickers + cutdowns) and the actor image.
