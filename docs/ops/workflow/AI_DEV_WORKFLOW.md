---
id: ai-dev-workflow
type: how-to
phase: [0, 1, 8]
audience: [pm, architect, builder]
status: active
authority: workflow
tokens_est: 360
summary: "Build/test/acceptance — load build policy or testing pack"
---
# AI Dev Workflow

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`build_policy.md`](ai_dev/build_policy.md) | AI build policy |
| [`commands.md`](ai_dev/commands.md) | Commands quick ref |
| [`packs_gates.md`](ai_dev/packs_gates.md) | Related gates |
| [`phase_acceptance.md`](ai_dev/phase_acceptance.md) | Phase acceptance |
| [`testing_policy.md`](ai_dev/testing_policy.md) | AI testing policy |

**Version:** 1.3
**Applies to:** `main` clean baseline → Phases 1–8 rebuild
**Cross-refs:** `.cursorrules` §0, `AGENTS.md`, `docs/engineering/technical/CODE_BASE_CLASS_RULES.md`, `docs/ops/agents/GDAI_CLOUD_SETUP.md`, `docs/ops/qa/AI_TESTING_SPEC.md`, `docs/ops/workflow/IMPLEMENTATION_PLAN.md`, `docs/ops/qa/QA_AND_BUG_PROCESS.md`

This document is the **single source of truth** for:

## Factory hooks (registry keywords)

- Cycle close: `bash tools/run_post_agent_cycle.sh`
- Telemetry: `AGENT_SESSION_TELEMETRY`
- Watchdog: `bash tools/run_factory_watchdog.sh`
- Setup: `docs/ops/agents/FACTORY_SETUP_GUIDE.md`
- Stakeholder: `bash tools/pm_emit_stakeholder_report.sh`
- Alignment: `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png`
- Tournament: `CANDIDATE_TOURNAMENT`
- Portable pack: `packages/game-dev-factory/` · `FACTORY_DATA_DIR`

