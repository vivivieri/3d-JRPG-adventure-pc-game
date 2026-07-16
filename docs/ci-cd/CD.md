# Continuous Deployment — Artifact & Steam

**Version:** 1.1  
**Workflows:** `.github/workflows/cd-artifact.yml` · `.github/workflows/cd-steam.yml`  
**Gate script:** `bash tools/run_cd_gates.sh`  
**Steam checklist:** `docs/ci-cd/STEAM_RELEASE_CHECKLIST.md`  
**Branch policy:** `docs/workflow/BRANCHING.md`

---

## 1. Purpose

CD automates **release builds** after CI passes. It does **not** replace human QA (L6) or Steamworks business setup.

| Channel | Trigger | Deploy target | L5 E2E required |
|---------|---------|---------------|-----------------|
| **RC** | Tag `v*-rc*` | GitHub Release zip | No |
| **Beta** | Tag `v*-beta*` or manual | Steam beta depot | Yes |
| **Production** | Tag `v*.*.*` + approval | Steam default depot | Yes + L6 sign-off |

**Tag from `game/development` only** — `main` has no `game/project.godot`.

---

## 2. Prerequisites

Before first CD run:

1. Game implementation on `game/development` (Phases 1–8)
2. `bash tools/run_ci_checks.sh` green on the tagged commit
3. For beta/prod: `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` passes
4. For prod: `artifacts/qa_reports/L6_human_playtest.json` with `status=pass`, ≥5 testers (`run_cd_gates.sh --channel prod`)
5. For Steam CD: GitHub Secrets configured (see §5)
6. Review `docs/ci-cd/STEAM_RELEASE_CHECKLIST.md` — many items are still open

---

## 3. Workflows

### 3.1 Artifact CD (`cd-artifact.yml`)

**Triggers:** push tags matching `v*-rc*`, `v*-beta*`, `v*.*.*`

```
checkout → guard project.godot → install_ci_deps.sh
→ run_cd_gates.sh --channel <derived from tag>
→ install_godotsteam.sh → export_windows.sh → prepare_steam_depot.sh
→ zip build/steam_depot → GitHub Release
```

**Output:** `TidesOfUrashima-steam-depot-<tag>.zip` attached to GitHub Release.

### 3.2 Steam CD (`cd-steam.yml`)

**Triggers:** `workflow_dispatch` only (manual) until Steamworks secrets are configured.

Requires GitHub Environment **`steam-production`** with required reviewers for prod uploads.

```
run_cd_gates.sh → export → prepare_steam_depot.sh → steamcmd upload
```

**Not automated by default** — Steam App ID, depot VDF, and credentials must exist first.

---

## 4. Local CD (same gates as CI runner)

```bash
git checkout game/development
git tag v0.1.0-rc1
git push origin v0.1.0-rc1          # triggers cd-artifact.yml

# Or locally without pushing:
bash tools/run_cd_gates.sh --channel rc
bash tools/install_godotsteam.sh
bash tools/export_windows.sh
bash tools/prepare_steam_depot.sh
```

---

## 5. GitHub Secrets (Steam — Phase 8)

| Secret | Purpose |
|--------|---------|
| `STEAM_USERNAME` | Steamworks build account |
| `STEAM_PASSWORD` | Account password (or use Steam Guard token flow) |
| `STEAM_APP_ID` | Your game's App ID (not 480) |
| `STEAM_DEPOT_ID` | Windows depot ID from Steamworks |

Optional: store `steam/depot/*.vdf` in repo (without secrets) once App ID is assigned.

---

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

- `docs/ci-cd/STEAM_RELEASE_CHECKLIST.md` — full ship gap list
- `steam/GODOTSTEAM_SETUP.md` — depot layout
- `docs/ci-cd/CI.md` — continuous integration
- `docs/qa/ACCEPTANCE_CRITERIA.md` — L5/L6 gates
