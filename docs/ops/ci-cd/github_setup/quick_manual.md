---
id: quick-manual
type: tutorial
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 867
summary: "Quick setup + manual UI"
---
# GitHub Setup — Quick setup + manual UI

**Hub:** [`GITHUB_SETUP.md`](../GITHUB_SETUP.md)

## 1. Quick setup (recommended)

### Step A — Create a token

1. GitHub → **Settings** → **Developer settings** → **Fine-grained personal access token**
2. Repository access: **Only** `vivivieri/3d-JRPG-adventure-pc-game` (or your fork)
3. Permissions:
   - Issues: Read and write
   - Pull requests: Read and write
   - Actions: Read
   - Secrets: Read and write *(repo Actions secrets — `bash tools/setup_github_actions_secrets.sh`)*
   - Administration: Read and write *(branch protection)*
4. Copy the token (`github_pat_...` or classic `ghp_...`)

### Step B — Run setup

**Cursor Cloud:** add token to **Secrets** tab as `GH_TOKEN`, then ask agent to run:

```bash
bash tools/setup_github_project.sh
bash tools/setup_github_actions_secrets.sh   # webhook URL + auth → GitHub Actions
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
| **Environments** | `qa`, `uat`, `steam-beta`, `steam-production` — no required reviewers |
| **Branch protection** | `main` + `game/development` — CI status only (**no PR review required**) |
| **Git LFS** | `.gitattributes` + `tools/install_git_lfs.sh` — see `docs/ops/ci-cd/GIT_LFS.md` |

**GitHub Environments:** `qa`, `uat`, `steam-beta`, `steam-production` — **no required reviewers** (CI gates only). Re-apply with:

```bash
bash tools/setup_github_project.sh
```

**Already in repo (no script needed):** issue templates, PR templates, CI/CD/QA workflows with GitHub Environment gates.

---


## 2. Manual UI setup (if script fails)

### Labels

**Settings → Labels → New label** — create each from `docs/ops/agents/PROJECT_MANAGEMENT.md` §2.

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
| `uat` | None (CI gates on RC tags) |
| `steam-beta` | None (CI gates on beta CD) |
| `steam-production` | None (CI gates on prod CD) |

Used by: `qa-nightly.yml`, `cd-artifact.yml`, `cd-steam.yml`

### Branch protection

**Settings → Branches → Add branch ruleset**

**`main`:**

- Require status check: **Docs + design data gates**
- Require pull request before merging
- **Do not** require approving reviews (CI-only merge)

**`game/development`:**

- Require status check: **L0–L2 headless gates**
- Require pull request before merging
- **Do not** require approving reviews (CI-only merge)
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
