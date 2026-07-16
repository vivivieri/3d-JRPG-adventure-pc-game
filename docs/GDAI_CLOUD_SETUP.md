# GDAI MCP — local & cloud dev setup

**GDAI MCP** is a **dev-only** Godot 4 plugin that lets Cursor (and other MCP clients) control the **Godot Editor** — create scenes, move nodes, read script errors, etc.

> **Full MCP stack:** This project also supports **Godotiq** (analyze/debug) and **Godot MCP Pro** (automated testing). See **`docs/MCP_STACK.md`** for roles, install, and conflict rules.  
> **Plugin install steps:** `docs/PLUGIN_INSTALL_GUIDE.md`

Official docs: https://gdaimcp.com/docs/installation  
Cursor MCP docs: https://cursor.com/help/customization/mcp

This repo does **not** commit the plugin. It is gitignored so Steam/release builds stay clean. Only **GodotSteam** ships under `game/addons/`.

---

## Architecture (two layers — both required)

GDAI is **not** a single server. Cursor talks to a stdio bridge, which talks to the Godot editor plugin:

```
Cursor Agent  →  godot-mcp (stdio via uv)  →  gdai_mcp_server.py
                                                    ↓ HTTP
                                            Godot Editor plugin (:3571)
```

| Layer | What | How to start |
|-------|------|----------------|
| **Godot side** | Editor plugin HTTP API | Godot open → **GDAI MCP** panel → **Start** |
| **Cursor side** | stdio MCP bridge | Cursor spawns `uv run …/gdai_mcp_server.py` |

**Important:** GDAI controls the **editor**, not headless Godot. Headless smoke tests (`tools/run_playtest_smoke.sh`) validate logic **after** GDAI editor verification — they do not replace GDAI.

**Startup order:** Godot editor open → GDAI MCP **Started** → Cursor `godot-mcp` connected → then chat with the agent.

---

## What you need (3 pieces)

| Piece | Purpose |
|-------|---------|
| **Godot Editor** | Project open at `game/project.godot`, plugin enabled, MCP server **Started** |
| **`gdai_mcp_server.py`** | Stdio bridge run via `uv` (inside the plugin folder) |
| **Cursor MCP config** | Points Cursor at that Python server (method differs for desktop vs cloud — see §3–§4) |

---

## 1. Prerequisites

### `uv` (required by GDAI)

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.sh | iex"
```

### Godot 4.7 stable

Open `game/project.godot` in Godot **4.7** (Forward+). Cloud: `bash tools/install_cloud_dev.sh`. See `docs/TECH_STACK.md`.

---

## 2. Install the plugin (local, dev only)

1. Purchase/download from https://gdaimcp.com/ (commercial plugin).
2. Extract the zip — you get `addons/gdai-mcp-plugin-godot/`.
3. Copy that folder to:

   ```
   game/addons/gdai-mcp-plugin-godot/
   ```

4. In Godot: **Project → Project Settings → Plugins** → enable **GDAI MCP**.
5. Open the **GDAI MCP** tab in the bottom panel → **Start** the MCP server.
6. Copy the JSON config shown in that panel.

### Recommended editor settings

**Editor → Editor Settings** (enable **Advanced Settings**):

- Auto Reload Scripts on External Change — **On**
- Auto Reload and Parse Scripts on Save — **On**

### Path without spaces

GDAI can fail if the project or `gdai_mcp_server.py` path contains spaces. Prefer a short path, e.g. `~/dev/3d-JRPG-adventure-pc-game`.

---

## 3. Configure Cursor — Desktop (local IDE)

Use this when running Cursor on your machine with a local Godot editor.

### 3.1 Get the JSON from Godot (authoritative)

1. Open **GDAI MCP** tab in the Godot bottom panel.
2. Click **Start** the MCP server.
3. **Copy the JSON config** shown in that panel (paths match your machine).

### 3.2 Register in Cursor

**Method A — UI (recommended):**

1. Open **Cursor Settings** (`Ctrl+Shift+J` / `Cmd+Shift+J`).
2. Go to **Tools & MCP**.
3. Click **Add new global MCP server** (or edit project config).
4. Paste the JSON from the GDAI MCP panel.

**Method B — project file (team-shared):**

Create or edit `.cursor/mcp.json` in the project root:

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": [
        "run",
        "/absolute/path/to/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
      ]
    }
  }
}
```

Replace the path with your machine’s absolute path (or use the path from the GDAI panel).  
Template: `.cursor/mcp.json.example`

### 3.3 Verify (desktop)

1. Restart Cursor.
2. **Settings → Tools & MCP** — `godot-mcp` shows **connected** (green).
3. Godot editor is open with this project.
4. In chat, Agent should list GDAI tools (scene tree, run scene, etc.).

---

## 4. Configure Cursor — Cloud Agents

Cloud agents run in a remote VM. You need **both** VM bootstrap **and** Cursor dashboard MCP registration.

> **Latest Cursor guidance (2026):** Cloud Agents support MCP servers configured in the **Cloud Agents dashboard** ([cursor.com/agents](https://cursor.com/agents)). Team plans: **Dashboard → Integrations & MCP**.  
> A workspace `.cursor/mcp.json` helps the VM but **does not by itself** expose `godot-mcp` tools to the agent — you must register the server in the dashboard and restart the agent.

### 4.1 Environment bootstrap (VM)

**Snapshot ID + launch checklist:** `docs/CLOUD_SNAPSHOT_LAUNCH.md` — active snapshot `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8`, boot verification, and `main` vs `game/development` pitfalls.

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

### 4.3 Register MCP in Cursor dashboard (required for agent tools)

1. Open your cloud environment dashboard, e.g.  
   [cursor.com/dashboard/cloud-agents/environments](https://cursor.com/dashboard/cloud-agents/environments)  
   → select this repo’s environment.
2. Or go to [cursor.com/agents](https://cursor.com/agents) → MCP / integrations.
3. **Add custom MCP server** named `godot-mcp`:

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": ["run", "/workspace/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"]
    }
  }
}
```

Use `/workspace/...` for this cloud VM path, or the path shown in the Godot GDAI MCP panel for your environment.

4. **Restart the cloud agent** after saving.
5. Confirm the agent’s MCP catalog lists **`godot-mcp`** (not only Figma/Linear/Notion).

**Cloud MCP note:** `${env:VAR}` interpolation in dashboard MCP config often **fails** on cloud agents — paste literal secret values if your server needs `env` blocks.

### 4.4 Verify (cloud)

Run inside the agent VM:

```bash
bash tools/ensure_gdai_mcp.sh
curl -sf http://127.0.0.1:3571/tools | head -c 200   # should return JSON with mcp_tools
pgrep -af 'godot4.*--editor'                          # editor running
```

In the agent session, MCP catalog must include **`godot-mcp`**.  
**Agents must not implement editor/scene work until both checks pass.**

### 4.5 Workflow (mandatory — no manual fallback)

See `.cursorrules` §0 and **`AGENTS.md`**.

| Work | Tool |
|------|------|
| GDScript, shaders, architecture | **GodotPrompter** (Cursor) |
| Scenes, nodes, materials, F5 verify | **GDAI MCP** only |
| Procedural BGM/SFX (copyright-safe) | `python3 tools/generate_game_audio.py` |
| Procedural portrait placeholders | `python3 tools/generate_procedural_portraits.py` |
| Logic/data smoke (after GDAI verify) | `bash tools/run_playtest_smoke.sh` |
| JRPG UI/combat playtest via live editor | GDAI MCP — see `docs/AI_TESTING_SPEC.md` §11 |
| Steam build | **No GDAI** in `game/addons/` |

---

## 5. Before Steam / release export

1. **Disable** the GDAI MCP plugin in **Project → Project Settings → Plugins**.
2. **Remove** `game/addons/gdai-mcp-plugin-godot/` from the export tree (it should not exist on release machines if you follow gitignore).
3. Run `./tools/export_windows.sh` as usual — only `godotsteam` should remain in `addons/`.

See also: `steam/GODOTSTEAM_SETUP.md`, `game/addons/godotsteam/README.md`.

---

## 6. Troubleshooting

| Symptom | Desktop fix | Cloud fix |
|---------|-------------|-------------|
| No GDAI tools in Agent | Godot open → GDAI **Start** → restart Cursor | Run `ensure_gdai_mcp.sh` → register `godot-mcp` in [cursor.com/agents](https://cursor.com/agents) dashboard → restart agent |
| HTTP bridge down | GDAI MCP panel → **Start** | `bash tools/ensure_gdai_mcp.sh` |
| `godot-mcp` missing from MCP catalog | **Settings → Tools & MCP** → add server | **Cloud dashboard** → add custom MCP (`.cursor/mcp.json` alone is not enough) |
| Server won’t start | Path has **no spaces**; `uv --version` | Same + plugin folder present in VM |
| Tools listed but calls fail | Project open in **Editor**, not headless | Kill headless Godot; keep `--editor` process running |
| Port 3572 in use | Stop headless Godot tests | `ensure_gdai_mcp.sh` kills conflicting headless processes |
| macOS dylib warning | See GDAI docs | N/A (cloud uses Linux) |

**Quick health checks:**

```bash
bash tools/ensure_gdai_mcp.sh
curl -sf http://127.0.0.1:3571/tools | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('mcp_tools',[])), 'tools')"
```

GDAI common issues: https://gdaimcp.com/docs/common-issues

---

## 7. This repo’s shipped addons

| Addon | Shipped? | Path |
|-------|----------|------|
| GodotSteam | Yes | `game/addons/godotsteam/` |
| GDAI MCP | **No (dev only)** | `game/addons/gdai-mcp-plugin-godot/` (gitignored) |

Environment visuals: GodotPrompter drafts `zone_visuals.gd` / shaders; **GDAI MCP** applies lights, materials, and meshes in the editor.
