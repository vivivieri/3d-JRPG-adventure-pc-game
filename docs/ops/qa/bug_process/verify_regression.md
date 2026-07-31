---
id: verify-regression
type: how-to
phase: [1, 6]
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 711
summary: "Verification + regression suite"
---
# QA and Bug Process — Verification + regression suite

**Hub:** [`QA_AND_BUG_PROCESS.md`](../QA_AND_BUG_PROCESS.md)

## 5. Verification (definition of done)

A bug is **closed** only when:

1. **Fix merged** to target branch with clear commit message (`fix: SC-07 puzzle soft-lock when...`).
2. **Original steps** no longer reproduce on fixed build.
3. **Regression spot-check** from §6 (at minimum the act containing the fix).
4. **Automated checks** pass if data/assets touched:
   ```bash
   python3 tools/validate_story_data.py
   bash tools/check_asset_compliance.sh
   ```
5. **Related doc updated** if behavior was spec-defined (e.g. economy price, flag name).

### Verify matrix by area

| Area | Minimum verify |
|------|----------------|
| Story / quest | Load save before scene; replay scene; flag set in `user://` |
| Combat | Win and lose fight; check intent UI; boss phases |
| Save | Manual + autosave; load mid-act; game over reload |
| Ending | Reach SC-16; each choice once per full playtest cycle |
| Audio | Scene from `scene_audio_map.json` (mirror: `AUDIO_PRODUCTION_GUIDE.md` §4) |
| L10n | Switch language; revisit same scene |

---


## 6. Regression suite

Run before each milestone demo or playtest build.

### Automated (required)

```bash
python3 tools/validate_story_data.py
bash tools/check_asset_compliance.sh
```

### Smoke (15 min)

| # | Action | Pass |
|---|--------|------|
| 1 | Launch → title → new game | No crash |
| 2 | SC-00 skip or watch → SC-01 | Spawn OK |
| 3 | Walk village → SC-05 crab | Combat starts |
| 4 | Win combat → Tab menu | All tabs open |
| 5 | Save at well → quit → load | Position + flags OK |

### Full regression

Follow `PLAYTEST_SCRIPT.md` Acts I–III once per milestone. **Who runs it:** at **M2** and any
milestone where L5 has not yet passed, the regression is executed by **AI agents** (GDAI F5 +
Godot MCP Pro scripted runs — the golden rule in `AI_TESTING_SPEC.md` §1 forbids human playtests
before L0–L5 pass). **Human** testers run it at **M4+** only after L0–L5 are green (**M4** full
story, **M5** art pass, **M6** ship gate).

### Post-fix regression

When fixing a bug, always re-run:

- The **exact steps** from the report
- **One scene before and after** the affected scene
- **`L3_perf_review`** (Godotiq `perf_snapshot` → `artifacts/perf_reviews/`) when the fix touches scenes, shaders, materials, meshes, lights, or fog — on **`reference_pc_gtx1060` only** (`docs/ops/qa/PERFORMANCE_BASELINE.md`)
- **Affected `INT-*`** integration scenario when narrative/combat flows changed (`bash tools/run_integration_tests.sh`)
- **Automated checks** if any `game/data/` or `game/assets/` changed

---
