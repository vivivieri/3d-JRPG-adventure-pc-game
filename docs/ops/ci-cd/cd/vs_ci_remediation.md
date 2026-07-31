---
id: vs-ci-remediation
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 383
summary: "- `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` — full ship gap list"
---
# Continuous Delivery — CD vs CI, remediation, refs

**Hub:** [`CD.md`](../CD.md)

## When to read

Use **Continuous Delivery — CD vs CI, remediation, refs** (roles: release, pm) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [6. CD vs CI](#6-cd-vs-ci)
- [7. Failure remediation](#7-failure-remediation)
- [8. Cross-refs](#8-cross-refs)


## 6. CD vs CI

| | CI | CD |
|---|----|----|
| **When** | Every push / PR | Tagged releases only |
| **Branch** | `main` (docs) + `game/development` (game) | Tags on `game/development` |
| **Output** | Pass/fail | `build/TidesOfUrashima.exe` + depot zip |
| **Ship** | No | RC → testers; beta/prod → Steam |

---


## 7. Failure remediation

| Failed step | Fix |
|-------------|-----|
| `game/project.godot missing` | Tag from `game/development`, not `main` |
| `run_ci_checks.sh` | Fix failing L0–L2 gate |
| `check_asset_compliance.sh` | Update `docs/asset_manifest.license.json` |
| L5 E2E | Complete Phase 6 playable build |
| L6 sign-off | Run `PLAYTEST_SCRIPT.md`; write `qa_write_gate_result.py --gate L6_human_playtest` |
| GodotSteam install | `GODOTSTEAM_VERSION=4.20 bash tools/install_godotsteam.sh` |
| Export fails | Check `game/export_presets.cfg`, templates installed |

---


## 8. Cross-refs

- `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` — full ship gap list
- `steam/GODOTSTEAM_SETUP.md` — depot layout
- `docs/ops/ci-cd/CI.md` — continuous integration
- `docs/ops/qa/ACCEPTANCE_CRITERIA.md` — L5/L6 gates
