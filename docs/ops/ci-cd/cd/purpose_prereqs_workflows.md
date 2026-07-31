---
id: purpose-prereqs-workflows
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 609
summary: "Purpose, prerequisites, workflows"
---
# Continuous Delivery — Purpose, prerequisites, workflows

**Hub:** [`CD.md`](../CD.md)

## 1. Purpose

CD automates **release builds** after CI passes. It does **not** replace human QA (L6) or Steamworks business setup.

| Channel | Trigger | Deploy target | L5 E2E required |
|---------|---------|---------------|-----------------|
| **RC** | Tag `v*-rc*` or `v*-uat*` | GitHub Release zip | No |
| **Beta** | Tag `v*-beta*` or manual | Steam beta depot | Yes |
| **Production** | Tag `v*.*.*` | Steam default depot | CI gates + L6 sign-off (automated where configured) |

**Tag from `game/development` only** — `main` has no `game/project.godot`.

---


## 2. Prerequisites

Before first CD run:

1. Game implementation on `game/development` (Phases 1–8)
2. `bash tools/run_ci_checks.sh` green on the tagged commit
3. For beta/prod: `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` passes
4. For prod: `artifacts/qa_reports/L6_human_playtest.json` with `status=pass`, ≥5 testers (`run_cd_gates.sh --channel prod`)
5. For Steam CD: GitHub Secrets configured (see §5)
6. Review `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` — many items are still open

---


## 3. Workflows

### 3.1 Artifact CD (`cd-artifact.yml`)

**Triggers:** push tags matching `v*-rc*`, `v*-uat*`, `v*-beta*`, `v*.*.*`

```
checkout → guard project.godot → install_ci_deps.sh
→ run_cd_gates.sh --channel <derived from tag>
→ install_godotsteam.sh → export_linux.sh → export_windows.sh
→ prepare_steam_depot.sh --platform all
→ zip steam_depot_linux + steam_depot_windows → GitHub Release
```

**Output:** Linux + Windows binaries and Steam depot zips (v1 requires both — `docs/ops/qa/PLATFORM_SUPPORT.md`).

### 3.2 Steam CD (`cd-steam.yml`)

**Triggers:** `workflow_dispatch` only (manual) until Steamworks secrets are configured.

Requires GitHub Environment **`steam-production`** (no required reviewers — CI gates only).

```
run_cd_gates.sh → export_linux + export_windows → prepare_steam_depot.sh --platform all
→ materialize app_build.vdf from example + secrets → steamcmd upload
```

**Template:** `steam/depot/app_build.vdf.example` (sed `@STEAM_APP_ID@` / `@STEAM_DEPOT_ID@`).

**Not automated by default** — Steam App ID, depot VDF, and credentials must exist first.

---
