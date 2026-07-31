---
id: steam-supply
type: reference
phase: [1, 6]
audience: [release, pm, architect]
status: active
authority: qa
tokens_est: 265
summary: "Steam/CD + supply chain"
---
# Security — Steam/CD + supply chain

**Hub:** [`SECURITY.md`](../SECURITY.md)

## 6. Steam / CD

| Item | Control |
|------|---------|
| `STEAM_*` secrets | GitHub Environment `steam-production` + required reviewers |
| `cd-steam.yml` | Manual `workflow_dispatch` only |
| `steam_appid.txt` test id **480** | Replace before prod upload |
| GodotSteam | Ship path only — not dev MCP addons |

**M6 manual:** Windows Authenticode signing (not automated in v1).

---


## 7. Supply chain

Documented in `ship_security.json` → `supply_chain`:

- Godot **4.7-stable** editor + export templates from `github.com/godotengine/godot` releases only
- Install via `tools/install_ci_deps.sh`, `install_cloud_dev.sh`, `install_ci_deps_windows.sh`
- **Future:** set `pin_checksums: true` + SHA256 after audited download

Third-party MCP/commercial zips: vendor sites only (`PLUGIN_COMPATIBILITY.md`).

---
