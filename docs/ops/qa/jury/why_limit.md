---
id: why-limit
type: how-to
phase: [1, 6]
audience: [qa, visual, audio]
status: active
authority: qa
tokens_est: 445
summary: "Why + hard limitation"
---
# Agent Jury — Why + hard limitation

**Hub:** [`AGENT_JURY.md`](../AGENT_JURY.md)

## 1. Why this exists

The external-API jury (`tools/review_*_vision.py`) calls `api.openai.com` / `api.anthropic.com` / Gemini directly, which needs provider API keys. Those calls are made by a **headless Python script**, and Cursor exposes no general inference API a script can use — so the script cannot reach Cursor's subscription models.

A **Cursor agent can**, by dispatching subagents pinned to distinct models. This doc defines a jury where the review verdicts are produced by the agent's LLMs and then validated by a pure script. No provider keys required.

**Integrity is identical to the API path.** Verdicts are ingested through the same `qa_acceptance_lib` functions: `overall_pass` is recomputed from the measurable criteria (not the model's self-report), the confidence floor is enforced, and consensus still requires `jury_min_pass_models` (2) **distinct** models to pass. `WARN`/`SKIP` are still not `PASS`.


## 2. Hard limitation (read this)

This path requires a **Cursor agent runtime** (a cloud/PM-factory agent or the editor). It is **not** available in headless GitHub Actions, which has no Cursor LLM access. That is acceptable because the vision/audio jury is already **agent/editor-only** — it is explicitly listed under "Not run in CI" in `tools/run_ci_checks.sh` and is executed via `tools/run_*_smoke_checks.sh` by a QA agent, not by the game-ci workflow.

So: use provider keys if you need a fully headless (no-agent) jury; use this agent jury if the QA step always runs inside a Cursor agent (the sprint factory model).
