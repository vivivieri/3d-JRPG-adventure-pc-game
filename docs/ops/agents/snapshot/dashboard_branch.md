---
id: dashboard-branch
type: tutorial
phase: [0, 1]
audience: [pm, builder, architect]
status: active
authority: ops
tokens_est: 1067
summary: "Dashboard branch + active snapshot + skip reasons"
---
# Cloud Snapshot Launch — Dashboard branch + active snapshot + skip reasons

**Hub:** [`CLOUD_SNAPSHOT_LAUNCH.md`](../CLOUD_SNAPSHOT_LAUNCH.md)

## When to read

Use **Cloud Snapshot Launch — Dashboard branch + active snapshot + skip reasons** (roles: pm, builder, architect) when learning/setup for the first time Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [0. Dashboard branch (no branch picker — bootstrap workaround)](#0-dashboard-branch-no-branch-picker-bootstrap-workaround)
- [1. Active snapshot (game/development)](#1-active-snapshot-gamedevelopment)
- [2. Why agents sometimes skip the snapshot](#2-why-agents-sometimes-skip-the-snapshot)


## 0. Dashboard branch (no branch picker — bootstrap workaround)

Cursor reads `.cursor/environment.json` from the **checked-out branch** (`recordedVia: REPO_FILE_OBSERVED`). The Cloud Environment editor **does not expose a repository branch picker** (Environment tab = Secrets/install; Git tab = Diff/Review/Commits only).

| Observed branch | `.cursor/environment.json` install | Result |
|-----------------|-----------------------------------|--------|
| **`main`** (default) | `bootstrap_cloud_environment.sh` | Auto-checkouts `game/development`, then `install_cloud_dev.sh` |
| **`game/development`** | `snapshot` + `install_cloud_dev.sh` + `ensure_mcp_stack.sh` | Full dev stack + pinned snapshot |

**Setup Agent / Update dev environment (no dashboard branch picker):**

1. Let the install script run — `bootstrap_cloud_environment.sh` on `main` will `git checkout game/development` automatically.
2. Or paste in the Setup Agent chat:

   ```bash
   git fetch origin game/development
   git checkout game/development
   bash tools/install_cloud_dev.sh
   bash tools/ensure_mcp_stack.sh
   ```

**Ad-hoc docs-only cloud agent on `main`** (not dev Environment): set secret or env `CLOUD_DOCS_ONLY=1` so bootstrap runs `install_main_ci.sh` only.

**Fix (agent — every Setup Agent session):**

```bash
bash tools/ensure_dev_environment_branch.sh
```

If FAIL → checkout `game/development` before any install or snapshot work.

---


## 1. Active snapshot (game/development)

Committed in `.cursor/environment.json` on branch **`game/development`** (template on `main`: `.cursor/environment.game-development.json.example`):

| Field | Value |
|-------|-------|
| **Snapshot ID** | `snapshot-20260731-6674a8af-9b2c-4315-a2ff-dd7e4d211b66` |
| **Saved** | 2026-07-31 |
| **Install** | `bash tools/install_cloud_dev.sh` |
| **Start** | `bash tools/ensure_mcp_stack.sh` |

**Dashboard:** [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game)

> **Gap (2026-07-21):** `origin/game/development` tip currently has the same pip-only `environment.json` as `main` and **no** `game/project.godot`. Until P1-00 restore lands, launch from the dashboard Environment that pins this snapshot id — do **not** trust repo JIT on the game branch tip. After restore: copy `.cursor/environment.game-development.json.example` → `.cursor/environment.json` on `game/development`, rebuild snapshot if plugins changed, commit + push.

> **After rebuilding the snapshot:** update the `snapshot` field in `.cursor/environment.json`, commit on `game/development`, and push.

---


## 2. Why agents sometimes skip the snapshot

| Symptom | Cause |
|---------|-------|
| `build: null` in environment metadata | Pod booted **JIT** from repo `environment.json`, not from env-build-manager |
| `source: Repository`, `recordedVia: REPO_FILE_OBSERVED` | Cursor read `.cursor/environment.json` from the checked-out branch |
| Only `pip3 install` ran | Agent started on **`main`** — minimal docs-only boot config |
| No Godot / GDAI / MCP stack | Snapshot not used, or snapshot never saved with commercial plugins |

**`main` vs `game/development`**

| Branch | `.cursor/environment.json` | Snapshot |
|--------|---------------------------|----------|
| `main` | `pip3 install … requirements-ci.txt` only | **None** — by design |
| `game/development` | `snapshot` + `install_cloud_dev.sh` + `ensure_mcp_stack.sh` | **Required** for scene/MCP work |

Do **not** expect a snapshot boot when launching an ad-hoc web agent on `main`.

---
