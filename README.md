# AI Yapper System

Repeatable system for AI yapper ads: AI UGC videos of one person talking fast to a phone camera about a story they have.

- **The method:** [`YAPPER-PLAYBOOK.md`](YAPPER-PLAYBOOK.md) — living doc, read by every agent.
- **Agent instructions:** [`AGENTS.md`](AGENTS.md) (`CLAUDE.md` links to it).
- **Default stack:** kie.ai Omni (`gemini-omni-video`) for takes, Nano Banana Pro for actors, Whisper + ffmpeg for cut and sound.

Flow: brief → director sheet + job.yaml → approve → actor → chained takes → audio clean → rough cut → human trim → render → QA.
