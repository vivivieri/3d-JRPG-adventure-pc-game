# Controls Cheat Sheet — How We Enforce Roles

**Version:** 1.4  
**Print this:** One-page reference for automated + process controls  
**Companion:** `docs/cheat-sheets/RR_CHEATSHEET.md` v1.1 (who does what — includes per-role **control hook** column)  
**Authority:** `docs/ci-cd/CI.md` · `game/data/qa/acceptance_criteria.json` · `docs/agents/PROJECT_MANAGEMENT.md`

---

## Golden rules

1. **Enforce outputs, not intentions** — gates PASS with evidence, or merge/tag is blocked.
2. **CI is the hard floor** — agent honor system fills gaps CI cannot see.
3. **WARN ≠ PASS · SKIP ≠ PASS** — on `game/development`, CI maps SKIP → FAIL via `tools/gate_lib.sh`.
4. **Builder proof** — scene changes require `.gdai_built` in the same PR (`L3_gdai_built`).
5. **Human L6** — only after L0–L5 pass.
6. **Cross-cutting factory features** — register in `workflow_integration_registry.json`; `bash tools/check_feature_integration.sh --remind` before merge (`docs/qa/WORKFLOW_INTEGRATION.md`).

---

## Control stack (strong → weak)

| # | Control | Blocks merge? | Blocks ship/tag? |
|---|---------|---------------|------------------|
| 1 | **GitHub Actions CI** | ✅ PR/push fail | ✅ via `run_cd_gates.sh` |
| 2 | **Branch protection** | ✅ when configured | — |
| 3 | **PR role checklist** | ⚠️ Review discipline | — |
| 4 | **Issue templates** | ⚠️ Required fields | — |
| 5 | **R&R scripts** | ✅ in CI | ✅ |
| 6 | **Remediation loop** | ⚠️ Process | ✅ anti-infinite-retry |
| 7 | **Phase exit gates** | — | ✅ phase promotion |
| 8 | **Pre-delivery control** | — | ✅ blocks outbound delivery until checks pass + **QA** approves (separation of duties; `docs/workflow/DELIVERY_CONTROL.md`) |
| 9 | **Agent rules** | — | — |

---

## Automated gates by branch

### `main` — `ci.yml` → `run_docs_ci_checks.sh`

| Gate | Enforces |
|------|----------|
| `L0_story_data` | Data JSON valid |
| `L0_acceptance_catalog` | Gate catalog schema |
| `L0_environments_catalog` | Env catalog |
| `L0_sprint_phases` | Sprint config |
| `L0_base_classes` | Code base class registry schema |
| `L0_zone_composition` | Zone composition contract |
| `L0_qa_catalog` | 3D model QA catalog |
| `L0_audio_qa_catalog` | BGM/VO QA catalog |
| `L0_scene_audio_map` | Scene/zone audio map |
| `L0_generation_readiness_backlog` | GR-* backlog traceability |
| `L0_sprint_board` | Sprint board + PM orchestrator state |
| `L0_workflow_integration` | Factory feature registry — hooks + doc parity |
| `L0_rr_compliance` | No ship scenes on main |
| `M5_asset_compliance` | License manifest |

### `game/development` — `game-ci.yml` → `run_ci_checks.sh`

| Gate | Role mainly enforced |
|------|----------------------|
| `L0_rr_compliance` | **Builder** — GDAI-verified ship `.tscn` only (`.gdai_built`) |
| `L0_story_data` | **Architect** / data |
| `L0_acceptance_catalog` | **QA** catalog |
| `L0_workflow_integration` | **PM** — factory feature registry parity |
| `L0_base_classes` | **Architect** — base class registry |
| `L1_unit_tests` | **Architect** |
| `L2_scene_primitives` | **Builder** / **Visual** |
| `L2_boot_headless` | **Builder** (when `main_scene` set) |
| `L3_gdai_built` | **Builder** — marker updated with scene diff |
| `L2_animation_whitelist` | **Builder** / **Visual** — required ⊆ Mixamo clips ⊆ whitelist |
| `L2_feel_smoke` | **Architect** — `GAME_FEEL.md` constants |
| `L2_perf_catalog` | **QA** / **Builder** — `perf_thresholds.json` catalog |
| `L2_glb_import` | **Builder** / **Visual** — post-import toon pipeline |
| `L1_gdscript_lint` | **Architect** — changed `.gd` files (`gdtoolkit` required) |
| `L0_base_class_compliance` | **Architect** — no rogue native extends |
| `L4_integration` | **Flow** |
| `M5_asset_compliance` | **Release** / compliance |

**Not in CI (agent-local):** `check_mcp_ready.sh`, full **L3 F5 viewport**, L2 jury, **L5 E2E**, **L6 human**.

---

## Per-role controls

| Role | Hard (automated) | Soft (process) |
|------|------------------|----------------|
| **PM** | `L0_sprint_board`; **`run_pm_orchestrator.sh` PASS** | Dispatch + escalation via `pm_emit_escalation.sh` |
| **Architect** | `L1_unit_tests`, `L1_gdscript_lint`, `L0_base_class_compliance` | Handoff + **base class** registry |
| **Builder** | `L0_rr_compliance`, `L2_*`, `L3_gdai_built`, `L2_animation_whitelist`, `L2_glb_import`, component scenes | `.gdai_built`; F5 in editor; `install_glb_import_pipeline.sh` |
| **QA** | CI must green; measurable thresholds in `acceptance_criteria.json` | Gate report in PR/issue; evidence paths |
| **Flow** | `L4_integration`; L5 in `run_cd_gates.sh` for beta/prod | MCP Pro `--minimal` only |
| **Debugger** | Godotiq read-only by policy | — |
| **Release** | `run_cd_gates.sh`; CD workflows; tag patterns | Steam secrets + env reviewers |
| **Visual** | L2 palette/model/audio/vo scripts when assets exist | Jury ≥2 models @ conf ≥ 0.65 |
| **Human** | L6 in ship checklist / CD prod (`min_testers: 5`, feel checklist §7b) | Playtest script + gate JSON |

---

## L3 split (important)

| Check | Script | Where |
|-------|--------|-------|
| **L3_gdai_built** (CI) | `check_l3_gdai_built.sh` | GitHub Actions — marker updated when scenes change |
| **L3_gdai_f5** (full) | GDAI F5 + editor | Agent session — viewport verify |
| **L3_perf_review** | Godotiq `perf_snapshot` | Agent session — FPS / draw calls / materials |

CI cannot run the editor; `L3_gdai_built` is the **merge blocker** for Builder handoffs.

---

## PR + GitHub controls

### PR templates (`.github/PULL_REQUEST_TEMPLATE/`)

| Template | Branch | Requires |
|----------|--------|----------|
| **game_development.md** | `game/development` | PM / Architect / Builder / QA checkboxes + gate report |
| **docs_main.md** | `main` | Docs-only checklist + `run_docs_ci_checks.sh` |

### Branch protection (`tools/setup_github_project.sh`)

| Branch | Status check | PR review |
|--------|--------------|-----------|
| `main` | Docs + design data gates | 1 approval (when admin PAT) |
| `game/development` | L0–L2 headless gates | 1 approval (when admin PAT) |

```bash
export GH_TOKEN=github_pat_...   # Cursor Secrets
bash tools/setup_github_project.sh
```

Manual fallback: `docs/ci-cd/GITHUB_SETUP.md` §2.

### Issue templates

| Template | Enforces |
|----------|----------|
| `feature_task.yml` | Phase, gate IDs, `agent_owner` |
| `gate_failure.yml` | Gate ID, SHA, remediation |
| `bug_report.yml` | Severity, env, repro |

Labels: `agent/*`, `gate/*`, `env/*` — see `docs/agents/PROJECT_MANAGEMENT.md` §2.

---

## Session startup (before scene work)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh       # blocks Builder without P0 MCP
bash tools/check_rr_compliance.sh
```

---

## Ship / CD controls

```bash
bash tools/run_cd_gates.sh --channel rc      # CI + assets
bash tools/run_cd_gates.sh --channel beta    # + L5 E2E required
bash tools/run_cd_gates.sh --channel prod    # + L6 policy
```

Tags on `game/development` only until M6 (`docs/ci-cd/CD.md`).

---

## Remediation (QA FAIL loop)

1. `bash tools/qa_emit_remediation.sh <brief-id>`
2. Change **one lever** (mesh / albedo / lighting / prompt — not all at once)
3. Re-run failing gate; paste evidence in issue
4. Same prompt twice → **blocked** after 2 attempts (`docs/qa/QA_REMEDIATION_LOOP.md`)

---

## Definition of done (merge)

- [ ] PR template checkboxes satisfied for touched roles
- [ ] All listed **gate IDs PASS** on PR commit (CI green)
- [ ] QA gate report in PR body with evidence paths
- [ ] Builder: `.gdai_built` updated if scenes changed
- [ ] Correct branch (`main` = docs/data; `game/development` = code)

---

## Quick verify commands

```bash
# game/development
bash tools/run_ci_checks.sh
bash tools/check_rr_compliance.sh
bash tools/check_l3_gdai_built.sh

# main
bash tools/run_docs_ci_checks.sh

# pre-tag
bash tools/run_cd_gates.sh --channel rc
```

---

## Related docs

| Doc | Contents |
|-----|----------|
| `docs/cheat-sheets/RR_CHEATSHEET.md` | Role ownership |
| `docs/ci-cd/CI.md` | Full CI matrix |
| `docs/qa/ACCEPTANCE_CRITERIA.md` | Gate thresholds |
| `docs/agents/PROJECT_MANAGEMENT.md` | Issues, labels, traceability |
| `docs/ci-cd/GITHUB_SETUP.md` | PAT + branch protection |
| `docs/qa/QA_REMEDIATION_LOOP.md` | FAIL iteration |
| `game/data/qa/acceptance_criteria.json` | Machine-readable gates |
