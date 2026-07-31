---
id: part-b
type: reference
phase: [1, 6]
audience: [qa, pm]
status: active
authority: qa
tokens_est: 511
summary: "Acceptance — Gate Catalog (B)"
---
# Acceptance — Gate Catalog — Acceptance — Gate Catalog (B)

**Hub:** [`gate_catalog.md`](../gate_catalog.md)

### L3 — GDAI Builder handoff

| Gate ID | Pass when |
|---------|-----------|
| `L3_gdai_built` | `check_l3_gdai_built.sh` exit 0 — if ship scenes or `main_scene` changed in diff, `.gdai_built` updated with `verified_f5=true` |
| `L3_gdai_f5` | GDAI MCP F5 in editor — agent-local; not full CI |
| `L3_perf_review` | Godotiq `perf_snapshot` after F5 on **`reference_linux_cloud`** (snapshot) and/or **`reference_pc_gtx1060`** (Windows) — evidence with `baseline_id` — agent-local |


### L4 / L5 — Flow

| Gate ID | Pass when |
|---------|-----------|
| `L4_integration` | All `INT-*` scenarios pass, exit 0 |
| `L5_e2e_three_endings` | Exit 0, **not SKIP** (gate runs use `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` — the stub then exits 1), Rewind + Anchor + Drift |


### Ship

| Gate ID | Pass when |
|---------|-----------|
| `M5_asset_compliance` | `check_asset_compliance.sh` exit 0 |
| `L6_human_playtest` | ≥80% `PLAYTEST_SCRIPT.md`, feel checklist avg ≥3.5, ≥5 testers, 0 open S0/S1 — **required ship gate**; **after L5** (Phase 8 prod CD) |


### Required toolchain (not optional)

| Requirement | Check | Notes |
|-------------|-------|-------|
| GameLab MCP | `gamelab-mcp` + `GAMELAB_API_KEY`; `check_extended_toolchain.sh` | Procedural UI fallbacks OK for **asset output** only |
| Blender | `blender` in PATH; `check_extended_toolchain.sh` | M5 turntable QA (`docs/design/art/MODEL_QA.md` M3) |
| `game/development` CI | `run_ci_checks.sh` exit 0 | Required merge gate; fails until `project.godot` + tests exist |
| L6 human playtest | `L6_human_playtest` gate | Phase 8 only; after L0–L5 — still **required** for ship |

Machine-readable: `acceptance_criteria.json` → `toolchain_requirements`.

Full thresholds: `game/data/qa/acceptance_criteria.json`.

---
