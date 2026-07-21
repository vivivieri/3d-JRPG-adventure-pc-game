# Steam Release Checklist — Technical & Non-Technical

**Version:** 1.0
**Milestone:** M6 (Phase 8)
**Authority:** Complete every **Blocker** before production Steam release.
**Cross-refs:** `docs/workflow/MILESTONES.md` §M6, `steam/STORE_PAGE.md`, `steam/GODOTSTEAM_SETUP.md`, `docs/art/ASSET_COMPLIANCE.md`

**Status key:** ✅ Done · 🟡 Partial · ❌ Missing · ⏳ Blocked on earlier phase

---

## Summary

| Category | Done | Partial | Missing |
|----------|------|---------|---------|
| Game complete | 0 | 0 | 12+ |
| Technical / build | 2 | 3 | 10+ |
| Steamworks setup | 0 | 0 | 8+ |
| Store & marketing | 4 | 2 | 6+ |
| Legal & compliance | 3 | 2 | 4+ |
| QA & ops | 1 | 1 | 5+ |

**Bottom line:** Documentation, story data, trailers, and export **scripts** exist. The **playable game**, **GodotSteam integration**, **store art from M5 builds**, and **Steamworks account setup** are not ship-ready.

---

## 1. Game complete (blockers — Phases 1–7)

All items ❌ until `game/development` phases land.

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1.1 | Playable game start → end (2–3 h) | ❌ | No `run/main_scene`; Phases 1–6 not built |
| 1.2 | SC-02 ruined village vertical slice | ❌ | Phase 1 gate |
| 1.3 | Boot + main menu + settings | ❌ | Phase 2; `LocalizationManager` deferred |
| 1.4 | Full Chapter 1 + dungeons | ❌ | Phases 3–5 |
| 1.5 | Three endings (Rewind / Anchor / Drift) | ❌ | Phase 6 + L5 E2E |
| 1.6 | M5 art rebuild (NPR zones, hero meshes) | ❌ | Phase 7 — placeholders only |
| 1.7 | 12 selective VO clips × locales | ❌ | Phase 7; data paths exist, no OGG clips |
| 1.8 | Credits screen with license attributions | ❌ | Required per `LICENSES.md` |
| 1.9 | Graphics presets (Low / Med / High) | ❌ | Phase 8.3 |
| 1.10 | `game/scenes/.gdai_built` + F5 verified | ❌ | R&R gate when `main_scene` set |
| 1.11 | L0–L5 all pass on RC commit | ❌ | `run_cd_gates.sh --channel prod` |
| 1.12 | L6 human playtest sign-off | ❌ | `docs/qa/PLAYTEST_SCRIPT.md` — after L5 |

---

## 2. Technical — build & engine

| # | Item | Status | Notes |
|---|------|--------|-------|
| 2.1 | `game/project.godot` on ship branch | 🟡 | On `game/development` only; stripped from `main` |
| 2.2 | `game/export_presets.cfg` | 🟡 | Example exists on dev branch; verify Windows preset |
| 2.3 | `tools/export_windows.sh` | ✅ | Strips GDAI autoload; headless export |
| 2.3a | `tools/export_linux.sh` | ✅ | Linux x86_64 export for Steam depot |
| 2.3b | `tools/run_linux_export_smoke.sh` | ✅ | Ubuntu CI — export + native headless run |
| 2.3c | `tools/run_windows_export_run.sh` | ✅ | **windows-latest** CI — export + .exe run |
| 2.3d | `tools/run_windows_cross_export.sh` | ✅ | Ubuntu CI — cross-export .exe (build only) |
| 2.4 | `tools/prepare_steam_depot.sh` | ✅ | Bundles exe + Steam DLLs |
| 2.5 | Godot 4.7 + export templates in CI/CD | ✅ | `install_ci_deps.sh` |
| 2.6 | GodotSteam **4.20+** installed | ❌ | `bash tools/install_godotsteam.sh` — v4.15 stale |
| 2.7 | `SteamManager.gd` runtime | ❌ | Documented only; not implemented |
| 2.8 | `AchievementManager` + flag hooks | ❌ | JSON exists; no runtime unlock code |
| 2.9 | GDAI / MCP plugins removed from export | ✅ | `godot_strip_dev_plugins.py` + `L0_ship_build_security` |
| 2.10 | Godotiq / MCP Pro removed from ship build | ✅ | Same strip list — verify on export smoke |
| 2.11 | Windows smoke on real hardware | ❌ | M6 — GTX 1060 class target |
| 2.12 | CD pipeline | 🟡 | `cd-artifact.yml` draft; Steam CD manual |
| 2.13 | `tools/run_cd_gates.sh` | ✅ | RC / beta / prod channel gates |
| 2.14 | Save system + optional Steam Cloud | ❌ | Phase 8 future per `TECHNICAL_DESIGN.md` |
| 2.15 | Noto fonts shipped in PCK | ❌ | Manifest lists fonts; files not on disk |
| 2.16 | PCK encryption + save HMAC (RC) | 🟡 | `docs/qa/SECURITY.md` §9; custom templates + `SHIP_RELEASE=1` |
| 2.17 | `SaveIntegrity` wired in `SaveSystem` | ❌ | Reference GDScript exists; Phase 8 |

---

## 3. Steamworks — platform setup

| # | Item | Status | Notes |
|---|------|--------|-------|
| 3.1 | Steamworks partner account | ❌ | $100 USD registration; tax/bank info |
| 3.2 | Steam App ID assigned | ❌ | `prepare_steam_depot.sh` uses test id **480** |
| 3.3 | Windows depot created | ❌ | Depot ID → GitHub Secret `STEAM_DEPOT_ID` |
| 3.4 | Depot VDF (`app_build_*.vdf`, `depot_build_*.vdf`) | ❌ | Not in repo — create in `steam/depot/` |
| 3.5 | `steamcmd` + build account | ❌ | For `cd-steam.yml` |
| 3.6 | GitHub Secrets (`STEAM_*`) | ❌ | See `docs/ci-cd/CD.md` §5 |
| 3.7 | Achievements registered in Steamworks | ❌ | 13 APIs per `ACHIEVEMENTS.md` / `achievements.json` |
| 3.8 | Achievement icons (64×64) | ❌ | Upload per achievement in partner site |
| 3.9 | Beta branch + playtest keys | ❌ | Internal testers before prod |
| 3.10 | Steam DRM / depots config | ✅ | **Policy: none** — `ship_security.json` → `steam_drm`; achievements via Steam API |

---

## 4. Store page & marketing

| # | Item | Status | Notes |
|---|------|--------|-------|
| 4.1 | Store copy EN | ✅ | `steam/STORE_PAGE.md` |
| 4.2 | Store copy JA | ❌ | `STORE_PAGE_ja.md` referenced but **not created** |
| 4.3 | Store copy ZH (Simplified) | ❌ | `STORE_PAGE_zh.md` **not created** |
| 4.4 | Store copy zh-Hant | ✅ | `steam/STORE_PAGE_zh-Hant.md` |
| 4.5 | Trailer EN / JA / ZH / zh-Hant | ✅ | `steam/trailer*.mp4` (~75s each) |
| 4.6 | Trailer BGM | ✅ | `steam/trailer_bgm.ogg` |
| 4.7 | Header capsule 1232×706 | ❌ | `steam/capsule_header.png` missing |
| 4.8 | Main capsule 616×353 | ❌ | `steam/capsule_main.png` missing |
| 4.9 | Small capsule 231×87 | ❌ | `steam/capsule_small.png` missing |
| 4.10 | Library hero 3840×1240 | ❌ | TODO in STORE_PAGE |
| 4.11 | Screenshots 1920×1080 (5+) | ❌ | `steam/screenshots/` **empty** — need M5 3D captures |
| 4.12 | Tags & categories set | 🟡 | Listed in STORE_PAGE; not live on Steamworks |
| 4.13 | Pricing (USD + regions) | 🟡 | Suggested $4.99–$7.99; not configured |
| 4.14 | Release date / Coming Soon | ❌ | Business decision |
| 4.15 | Wishlist campaign / press kit | ❌ | Non-technical marketing |

---

## 5. Legal & compliance

| # | Item | Status | Notes |
|---|------|--------|-------|
| 5.1 | `docs/asset_manifest.license.json` | ✅ | Maintained |
| 5.2 | `bash tools/check_asset_compliance.sh` | ✅ | Passes on main (marketing media only) |
| 5.3 | `docs/art/LICENSES.md` ship checklist | 🟡 | Template exists; credits screen not built |
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
| 6.5 | Bug triage S0/S1 = 0 open | ❌ | `docs/qa/QA_AND_BUG_PROCESS.md` |
| 6.6 | Support contact / refund policy | ❌ | Steam requires support email |
| 6.7 | Post-launch patch branch strategy | ❌ | Define after 1.0 ship |
| 6.8 | Branch protection on `main` | 🟡 | Recommended in `docs/ci-cd/CI.md` |

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

- `docs/ci-cd/CD.md` — automation
- `docs/workflow/BRANCHING.md` — when to merge to `main`
- `docs/workflow/MILESTONES.md` §M6 — milestone checklist
- `docs/workflow/IMPLEMENTATION_PLAN.md` §Phase 8 — task list
