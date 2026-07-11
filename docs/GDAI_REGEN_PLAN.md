# GDAI MCP regeneration plan — ARCHIVED

> **⛔ DO NOT USE THIS DOCUMENT FOR BUILDING.**  
> **Superseded by:** [`docs/IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) on branch **`main`**.  
> **Workflow:** GodotPrompter + full MCP stack — see [`.cursorrules`](../.cursorrules) §0 and [`docs/MCP_STACK.md`](MCP_STACK.md).  
> **Engine:** Godot **4.7** stable (not 4.3).  
> Old branches (`cursor/gdai-regen-dc91`, `cursor/game-implementation-01be`) are deleted.

---

The content below is kept for historical reference only.

---

# GDAI MCP regeneration plan (archived snapshot)

**Branch:** `cursor/gdai-regen-dc91` *(deleted)*  
**Design source:** `main` — `docs/GDD.md`, `docs/STORYBOARD.md`, `docs/ART_DIRECTION.md`  
**Tooling:** ~~GDAI MCP only~~ — **obsolete**; current policy requires GodotPrompter + GDAI + Godotiq + MCP Pro + GameLab + Notion.

---

## Setup (once per machine) — OUTDATED

1. Install `uv` — see `docs/GDAI_CLOUD_SETUP.md`
2. Copy commercial plugin → `game/addons/gdai-mcp-plugin-godot/` (gitignored)
3. Open `game/project.godot` in Godot **4.7**
4. Enable **GDAI MCP** plugin → **Start** server
5. Configure Cursor MCP (`~/.cursor/mcp.json` from `.cursor/mcp.json.example`)
6. Run `bash tools/ensure_mcp_stack.sh` before every agent session

---

*Remaining archived sections unchanged below — ignore phase names and scene paths; use `IMPLEMENTATION_PLAN.md` instead.*
