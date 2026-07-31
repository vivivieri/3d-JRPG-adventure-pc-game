---
id: architecture-needs
type: how-to
phase: [0, 1]
audience: [builder, pm, architect]
status: active
authority: ops
tokens_est: 508
summary: "Architecture + needs + prereqs"
---
# GDAI Cloud Setup — Architecture + needs + prereqs

**Hub:** [`GDAI_CLOUD_SETUP.md`](../GDAI_CLOUD_SETUP.md)

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

Open `game/project.godot` in Godot **4.7** (Forward+). Cloud: `bash tools/install_cloud_dev.sh`. See `docs/engineering/technical/TECH_STACK.md`.

---
