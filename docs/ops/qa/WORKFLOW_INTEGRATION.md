---
id: workflow-integration
type: how-to
phase: [1, 6]
audience: [pm, architect]
status: active
authority: qa
tokens_est: 244
summary: "Register factory features before merge — load checklist or registry"
---
# Workflow Integration

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`problem_register.md`](workflow_int/problem_register.md) | Problem + register-before-merge |
| [`checklist_features.md`](workflow_int/checklist_features.md) | Add-feature checklist + registered features |
| [`alignment_gates.md`](workflow_int/alignment_gates.md) | Alignment coop + related gates |
**Version:** 1.0
**Authority:** `game/data/qa/workflow_integration_registry.json`
**Gate:** `python3 tools/validate_workflow_integration.py` (`L0_workflow_integration`)
**Cross-refs:** `docs/ops/qa/ALIGNMENT_AUDIT.md`, `docs/ops/qa/AGENT_SESSION_TELEMETRY.md`

---

## Factory hooks (registry keywords)

- Portable pack: `packages/game-dev-factory/` · `game_dev_factory_pack` · `FACTORY_DATA_DIR`
- Alignment: `bash tools/run_alignment_audit.sh`

