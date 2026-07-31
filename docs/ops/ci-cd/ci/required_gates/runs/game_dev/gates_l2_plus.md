---
id: gates-l2-plus
type: reference
audience: [release, qa, pm]
phase: [6, 8]
status: active
authority: ci-cd
tokens_est: 615
summary: "See `docs/ops/qa/PLATFORM_SUPPORT.md` — Linux run on ubuntu CI; Windows **run** on windows-latest CI."
---
# CI — game/development Gates — L2+ / Windows / CD

**Hub:** [`part_b.md`](../part_b.md)

### `game/development` — `game-ci.yml` → `run_ci_checks.sh`

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L2_scene_primitives` | `bash tools/check_scene_visuals.sh` | 0 banned meshes in ship scenes |
| `L3_gdai_built` | `bash tools/check_l3_gdai_built.sh` | Exit 0 — **SKIP** when no scene diff; else `.gdai_built` updated + `verified_f5=true` |
| `L2_animation_whitelist` | `python3 tools/check_animation_whitelist.py --phase m5 --strict` | Exit 0 — required ⊆ clips ⊆ `allowed_animations` |
| `L2_feel_smoke` | `bash tools/run_feel_smoke_checks.sh` | Exit 0 — `feel_thresholds.json` + player constants |
| `L2_perf_catalog` | `bash tools/run_perf_review_checks.sh` | Exit 0 — perf baseline catalogs |
| `L2_linux_export_smoke` | `bash tools/run_linux_export_smoke.sh` | Exit 0 — Linux export + headless run; SKIP when no `project.godot` |
| `L2_windows_cross_export` | `bash tools/run_windows_cross_export.sh` | Exit 0 — Windows `.exe` cross-export on ubuntu; SKIP when no `project.godot` |
| `L2_glb_import` | `python3 tools/check_glb_import_scripts.py --strict` | Exit 0 — GLB `.import` post-import script set |
| `L2_boot_headless` | `godot4 --headless …` | Exit 0 when `run/main_scene` is set; exit **2** SKIP when unset |
| `L4_integration` | `bash tools/run_integration_tests.sh` | Exit 0 — `INT-BOOT-01`; fails if `integration_scenarios.json` required scenarios missing |
| `M5_asset_compliance` | `bash tools/check_asset_compliance.sh` | Exit 0 when manifest exists |

**Second job — `windows-export-run` (windows-latest):**

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L2_windows_export_run` | `bash tools/run_windows_export_run.sh` | Exit 0 — Windows export + native `.exe` headless run; **exit 2 SKIP → FAIL** (SKIP≠PASS) |

See `docs/ops/qa/PLATFORM_SUPPORT.md` — Linux run on ubuntu CI; Windows **run** on windows-latest CI.

**CD (`cd-artifact.yml`):** exports **Linux + Windows**, packages both Steam depot zips — required for v1 (`docs/ops/qa/PLATFORM_SUPPORT.md`).

---
