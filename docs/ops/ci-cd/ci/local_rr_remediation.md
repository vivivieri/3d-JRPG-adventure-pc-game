---
id: local-rr-remediation
type: reference
audience: [release, qa, pm]
status: active
authority: ci-cd
tokens_est: 669
summary: "Local repro, R&R, remediation"
---
# Continuous Integration — Local repro, R&R, remediation

**Hub:** [`CI.md`](../CI.md)

## 4. Local reproduction

**Main branch (docs/data):**

```bash
bash tools/run_docs_ci_checks.sh
```

**Game branch (`game/development`):**

```bash
bash tools/install_ci_deps.sh
bash tools/run_ci_checks.sh
```

Full dev smoke (includes extended toolchain + jury when assets exist):

```bash
bash tools/install_cloud_dev.sh   # requires GDAI stack for scene work
bash tools/run_playtest_smoke.sh
```

---


## 5. R&R alignment (`.cursorrules` §0)

CI **hard-blocks**:

- Ship `.tscn` without valid `game/scenes/.gdai_built` (`verified_f5=true`)
- `run/main_scene` set without matching `.gdai_built` + `verified_f5=true`
- Ship scene or `main_scene` changed in PR without updating `.gdai_built` (`L3_gdai_built`)
- Rogue native `extends` outside registered base classes (`L0_base_class_compliance`)
- Changed `.gd` files failing `gdlint` (`L1_gdscript_lint`) — `gdtoolkit` required on game branch
- Rigged GLB: missing `required_animations`, extra clip names, or missing post-import script (`L2_animation_whitelist`, `L2_glb_import`)
- Game-feel constants missing when `FEEL_SMOKE_STRICT=1` (`L2_feel_smoke`)

**MCP autoloads:** `tools/with_ci_godot.sh` strips dev-only GDAI/MCP Pro autoloads when commercial addons are absent (clean GitHub checkout). Does not install or require MCP.

CI **does not** replace full L3 F5 viewport verify in the editor — `L3_gdai_built` catches the common bypass (scene diff without Builder marker).

---


## 6. Failure remediation

| Failed gate | Fix |
|-------------|-----|
| `L0_rr_compliance` | Remove hand `.tscn` or build via GDAI MCP + write `.gdai_built` |
| `L0_story_data` | Fix JSON cross-refs; run `python3 tools/validate_story_data.py` |
| `L0_base_classes` | Fix `game/data/code/base_classes.json` schema; see `docs/engineering/technical/CODE_BASE_CLASS_RULES.md` |
| `L0_base_class_compliance` | Extend `PlayerController` / `Combatant` / `Interactable` bases — no rogue native `extends` |
| `L1_unit_tests` | Fix failing test in `game/tests/unit/` |
| `L1_gdscript_lint` | Fix `gdlint` warnings; run `bash tools/install_ci_deps.sh` if missing |
| `L2_scene_primitives` | Replace `BoxMesh` etc. with real assets or move to `greybox/` |
| `L2_animation_whitelist` | Add missing required clips or update `qa_catalog.json` |
| `L2_feel_smoke` | Add `INPUT_LATENCY` etc. per `game/data/qa/feel_thresholds.json` |
| `L2_glb_import` | `bash tools/install_glb_import_pipeline.sh` then reimport GLBs |
| `L3_gdai_built` | Rebuild scene via GDAI MCP; update `game/scenes/.gdai_built` |
| `M5_asset_compliance` | Update `docs/asset_manifest.license.json` |

See `docs/ops/qa/QA_REMEDIATION_LOOP.md` for structured remediation briefs.

---
