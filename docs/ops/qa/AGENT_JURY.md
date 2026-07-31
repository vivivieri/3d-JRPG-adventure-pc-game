---
id: agent-jury
type: how-to
phase: [1, 6]
audience: [qa, visual, audio]
status: active
authority: qa
tokens_est: 219
summary: "Vision/audio jury protocol — load limitation or checklist"
---
# Agent Jury

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`why_limit.md`](jury/why_limit.md) | Why + hard limitation |
| [`protocol_fields.md`](jury/protocol_fields.md) | Protocol, checklist fields, external API jury |
**Authority:** Alternative to the external-API vision/audio jury (`docs/design/art/VISUAL_QA.md`, `docs/design/art/MODEL_QA.md`, `docs/design/audio/AUDIO_QA.md`) that uses **Cursor's own LLMs via agent subagents** instead of `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY`.

**Cross-refs:** `docs/ops/qa/ACCEPTANCE_CRITERIA.md` (consensus rules) · `tools/ingest_agent_jury.py` · `tools/qa_acceptance_lib.py`

