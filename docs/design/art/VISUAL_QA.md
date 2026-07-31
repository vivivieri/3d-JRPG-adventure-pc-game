---
id: visual-qa
type: how-to
audience: [visual, builder, qa]
phase: [1, 5]
status: active
authority: art
tokens_est: 284
summary: "Screenshot + vision gates — load the layer for your pass"
---
# Visual QA

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`judge_layers.md`](visual_qa/judge_layers.md) | What AI can judge + defense layers |
| [`tools_antipattern.md`](visual_qa/tools_antipattern.md) | Tools + black-box anti-pattern |
| [`report_phase_tools.md`](visual_qa/report_phase_tools.md) | Report template, phase gates, tools |
**Version:** 1.0
**Problem:** An agent can “succeed” at placing a `BoxMesh`, decide it looks fine in the abstract, and replicate that placeholder across every zone. **Policy text alone does not prevent this.**

**Rule:** AI does **not** pass visual work on log output or node counts alone. It must pass **automated visual gates** + **screenshot review** against `docs/design/art/ART_DIRECTION.md`.

## Candidate tournament

Zone visual picks may use `golden_harness.json` via `bash tools/run_candidate_tournament.sh` (`docs/ops/qa/CANDIDATE_TOURNAMENT.md`).
