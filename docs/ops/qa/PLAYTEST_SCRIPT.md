---
id: playtest-script
type: how-to
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 233
summary: "Human L6 playtest — load act scripts or survey"
---
# Playtest Script

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`goals_setup_act1.md`](playtest_script/goals_setup_act1.md) | Goals, setup, Act I |
| [`act2_act3_regression.md`](playtest_script/act2_act3_regression.md) | Act II, Act III, regression |
| [`feel_survey_bugs.md`](playtest_script/feel_survey_bugs.md) | Feel checklist, survey, bugs |
**Version:** 1.2
**Target duration:** 2–3 hours
**Build:** Release candidate on `game/development`
**Prerequisite:** **All AI tests L0–L5 must pass** on the same commit before any human runs this script. See `docs/ops/qa/AI_TESTING_SPEC.md` §8.
**Minimum cohort:** 5 testers (diverse language rotation) — recorded in `artifacts/qa_reports/L6_human_playtest.json`

