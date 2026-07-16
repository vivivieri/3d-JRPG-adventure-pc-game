# Cloud Snapshot ID & Launch Checklist

**Authority:** How to boot **game/development** Cloud Agents from the saved environment snapshot — not JIT from `main`.  
**Cross-refs:** `docs/GDAI_CLOUD_SETUP.md` · `docs/MCP_STACK.md` · `.cursor/environment.json`

---

## 1. Active snapshot (game/development)

Committed in `.cursor/environment.json` on branch **`game/development`**:

| Field | Value |
|-------|-------|
| **Snapshot ID** | `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8` |
| **Saved** | 2026-07-14 |
| **Install** | `bash tools/install_cloud_dev.sh` |
| **Start** | `bash tools/ensure_mcp_stack.sh` |

**Dashboard:** [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game)

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

## 3. Launch checklist (every implementation session)

### Before starting the agent

- [ ] Open [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game) (not a bare “new chat” on `main`)
- [ ] Branch = **`game/development`**
- [ ] Snapshot in dashboard matches `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8` (or newer if rebuilt)
- [ ] **Cursor Secrets** set — see `docs/CURSOR_SECRETS_SETUP.md` (`GAMELAB_API_KEY`, `GH_TOKEN`, webhooks, etc.)
- [ ] **Dashboard → Integrations & MCP** — all four servers registered:

| Server | Transport | Notes |
|--------|-----------|-------|
| `godot-mcp` | stdio (`uv run …/gdai_mcp_server.py`) | Requires GDAI plugin in snapshot |
| `godotiq` | stdio (`uvx godotiq`) | |
| `godot-mcp-pro` | stdio (`node …/index.js --minimal`) | |
| `gamelab-mcp` | `mcp-remote` bridge | SSE-only server — see §5 |

### First commands in the agent (after boot)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_extended_toolchain.sh
```

### Verify snapshot boot (agent or Setup Agent)

Ask the agent to run **cursor-cloud `environment-info`**, or check boot metadata:

| Check | Snapshot boot PASS | JIT boot FAIL |
|-------|-------------------|---------------|
| `build` | Has `buildId` / `snapshotId` | `null` |
| `godot4` in PATH | Yes | No |
| `game/addons/gdai-mcp-plugin-godot/` | Present | Missing |
| `curl -sf http://127.0.0.1:3571/tools` | JSON response | Connection refused |

If any FAIL → **STOP** scene work; fix launch path or rebuild snapshot (§4).

---

## 4. Rebuild snapshot (one-time or after toolchain change)

1. Dashboard → environment → **Start Setup Agent**
2. Checkout `game/development`:

   ```bash
   git fetch origin game/development
   git checkout game/development
   ```

3. Upload GDAI purchase zip (not in git):

   ```
   game/addons/gdai-mcp-plugin-godot-YYYYMMDD.zip
   ```

4. Bootstrap:

   ```bash
   bash tools/install_cloud_dev.sh
   bash tools/install_gdai_plugin.sh
   bash tools/install_extended_toolchain.sh
   bash tools/ensure_mcp_stack.sh
   bash tools/check_mcp_ready.sh
   bash tools/check_extended_toolchain.sh
   curl -sf http://127.0.0.1:3571/tools | head -c 100
   ```

5. **Save snapshot** in the dashboard
6. Copy the new snapshot id into `.cursor/environment.json` on `game/development`
7. Commit and push; register MCP servers in the dashboard

**Snapshot must include:** Godot 4.7, GDAI plugin, Godotiq, MCP Pro build, Blender, `uv`, Node — see `docs/GDAI_CLOUD_SETUP.md` §4.

---

## 5. GameLab MCP (`gamelab-mcp`) — known Cursor transport issue

GameLab’s endpoint is **SSE-only** (`GET /sse` → 200; `POST /sse` → 405). Cursor may show:

> Streamable HTTP error: Error POSTing to endpoint: Method Not Allowed

**Workaround** — register via `mcp-remote` in Dashboard → Integrations & MCP:

```json
{
  "mcpServers": {
    "gamelab-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://api.gamelabstudio.co:8765/sse",
        "--transport",
        "sse-only",
        "--allow-http",
        "--header",
        "X-API-Key:${GAMELAB_API_KEY}"
      ],
      "env": {
        "GAMELAB_API_KEY": "set-in-cursor-secrets"
      }
    }
  }
}
```

Store the key in **Cursor Secrets** as `GAMELAB_API_KEY` — never commit it.

---

## 6. Quick troubleshooting

| Problem | Fix |
|---------|-----|
| `build: null` | Launch from environment dashboard on `game/development`, not JIT on `main` |
| GDAI bridge down | Rebuild snapshot with plugin; run `bash tools/ensure_gdai_mcp.sh` |
| `gamelab-mcp` 405 error | Use `mcp-remote` config (§5) |
| Stale snapshot after Godot/MCP upgrade | Re-run §4, save new snapshot, update `snapshot` id in `environment.json` |
| Docs/data only work | Stay on `main` — snapshot not required |
