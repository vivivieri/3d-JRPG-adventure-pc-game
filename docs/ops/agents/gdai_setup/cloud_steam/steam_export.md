---
id: steam-export
type: how-to
phase: [0, 1]
audience: [pm, builder, release]
status: active
authority: ops
tokens_est: 197
summary: "1. **Disable** the GDAI MCP plugin in **Project → Project Settings → Plugins**."
---
# GDAI Setup — Cloud / Steam / Troubleshoot — Before Steam export

**Hub:** [`cloud_steam_troubleshoot.md`](../cloud_steam_troubleshoot.md)

## When to read

Use **GDAI Setup — Cloud / Steam / Troubleshoot — Before Steam export** (roles: pm, builder, release) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



## 5. Before Steam / release export

1. **Disable** the GDAI MCP plugin in **Project → Project Settings → Plugins**.
2. **Remove** `game/addons/gdai-mcp-plugin-godot/` from the export tree (it should not exist on release machines if you follow gitignore).
3. Run `./tools/export_windows.sh` as usual — only `godotsteam` should remain in `addons/`.

See also: `steam/GODOTSTEAM_SETUP.md`, `game/addons/godotsteam/README.md`.

---
