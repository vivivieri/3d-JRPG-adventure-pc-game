---
id: plugin-compatibility
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder, pm]
status: active
authority: engineering
tokens_est: 217
summary: "Godot 4.7 plugin matrix — load engine, GDAI, or ship plugins"
---
# Plugin Compatibility

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`summary_engine_gdai.md`](plugin_compat/summary_engine_gdai.md) | Summary, engine, GDAI |
| [`godotiq_mcp_pro.md`](plugin_compat/godotiq_mcp_pro.md) | Godotiq + MCP Pro |
| [`steam_enable_check.md`](plugin_compat/steam_enable_check.md) | Steam, enablement, check, fail, related |
**Engine pin:** `GODOT_VERSION=4.7-stable` (`tools/install_cloud_dev.sh`)
**Audit date:** July 2026
**Check script:** `bash tools/check_plugin_compatibility.sh [--with-editor]`

Run this audit **before Phase 1 build** and after any engine or plugin upgrade.

---

