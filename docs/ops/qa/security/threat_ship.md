---
id: threat-ship
type: reference
phase: [1, 6]
audience: [release, pm, architect]
status: active
authority: qa
tokens_est: 520
summary: "Threat model + ship build rule"
---
# Security — Threat model + ship build rule

**Hub:** [`SECURITY.md`](../SECURITY.md)

## 1. Threat model (practical)

| Threat | Impact | Primary control |
|--------|--------|-----------------|
| Dev MCP/GDAI in Steam build | License leak, attack surface, wrong binaries | **Export strip** + `L0_ship_build_security` |
| Secrets in git | API abuse, webhook spam, Steam/GitHub takeover | **`L0_no_secrets`** scan |
| Compromised Godot/tool download | Supply-chain malware | Pinned URLs + future checksums (`ship_security.json`) |
| Webhook / PAT leak | Unauthorized agent runs | Cursor Secrets, rotate on leak, least-privilege `GH_TOKEN` |
| Telemetry / reports with PII | Privacy | `DELIVERY_CONTROL.md` checklist |
| Windows tamper / SmartScreen | User trust | Code signing at M6 (manual) |
| Casual PCK unpack / script browse | Spoilers, trivial mods | **PCK encryption** (custom templates) + release export |
| Save-file editing (gold, flags) | Broken progression | **HMAC-signed saves** (`SaveIntegrity`) |
| Fake Steam achievements | Leaderboard/gallery abuse | **GodotSteam API** unlocks (server-side) |

---


## 2. Ship build rule (non-negotiable)

**Never ship** dev editor integrations:

| Remove on export | Why |
|------------------|-----|
| `GDAIMCPRuntime` autoload | GDAI MCP — commercial dev bridge |
| `GodotIQRuntime` + Godotiq plugin | Debug/analysis WebSocket |
| Godot MCP Pro autoloads + plugin | Test automation |
| `godot-mcp-plugin-godot` editor plugin | Scene mutation in dev only |

**Implementation:** `tools/godot_strip_dev_plugins.py` — called by:

- `tools/export_linux.sh` / `tools/export_windows.sh` via `export_strip_dev_plugins_begin`
- `tools/with_ci_godot.sh` (headless CI when addons absent)

**Verify:**

```bash
bash tools/check_ship_build_security.sh    # L0_ship_build_security
```

After export smokes, binaries are scanned for forbidden dev path strings.

---
