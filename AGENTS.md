# AI Yapper System — agent instructions

You are working in the AI Yapper System: a repo for scripting, generating, cutting and shipping AI yapper ads (one person talking fast to a phone camera, jump cut every 2-3 s).

## Read first, every time
1. **`YAPPER-PLAYBOOK.md`** — the single source of truth. Read it fully before writing any script.
2. `brands/<slug>.md` — the brand brain for the brand you're writing for (product, offer, approved claims, VoC, banned words).

## What you produce
For any script request, output exactly what Appendix A of the playbook asks for:
concept → six moves → director sheet (markdown) → job file (YAML) → self-QA.
Save to `jobs/<brand>/<ad-id>/director-sheet.md` and `jobs/<brand>/<ad-id>/job.yaml`.

## QC
After generating takes, run the QC agent: `python3 pipeline/qc.py <job_dir> fix` (playbook §12b). Claude Code users can call the `yapper-qc` subagent (`.claude/agents/yapper-qc.md`); other agents follow the same steps from that file.

## Hard rules
- Never generate or describe a real person's likeness. No celebrity names in dialogue.
- Default video model: kie.ai `gemini-omni-video` (Omni).
- Don't change the playbook's rules silently. If you learn something, add it to the right section and log it in §14 Changelog.

## Repo map
- `YAPPER-PLAYBOOK.md` — the method
- `brands/` — one brand brain per brand
- `jobs/<brand>/<ad-id>/` — director sheet, job.yaml, generated takes, cuts, renders
- `library/actors/` — approved actors (source frame, approved image, prompt, card)
- `library/settings/` — reusable setting prompts
- `library/swipes/` — dissected real yapper ads used as references
- `prompts/` — prompt templates (actor edit, locked take)
- `pipeline/` — generation, audio, rough cut, render, QA scripts
- `schemas/` — job file schema
