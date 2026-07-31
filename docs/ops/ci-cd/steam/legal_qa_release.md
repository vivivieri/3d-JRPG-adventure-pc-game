---
id: legal-qa-release
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 744
summary: "Legal, QA, release sequence, commands, refs"
---
# Steam Release Checklist — Legal, QA, release sequence, commands, refs

**Hub:** [`STEAM_RELEASE_CHECKLIST.md`](../STEAM_RELEASE_CHECKLIST.md)

## 5. Legal & compliance

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5.1 | `docs/asset_manifest.license.json` | ✅ | Maintained |
| 5.2 | `bash tools/check_asset_compliance.sh` | ✅ | Passes on main (marketing media only) |
| 5.3 | `docs/design/art/LICENSES.md` ship checklist | 🟡 | Template exists; credits screen not built |
| 5.4 | Godot MIT attribution | ❌ | In-game credits |
| 5.5 | Noto OFL attribution | ❌ | Fonts not bundled yet |
| 5.6 | GodotSteam MIT attribution | ❌ | Credits screen |
| 5.7 | ACE-Step / ElevenLabs ToS if used | 🟡 | VO/BGM plan documented; verify before ship |
| 5.8 | AI asset ToS (Meshy, GameLab, etc.) | 🟡 | Per-tool registration in manifest |
| 5.9 | Content survey / age rating | ❌ | Steamworks questionnaire |
| 5.10 | Privacy policy (if analytics) | ❌ | Only if telemetry added |

---


## 6. QA & operations

| # | Item | Status | Notes |
|---|------|--------|-------|
| 6.1 | CI on `game/development` | ✅ | `game-ci.yml` |
| 6.2 | CD artifact on tag | 🟡 | `cd-artifact.yml` (this PR) |
| 6.3 | L5 E2E three endings automated | ❌ | Stub until Phase 6 playable |
| 6.4 | L6 human playtest 80%+ completion | ❌ | `PLAYTEST_SCRIPT.md` |
| 6.5 | Bug triage S0/S1 = 0 open | ❌ | `docs/ops/qa/QA_AND_BUG_PROCESS.md` |
| 6.6 | Support contact / refund policy | ❌ | Steam requires support email |
| 6.7 | Post-launch patch branch strategy | ❌ | Define after 1.0 ship |
| 6.8 | Branch protection on `main` | 🟡 | Recommended in `docs/ops/ci-cd/CI.md` |

---


## 7. Release sequence (recommended order)

```
1. Complete Phases 1–7 on game/development
2. L0–L5 pass → tag v0.9.0-rc1 → CD artifact → internal testers
3. L6 human playtest → fix S0/S1
4. M5 final screenshots + capsules from 3D builds
5. Steamworks: app, depots, achievements, store page live (Coming Soon)
6. Register fonts/assets; credits screen; GodotSteam 4.20+
7. tag v1.0.0-beta1 → Steam beta branch
8. Beta feedback → tag v1.0.0 → manual Steam prod CD + store release
9. Merge game/development → main (one-time, per BRANCHING.md)
```

---


## 8. Quick commands before upload

```bash
git checkout game/development
bash tools/run_cd_gates.sh --channel prod    # after L5 exists
bash tools/install_godotsteam.sh
bash tools/export_windows.sh
bash tools/prepare_steam_depot.sh
bash tools/check_asset_compliance.sh
# Manual: upload build/steam_depot/ via Steamworks or cd-steam.yml
```

---


## 9. Cross-refs

- `docs/ops/ci-cd/CD.md` — automation
- `docs/ops/workflow/BRANCHING.md` — when to merge to `main`
- `docs/ops/workflow/MILESTONES.md` §M6 — milestone checklist
- `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase 8 — task list
