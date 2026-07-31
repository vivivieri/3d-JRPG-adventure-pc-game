---
id: gate-catalog
type: reference
audience: [qa, pm]
phase: [1, 6]
status: active
authority: qa
tokens_est: 1439
summary: "L0–L6 / ship gate ids + pass rules — open when wiring CI, remediating a named gate, or checking toolchain requirements"
---
# Acceptance — Gate Catalog

**Hub:** [`ACCEPTANCE_CRITERIA.md`](../ACCEPTANCE_CRITERIA.md)

## When to read

Use **Acceptance — Gate Catalog** (roles: qa, pm) when you need this reference during the current task Jump to a section below instead of reading end-to-end (8 sections).

## Jump to

- [L0 — Data & workflow](#l0-data-workflow)
- [L1 — Unit tests & lint](#l1-unit-tests-lint)
- [L2 — Smoke](#l2-smoke)
- [L2.5 — Candidate tournament (pre-merge, non-ship)](#l25-candidate-tournament-pre-merge-non-ship)
- [L3 — GDAI Builder handoff](#l3-gdai-builder-handoff)
- [L4 / L5 — Flow](#l4-l5-flow)
- [Ship](#ship)
- [Required toolchain (not optional)](#required-toolchain-not-optional)


### L0 — Data & workflow

| Gate ID | Pass when |
|---------|-----------|
| `L0_rr_compliance` | `check_rr_compliance.sh` exit 0 — ship `.tscn` requires `.gdai_built` with `verified_f5=true`; `main_scene` must match marker |
| `L0_story_data` | `validate_story_data.py` exit 0, **0 errors** |
| `L0_no_secrets` | `check_no_secrets.sh` exit 0 — no live keys in tracked files |
| `L0_ship_build_security` | `check_ship_build_security.sh` exit 0 — dev plugin strip policy |
| `L0_zone_composition` | `validate_zone_composition.py` exit 0 — zone composition contract schema |
| `L0_qa_catalog` | `validate_qa_catalog.py` exit 0 — model catalog + `animation_timing` floor |
| `L0_audio_qa_catalog` | `validate_audio_qa_catalog.py` exit 0 — audio catalog + brief cross-refs |
| `L0_scene_audio_map` | `validate_scene_audio_map.py` exit 0 — scene/zone audio map |
| `L0_base_classes` | `validate_base_classes.py` exit 0 — `base_classes.json` schema valid |
| `L0_base_class_compliance` | `check_base_class_compliance.sh` exit 0 — no rogue native `extends` (game branch) |


### L1 — Unit tests & lint

| Gate ID | Pass when |
|---------|-----------|
| `L1_unit_tests` | All registered tests return `""` (no error string) |
| `L1_gdscript_lint` | `check_gdscript_changed.sh` exit 0 on changed `.gd` files (exit 2 SKIP when no diff — FAIL on game branch) |


### L2 — Smoke

| Gate ID | Pass when |
|---------|-----------|
| `L2_boot_headless` | Godot headless boot exit 0 |
| `L2_scene_primitives` | `check_scene_visuals.sh` exit 0, 0 banned meshes |
| `L2_animation_whitelist` | `check_animation_whitelist.py` exit 0 — required ⊆ clips ⊆ `allowed_animations` |
| `L2_zone_composition` | `run_zone_composition_checks.sh` exit 0 — warn in early phases; `ZONE_COMPOSITION_STRICT=1` at M5 ship (**GR-003**) |
| `L2_feel_smoke` | `run_feel_smoke_checks.sh` exit 0 — `feel_thresholds.json` + player constants |
| `L2_linux_export_smoke` | `run_linux_export_smoke.sh` exit 0 — Linux export + headless run |
| `L2_windows_cross_export` | `run_windows_cross_export.sh` exit 0 — Windows .exe cross-built on Linux CI |
| `L2_windows_export_run` | `run_windows_export_run.sh` exit 0 on **windows-latest** CI — native .exe run |
| `L2_glb_import` | `check_glb_import_scripts.py --strict` exit 0 — post-import toon pipeline |
| `L2_visual_palette` | `avg_anchor_dist ≤ 85`, `bright_ratio ≤ 0.35` |
| `L2_visual_jury` | ≥2 models, all V1–V8 met, confidence ≥ 0.65 |
| `L2_model_technical` | Tris in `qa_catalog.json` range, textures ≥ min, no greybox on ship |
| `L2_model_jury` | ≥2 models, M1–M8 met, confidence ≥ 0.65 |
| `L2_audio_technical` | 44.1 kHz, LUFS/peak per bus table, no procedural on ship |
| `L2_audio_jury` | ≥2 models, A1–A7 met, confidence ≥ 0.65 (hero BGM tracks) |
| `L2_vo_technical` | P0 VO duration ≤ catalog max, voice loudness, locale paths vs dialogue |
| `L2_vo_jury` | ≥2 models, V1–V7 met, confidence ≥ 0.65 (P0 clips, gate locale `en`) |


### L2.5 — Candidate tournament (pre-merge, non-ship)

| Gate ID | Pass when |
|---------|-----------|
| `L2_candidate_select` | `run_candidate_tournament.sh` verdict `promote_challenger` + `comparison_*.json` artifact — **does not block ship**; required when M5 tournament policy applies |

See `docs/ops/qa/CANDIDATE_TOURNAMENT.md`.

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
