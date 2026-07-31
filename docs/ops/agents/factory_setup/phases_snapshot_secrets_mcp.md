---
id: phases-snapshot-secrets-mcp
type: tutorial
phase: [0, 1]
audience: [pm, architect]
status: active
authority: ops
tokens_est: 612
summary: "Factory Setup Guide — Snapshot, secrets, MCP — Dashboard: Cloud Agents → Environments"
---
# Factory Setup Guide — Snapshot, secrets, MCP

**Hub:** [`FACTORY_SETUP_GUIDE.md`](../FACTORY_SETUP_GUIDE.md)

## When to read

Use **Factory Setup Guide — Snapshot, secrets, MCP** (roles: pm, architect) when learning/setup for the first time Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [3. Phase 1 — Snapshot (one-time, human)](#3-phase-1-snapshot-one-time-human)
- [4. Phase 2 — Secrets (Environment → Secrets)](#4-phase-2-secrets-environment-secrets)
- [5. Phase 3 — MCP (Dashboard → Integrations & MCP)](#5-phase-3-mcp-dashboard-integrations-mcp)


## 3. Phase 1 — Snapshot (one-time, human)

**Dashboard:** [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game)

1. **Start Setup Agent** on branch `game/development` (not ad-hoc web chat).
2. Upload commercial zips to `game/addons/`:
   - `gdai-mcp-plugin-godot-*.zip`
   - `godot-mcp-pro*.zip`
3. Run:

   ```bash
   bash tools/rebuild_cloud_snapshot.sh
   ```

4. Enable Godotiq editor plugin (`docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` §4 step 4a).
5. Confirm:

   ```bash
   bash tools/check_mcp_ready.sh
   curl -sf http://127.0.0.1:3571/tools | head -c 100
   ```

6. **Save snapshot** in dashboard → copy id into `.cursor/environment.json`:

   ```json
   {
     "snapshot": "snapshot-YYYYMMDD-…",
     "install": "bash tools/install_cloud_dev.sh",
     "start": "bash tools/ensure_mcp_stack.sh"
   }
   ```

7. Commit and push on `game/development`.

**Pass:** new agent from Environment dashboard shows GDAI plugin on disk and `check_snapshot_boot.sh` PASS.

---


## 4. Phase 2 — Secrets (Environment → Secrets)

All day-one secrets (11, incl. webhook auth) — see `docs/ops/agents/CURSOR_SECRETS_SETUP.md`.

```bash
bash tools/check_day_one_secrets.sh
```

Mirror webhook **URL + auth** pairs in **GitHub repo Secrets** for Actions:

```bash
bash tools/setup_github_actions_secrets.sh
```

Agents must POST webhooks only via `tools/curl_cursor_webhook.sh` (`pm` | `alert` | `worker`) — see `game/data/qa/factory_automations.json` → `webhook_dispatch`.

---


## 5. Phase 3 — MCP (Dashboard → Integrations & MCP)

| Server | Required for |
|--------|----------------|
| `godot-mcp` | Builder (GDAI) |
| `godotiq` | Debug / perf |
| `godot-mcp-pro` | Flow L4/L5 |
| `gamelab-mcp` | UI art |

GameLab SSE config: `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` §5.

---
