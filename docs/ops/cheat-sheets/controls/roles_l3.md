---
id: roles-l3
type: reference
audience: [pm, builder, qa, release]
status: active
authority: ops
tokens_est: 465
summary: "Per-role controls + L3 split"
---
# Controls Cheat Sheet — Per-role controls + L3 split

**Hub:** [`CONTROLS_CHEATSHEET.md`](../CONTROLS_CHEATSHEET.md)

## Per-role controls

| Role | Hard (automated) | Soft (process) |
|------|------------------|----------------|
| **PM** | `L0_sprint_board`; **`run_pm_orchestrator.sh` PASS** | Dispatch + `run_post_agent_cycle.sh` enforcement |
| **Architect** | `L1_unit_tests`, `L1_gdscript_lint`, `L0_base_class_compliance` | Handoff + **base class** registry |
| **Builder** | `L0_rr_compliance`, `L2_*`, `L3_gdai_built`, `L2_animation_whitelist`, `L2_glb_import`, component scenes | `.gdai_built`; F5 in editor; `install_glb_import_pipeline.sh` |
| **QA** | CI must green; measurable thresholds in `acceptance_criteria.json` | Gate report in PR/issue; evidence paths |
| **Flow** | `L4_integration`; L5 in `run_cd_gates.sh` for beta/prod | MCP Pro `--minimal` only |
| **Debugger** | Godotiq read-only by policy | — |
| **Release** | `run_cd_gates.sh`; CD workflows; tag patterns | Steam secrets; CI gates only |
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
