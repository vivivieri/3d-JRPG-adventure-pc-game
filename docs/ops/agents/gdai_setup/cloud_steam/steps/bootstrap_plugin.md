---
id: bootstrap-plugin
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 640
summary: "Snapshot ID + launch checklist: `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` — active snapshot `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8`, boot veri"
---
# GDAI — Configure Cloud Agents — Bootstrap + GDAI plugin

**Hub:** [`cloud_agents.md`](../cloud_agents.md)

## When to read

Use **GDAI — Configure Cloud Agents — Bootstrap + GDAI plugin** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [4.1 Environment bootstrap (VM)](#41-environment-bootstrap-vm)
- [4.2 GDAI plugin in cloud (required — not in git)](#42-gdai-plugin-in-cloud-required-not-in-git)


### 4.1 Environment bootstrap (VM)

**Snapshot ID + launch checklist:** `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` — active snapshot `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8`, boot verification, and `main` vs `game/development` pitfalls.

Cloud agents install dependencies via `.cursor/environment.json`:

```bash
bash tools/install_cloud_dev.sh   # Godot 4.7, uv, export templates
bash tools/ensure_gdai_mcp.sh     # Editor + GDAI HTTP bridge — REQUIRED
bash tools/check_dev_environment.sh
```

**Installed by `install_cloud_dev.sh`:**

| Component | Location |
|-----------|----------|
| Godot 4.7 editor | `godot4` → `~/.local/bin` |
| Export templates | `.cache/godot-data/godot/export_templates/` |
| uv | `~/.local/bin/uv` |
| numpy | Python (trailer tool) |

**`ensure_gdai_mcp.sh` does:**

1. Writes `.cursor/mcp.json` for the `godot-mcp` stdio bridge
2. Starts Godot Editor if not running (`--rendering-driver opengl3`)
3. Waits for GDAI HTTP `http://127.0.0.1:3571/tools`
4. Exits non-zero with notify instructions if the bridge is not ready


### 4.2 GDAI plugin in cloud (required — not in git)

GDAI MCP is **commercial** and **gitignored**. Snapshots cloned from GitHub **do not** include it. Install it once, then **save a snapshot**.

**Option A — Rebuild snapshot (recommended)**

1. [cursor.com/agents](https://cursor.com/agents) → your environment → **Start Setup Agent**
2. Upload your purchase zip to the VM:
   ```
   game/addons/gdai-mcp-plugin-godot-YYYYMMDD.zip
   ```
3. Run in the setup terminal:
   ```bash
   bash tools/install_gdai_plugin.sh
   bash tools/ensure_gdai_mcp.sh
   curl -sf http://127.0.0.1:3571/tools | head -c 100
   ```
4. When setup succeeds, **save the snapshot**
5. Future agents boot with the plugin pre-installed

**Option B — Zip in snapshot folder**

If `game/addons/gdai-mcp-plugin-godot*.zip` exists, `install_cloud_dev.sh` auto-extracts on boot.

**Without the plugin:** `ensure_gdai_mcp.sh` fails, `.cursor/mcp.json` is not written, and `godot-mcp` MCP calls fail even if registered in the dashboard.
