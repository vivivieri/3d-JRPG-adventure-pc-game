# GitHub Repository Setup

**Script:** `bash tools/setup_github_project.sh`  
**Requires:** `GH_TOKEN` with **Issues**, **Pull requests**, **Actions**, and **Administration** (for branch protection)  
**How to create token:** `docs/CURSOR_SECRETS_SETUP.md` §5 (day-one compulsory)  
**Cross-refs:** `docs/PROJECT_MANAGEMENT.md`, `docs/ENVIRONMENTS.md`

---

## 1. Quick setup (recommended)

### Step A — Create a token

1. GitHub → **Settings** → **Developer settings** → **Fine-grained personal access token**
2. Repository access: **Only** `vivivieri/3d-JRPG-adventure-pc-game` (or your fork)
3. Permissions:
   - Issues: Read and write
   - Pull requests: Read and write
   - Actions: Read
   - Administration: Read and write *(branch protection)*
4. Copy the token (`github_pat_...` or classic `ghp_...`)

### Step B — Run setup

**Cursor Cloud:** add token to **Secrets** tab as `GH_TOKEN`, then ask agent to run:

```bash
bash tools/setup_github_project.sh
```

**Local:**

```bash
export GH_TOKEN=github_pat_xxxxxxxx
bash tools/setup_github_project.sh
# Preview only:
bash tools/setup_github_project.sh --dry-run
```

### What the script creates

| Item | Count / names |
|------|----------------|
| **Labels** | 23 — `env/*`, `severity/S*`, `gate/*`, `domain/*`, `agent/*`, `status/*` |
| **Milestones** | M1-core, M5-art, M6-steam |
| **Environments** | `qa`, `uat`, `steam-beta`, `steam-production` |
| **Branch protection** | `main` + `game/development` — CI status + **1 PR review** (when `GH_TOKEN` admin) |

**Already in repo (no script needed):** issue templates, PR templates, CI/CD/QA workflows.

---

## 2. Manual UI setup (if script fails)

### Labels

**Settings → Labels → New label** — create each from `docs/PROJECT_MANAGEMENT.md` §2.

Minimum set to start:

```
env/development   env/qa   env/uat
severity/S0       severity/S1
agent/builder     agent/qa
status/in-progress   status/done
```

### Environments

**Settings → Environments → New environment**

| Name | Protection |
|------|------------|
| `qa` | None |
| `uat` | Optional: 1 reviewer |
| `steam-beta` | Required reviewers: 1 |
| `steam-production` | Required reviewers: 2 |

Used by: `qa-nightly.yml`, `cd-steam.yml`

### Branch protection

**Settings → Branches → Add branch ruleset**

**`main`:**

- Require status check: **Docs + design data gates**
- Require pull request before merging
- Require **1 approving review**

**`game/development`:**

- Require status check: **L0–L2 headless gates**
- Require pull request before merging
- Require **1 approving review**
- Do not require merge to main (long-lived dev branch)

### GitHub Projects board

1. **Projects** tab → **New project** → Board
2. Columns: Backlog → Ready → In Progress → QA → UAT → Done
3. Auto-add issues from repo optional

### Milestones

**Issues → Milestones → New**

| Title | Description |
|-------|-------------|
| M1-core | Phases 2–3 |
| M5-art | Phase 7 art rebuild |
| M6-steam | Phase 8 Steam ship |

---

## 3. Secrets for CD (Phase 8 only)

**Settings → Secrets and variables → Actions**

| Secret | When needed |
|--------|-------------|
| `STEAM_USERNAME` | Steam beta/prod CD |
| `STEAM_PASSWORD` | Steam beta/prod CD |
| `STEAM_APP_ID` | After Steamworks app created |
| `STEAM_DEPOT_ID` | After Windows depot created |

`GH_TOKEN` is for **setup script only** — do not confuse with Steam secrets.

---

## 4. Verify setup

```bash
gh label list --limit 30
gh api repos/$(gh repo view -q .nameWithOwner)/environments --jq '.environments[].name'
```

Open a test issue using template **Gate failure** — labels should apply.

---

## 5. Optional MCP (not GitHub)

| Tool | Setup |
|------|-------|
| **Linear** | Cursor → Integrations → Linear MCP → authenticate |
| **Notion** | Cursor → Integrations → Notion MCP → authenticate |

Game design authority stays in `docs/` + `game/data/` — PM tools track work only.

---

## 6. Troubleshooting

| Error | Fix |
|-------|-----|
| `GH_TOKEN not set` | Add to Cursor Secrets or `export GH_TOKEN=...` |
| Branch protection 403 | Need repo admin + GitHub Pro for private rules on free org |
| Label already exists | Script uses `--force` / PATCH — safe to re-run |
| Environment not in workflow | First workflow run auto-creates; script pre-creates for reviewers |
