---
id: gamelab-gh
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 591
summary: "API key for **GameLab Studio MCP** (`gamelab-mcp`) — ink-wash UI frames, combat icon sheets, menu borders."
---
# Secrets — API Keys — GAMELAB + GH_TOKEN

**Hub:** [`api_keys.md`](../api_keys.md)

## When to read

Use **Secrets — API Keys — GAMELAB + GH_TOKEN** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [4. `GAMELAB_API_KEY`](#4-gamelab_api_key)
- [Steps](#steps)
- [5. `GH_TOKEN`](#5-gh_token)
- [Steps](#steps-1)


## 4. `GAMELAB_API_KEY`

**What it is:** API key for **GameLab Studio MCP** (`gamelab-mcp`) — ink-wash UI frames, combat icon sheets, menu borders.

### Steps

1. Sign up at [gamelabstudio.co](https://gamelabstudio.co/)
2. Dashboard / account → **API key** (or developer settings)
3. Copy the key
4. Cursor **Secrets** → `GAMELAB_API_KEY` → paste key
5. **Dashboard → Integrations & MCP** → register **gamelab-mcp** (SSE) if not already listed
6. Re-run on environment:

```bash
bash tools/install_extended_toolchain.sh
bash tools/check_extended_toolchain.sh
```

Automation **Builder** agents: **Tools → MCP ON → + Add Tool or MCP → gamelab-mcp**.

**Cross-ref:** `docs/ops/agents/MCP_STACK.md` § GameLab Studio MCP · `docs/design/art/ART_AUTOMATION_PIPELINE.md`

---



## 5. `GH_TOKEN`

**What it is:** GitHub fine-grained personal access token for shell `gh`, `pm_sync_github_issues.py`, `repository_dispatch`, and `setup_github_project.sh` (labels, branch protection).

> Cursor’s built-in GitHub integration ≠ `gh` in the Cloud Agent VM. **`GH_TOKEN` is required day one** for factory scripts.

### Steps

1. GitHub → **Settings** → **Developer settings** → **Fine-grained personal access tokens** → **Generate**
2. **Repository access:** Only `vivivieri/3d-JRPG-adventure-pc-game` (or your fork)
3. **Permissions:**

| Permission | Access |
|------------|--------|
| Issues | Read and write |
| Pull requests | Read and write |
| Actions | Read |
| Secrets | Read and write *(GitHub Actions repo secrets via `setup_github_actions_secrets.sh`)* |
| Contents | Read (and write if agents push via `gh`) |
| Administration | Read and write *(branch protection via setup script)* |

4. Generate → copy token (`github_pat_...` or classic `ghp_...`)
5. Cursor **Secrets** → `GH_TOKEN` → paste token
6. Verify:

```bash
export GH_TOKEN="your_token"
gh auth status
bash tools/setup_github_project.sh --dry-run
```

**Cross-ref:** `docs/ops/ci-cd/GITHUB_SETUP.md` §1

---
