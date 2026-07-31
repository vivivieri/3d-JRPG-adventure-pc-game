---
id: requirements-github
type: reference
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 706
summary: "Per-env requirements + GitHub Environments"
---
# Environments — Per-env requirements + GitHub Environments

**Hub:** [`ENVIRONMENTS.md`](../ENVIRONMENTS.md)

## When to read

Use **Environments — Per-env requirements + GitHub Environments** (roles: pm, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [3. Per-environment requirements](#3-per-environment-requirements)
- [Development](#development)
- [QA (automated)](#qa-automated)
- [UAT](#uat)
- [Preproduction (Steam beta)](#preproduction-steam-beta)
- [Production](#production)
- [4. GitHub Environments (recommended setup)](#4-github-environments-recommended-setup)


## 3. Per-environment requirements

### Development

| Item | Requirement |
|------|-------------|
| Branch | `game/development` |
| MCP stack | P0 required (`godot-mcp`, `godotiq`, `godot-mcp-pro`) |
| Gates | L0–L2 on commit (agent); L3 per scene change |
| Issues | GitHub Issues label `env/development` |
| Logs | Godot Output via GDAI; Godotiq debug console |

### QA (automated)

| Item | Requirement |
|------|-------------|
| Trigger | Every push/PR to `game/development` |
| Workflow | `.github/workflows/game-ci.yml` |
| Script | `bash tools/run_ci_checks.sh` |
| Pass | All `ci_gates.required_gates` exit 0 |
| Fail action | Open/update issue with label `gate/*` + `env/qa` |
| Artifacts | CI logs in GitHub Actions run |

### UAT

| Item | Requirement |
|------|-------------|
| Trigger | Tag `v*-rc*` or `v*-uat*` on `game/development` |
| Workflow | `.github/workflows/cd-artifact.yml` |
| Gates | `bash tools/run_cd_gates.sh --channel rc` |
| Deliverable | GitHub Release zip (`TidesOfUrashima-steam-depot-*.zip`) |
| Human | `docs/ops/qa/PLAYTEST_SCRIPT.md` — **after** L0–L5 on same commit |
| Issues | `env/uat`, severity S0–S3 |

### Preproduction (Steam beta)

| Item | Requirement |
|------|-------------|
| Trigger | Tag `v*-beta*` + manual `cd-steam.yml` |
| Gates | `run_cd_gates.sh --channel beta` (L5 required) |
| GitHub Environment | `steam-beta` (optional reviewers) |
| Secrets | `STEAM_*` per `docs/ops/ci-cd/CD.md` |
| Human | Beta playtest group; no S0/S1 open |

### Production

| Item | Requirement |
|------|-------------|
| Trigger | Tag `v*.*.*` + `cd-steam.yml` |
| Gates | L5 + L6 sign-off + `check_asset_compliance.sh` |
| GitHub Environment | `steam-production` |
| Merge | `game/development` → `main` after ship (per `BRANCHING.md`) |

---


## 4. GitHub Environments (recommended setup)

Configure in **Settings → Environments**:

| Environment | Protection | Used by |
|-------------|------------|---------|
| `qa` | None | Future: scheduled QA workflow |
| `uat` | None | Manual promote |
| `steam-beta` | None | `cd-steam.yml` channel=beta |
| `steam-production` | None | `cd-steam.yml` channel=prod |

---
