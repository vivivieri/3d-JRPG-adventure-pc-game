---
id: playtest-telemetry
type: reference
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 222
summary: "Human playtest JSONL — load schema, metrics, or privacy"
---
# Playtest Telemetry

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`purpose_pipeline_schema.md`](playtest_tel/purpose_pipeline_schema.md) | Purpose, pipeline, schema |
| [`metrics_usage_logger.md`](playtest_tel/metrics_usage_logger.md) | Metrics, usage, in-game logger |
| [`privacy.md`](playtest_tel/privacy.md) | Privacy |
**Discipline:** Games User Research (GUR) — telemetry-driven playtest tuning
**Workflow:** measure → judge → tune → re-measure (a dev-time tuning loop, human-in-the-loop)
**Version:** 1.0
**Status:** Dev-time QA capability (schema + analyzer on `main`; in-game telemetry logger is a `game/development` implementation task)

