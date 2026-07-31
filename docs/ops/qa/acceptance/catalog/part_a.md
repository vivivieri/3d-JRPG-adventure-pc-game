---
id: part-a
type: reference
phase: [1, 6]
audience: [qa, pm]
status: active
authority: qa
tokens_est: 884
summary: "Acceptance — Gate Catalog (A)"
---
# Acceptance — Gate Catalog — Acceptance — Gate Catalog (A)

**Hub:** [`gate_catalog.md`](../gate_catalog.md)

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
