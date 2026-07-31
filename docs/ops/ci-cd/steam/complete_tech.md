---
id: complete-tech
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 883
summary: "Steam Release Checklist — Game complete + build/engine — All items ❌ until `game/development` phases land."
---
# Steam Release Checklist — Game complete + build/engine

**Hub:** [`STEAM_RELEASE_CHECKLIST.md`](../STEAM_RELEASE_CHECKLIST.md)

## When to read

Use **Steam Release Checklist — Game complete + build/engine** (roles: release, pm) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Game complete (blockers — Phases 1–7)](#1-game-complete-blockers-phases-17)
- [2. Technical — build & engine](#2-technical-build-engine)


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
| 1.12 | L6 human playtest sign-off | ❌ | `docs/ops/qa/PLAYTEST_SCRIPT.md` — after L5 |

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
| 2.16 | PCK encryption + save HMAC (RC) | 🟡 | `docs/ops/qa/SECURITY.md` §9; custom templates + `SHIP_RELEASE=1` |
| 2.17 | `SaveIntegrity` wired in `SaveSystem` | ❌ | Reference GDScript exists; Phase 8 |

---
