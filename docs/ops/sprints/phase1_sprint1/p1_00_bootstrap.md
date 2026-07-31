---
id: p1-00-bootstrap
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 604
summary: "P1-00 bootstrap"
---
# Phase1-Sprint1 — P1-00 bootstrap

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## P1-00 — Bootstrap `game/development` (prerequisite)

**Title:** `[DEV][P1-00] Bootstrap game/development — project.godot + CI baseline`

**Labels:** `agent/pm`, `agent/architect`, `status/blocked` (until MCP secrets set)

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | Phase 0 verify + branch bootstrap |
| Lead agent | **pm** (Architect executes) |
| Blocks | P1-01, P1-02, P1-03, P1-04, P1-05 |

### Acceptance gate IDs

```
L0_rr_compliance
L0_story_data
L0_narrative_density
L0_acceptance_catalog
L0_base_classes
L1_unit_tests
L2_boot_headless          # SKIP until main_scene set — OK for this issue only
```

### Spec summary

Merge latest `main` into `game/development`. Run `bash tools/setup_dev_environment.sh`. Create minimal Godot 4.7 Forward+ project shell (`game/project.godot`, autoload stubs, `game/tests/unit/test_runner.gd`). No ship `.tscn` without GDAI — stub `run/main_scene` only when boot test is ready.

**Core helpers (R&R — `docs/engineering/technical/GDSCRIPT_REGENERATION.md` §2):**
- **Architect:** port `event_bus.gd` from `helpers_registry.json` (signals only)
- **Builder:** register `EventBus` autoload in `project.godot` via GDAI MCP
- Phase 2+ helpers (`SettingsStore`, `SaveIntegrity`, etc.) are **not** in P1-00 — PM dispatches per `helpers_registry.json` → `dispatch_by_phase`

Verify bootstrap CI (P1-00 profile — art/export gates deferred until `main_scene`):

```bash
bash tools/install_cloud_dev.sh
bash tools/install_extended_toolchain.sh
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_extended_toolchain.sh
bash tools/run_bootstrap_ci_checks.sh
```

Full game CI (`bash tools/run_ci_checks.sh`) is required after **P1-02** sets `run/main_scene` and GDAI scenes land.

### Design refs

- `docs/ops/workflow/BRANCHING.md`
- `docs/ops/agents/MCP_STACK.md`
- `AGENTS.md` — Environment bootstrap

### Definition of done

- [ ] `game/project.godot` exists on `game/development`
- [ ] **Architect:** `event_bus.gd` ported per `helpers_registry.json`
- [ ] **Builder:** `EventBus` autoload registered via GDAI MCP
- [ ] `bash tools/run_bootstrap_ci_checks.sh` exits 0 (or document any unexpected FAIL in PR)
- [ ] After P1-02: `bash tools/run_ci_checks.sh` exits 0 on merge commits that add `main_scene`
- [ ] MCP stack PASS (`check_mcp_ready.sh` + `check_extended_toolchain.sh`)
- [ ] PR merged to `game/development`

---
