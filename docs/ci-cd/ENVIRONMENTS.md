# Deployment Environments — Dev · QA · UAT · Preprod · Prod

**Version:** 1.0  
**Machine-readable:** `game/data/qa/environments.json`  
**Cross-refs:** `docs/workflow/BRANCHING.md`, `docs/ci-cd/CD.md`, `docs/ci-cd/CI.md`, `docs/agents/MULTI_AGENT_TEAM.md`

---

## 1. Environment map

| Environment | Purpose | Git ref | CD / artifact | Human gate | Agent owner |
|-------------|---------|---------|---------------|------------|-------------|
| **Design** | Docs + story JSON only | `main` | — | — | PM + Architect |
| **Development** | Daily implementation | `game/development` | — | — | Builder + Architect |
| **QA** | Automated test gates | `game/development` @ CI green | — | — | QA Agent |
| **UAT** | Stakeholder / playtest builds | Tag `v*-rc*` or `v*-uat*` | `cd-artifact.yml` → GitHub Release (draft) | L6 playtest script | QA Lead + Human |
| **Preproduction** | Steam beta / near-final | Tag `v*-beta*` | `cd-steam.yml` → Steam **beta** depot | Beta testers | Release Agent |
| **Production** | Steam public | Tag `v*.*.*` | `cd-steam.yml` → Steam **default** depot | Manual approval | Release + PM |

```
main (design)
  │
game/development ──CI──► QA (automated)
  │
  ├── tag v0.8.0-uat1 ──CD artifact──► UAT (humans)
  │
  ├── tag v0.9.0-beta1 ──CD steam──► Preprod (Steam beta)
  │
  └── tag v1.0.0 ──CD steam + approval──► Production
```

---

## 2. Is preproduction necessary?

**For this project (2–3 h indie, small AI team):**

| Approach | When to use |
|----------|-------------|
| **Skip separate preprod early** | Phases 1–6: UAT RC zips from `cd-artifact.yml` are enough for internal + friend playtest |
| **Add preprod at M6** | When Steamworks beta branch exists and you need real depot keys, achievements, and store-linked builds |

**Recommendation:** Treat **UAT** = internal RC artifacts; **Preproduction** = Steam beta channel only. Do not build separate infra until Phase 8 — one beta tag (`v*-beta*`) is sufficient.

Preprod is **not** a duplicate of QA. QA is automated gates on every push; preprod is a **near-ship binary** on Steam's beta branch.

---

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
| Human | `docs/qa/PLAYTEST_SCRIPT.md` — **after** L0–L5 on same commit |
| Issues | `env/uat`, severity S0–S3 |

### Preproduction (Steam beta)

| Item | Requirement |
|------|-------------|
| Trigger | Tag `v*-beta*` + manual `cd-steam.yml` |
| Gates | `run_cd_gates.sh --channel beta` (L5 required) |
| GitHub Environment | `steam-beta` (optional reviewers) |
| Secrets | `STEAM_*` per `docs/ci-cd/CD.md` |
| Human | Beta playtest group; no S0/S1 open |

### Production

| Item | Requirement |
|------|-------------|
| Trigger | Tag `v*.*.*` + `cd-steam.yml` + **required approvers** |
| Gates | L5 + L6 sign-off + `check_asset_compliance.sh` |
| GitHub Environment | `steam-production` |
| Merge | `game/development` → `main` after ship (per `BRANCHING.md`) |

---

## 4. GitHub Environments (recommended setup)

Configure in **Settings → Environments**:

| Environment | Protection | Used by |
|-------------|------------|---------|
| `qa` | None | Future: scheduled QA workflow |
| `uat` | Optional: require reviewer for prod-like RC | Manual promote |
| `steam-beta` | 1 reviewer | `cd-steam.yml` channel=beta |
| `steam-production` | 2 reviewers | `cd-steam.yml` channel=prod |

---

## 5. Promotion rules

| From → To | Promotion criteria |
|-----------|-------------------|
| Dev → QA | Push to `game/development`; **CI green required** (bootstrap `project.godot` + tests first) |
| QA → UAT | All phase gates for milestone; tag RC |
| UAT → Preprod | L6 playtest ≥80%; S0/S1 = 0; Steamworks ready |
| Preprod → Prod | Beta soak complete; store page live; compliance pass |

**Never promote with SKIP gates** (`skip_is_not_pass` in `acceptance_criteria.json`).

---

## 6. Log & trace correlation

Every environment run should be traceable:

| Field | Where |
|-------|--------|
| Commit SHA | GitHub Actions run, issue body |
| Gate ID | `L0_story_data`, `L4_integration`, etc. |
| Agent session | Cloud agent URL or Cursor run ID |
| Artifacts | `artifacts/screenshots/`, `artifacts/test-reports/`, Actions logs |
| Remediation | `bash tools/qa_emit_remediation.sh <brief-id>` |

Issue title format: `[ENV][S1][L4] Short description`  
Example: `[UAT][S1][L5] Drift ending soft-lock at SC-16`

---

## 7. Cross-refs

- `docs/agents/PROJECT_MANAGEMENT.md` — issues, labels, MCP PM tools
- `docs/agents/MULTI_AGENT_TEAM.md` — which agent owns each environment
- `docs/ci-cd/CD.md` — artifact and Steam deploy
- `docs/ci-cd/STEAM_RELEASE_CHECKLIST.md` — prod readiness
