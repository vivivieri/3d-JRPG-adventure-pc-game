# Security — Ship Build, Secrets & Supply Chain

**Version:** 1.0  
**Machine-readable:** `game/data/qa/ship_security.json`  
**Cross-refs:** `docs/PLATFORM_SUPPORT.md`, `docs/CURSOR_SECRETS_SETUP.md`, `docs/DELIVERY_CONTROL.md`, `docs/ASSET_COMPLIANCE.md`, `docs/PLUGIN_COMPATIBILITY.md`

Security for *Tides of Urashima* focuses on **not shipping the dev factory**, **not leaking secrets**, and **verifying release binaries** — not anti-cheat or online hardening (single-player JRPG).

---

## 1. Threat model (practical)

| Threat | Impact | Primary control |
|--------|--------|-----------------|
| Dev MCP/GDAI in Steam build | License leak, attack surface, wrong binaries | **Export strip** + `L0_ship_build_security` |
| Secrets in git | API abuse, webhook spam, Steam/GitHub takeover | **`L0_no_secrets`** scan |
| Compromised Godot/tool download | Supply-chain malware | Pinned URLs + future checksums (`ship_security.json`) |
| Webhook / PAT leak | Unauthorized agent runs | Cursor Secrets, rotate on leak, least-privilege `GH_TOKEN` |
| Telemetry / reports with PII | Privacy | `DELIVERY_CONTROL.md` checklist |
| Windows tamper / SmartScreen | User trust | Code signing at M6 (manual) |

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

## 3. Secrets policy

| Rule | Detail |
|------|--------|
| **Storage** | Cursor Secrets + GitHub Actions Secrets only |
| **Never commit** | PATs, webhooks, API keys, Steam passwords, Telegram tokens |
| **Never in PRs** | Gate reports, screenshots, `artifacts/` committed to git |
| **Least privilege** | `GH_TOKEN` — issues/PRs/workflows scope; not admin unless `setup_github_project.sh` |
| **Rotate** | Webhook URLs and PATs on any leak suspicion |

**Scan:**

```bash
bash tools/check_no_secrets.sh           # L0_no_secrets
```

Patterns and allowlist: `game/data/qa/ship_security.json` → `secret_scan`.

---

## 4. CI gates

| Gate ID | Command | Branch |
|---------|---------|--------|
| `L0_no_secrets` | `bash tools/check_no_secrets.sh` | `main` + `game/development` |
| `L0_ship_build_security` | `bash tools/check_ship_build_security.sh` | `main` + `game/development` |

Export smokes (`L2_linux_export_smoke`, `L2_windows_export_run`) re-run ship security after building binaries.

---

## 5. Cloud agent factory

| Risk | Mitigation |
|------|------------|
| Agent posts secret in issue/PR | Agent rules + `L0_no_secrets` |
| JIT VM without snapshot | No scene work; no perf sign-off (`PLATFORM_SUPPORT.md`) |
| Webhook abuse | Separate PM vs alert URLs; do not log full URLs |
| Commercial addons in repo | **Gitignored** — snapshot only; stripped before ship |

---

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

## 8. M6 ship security checklist

- [ ] `bash tools/check_no_secrets.sh` PASS on RC tag
- [ ] `bash tools/check_ship_build_security.sh` PASS after export
- [ ] `L2_linux_export_smoke` + `L2_windows_export_run` green on RC commit
- [ ] No dev plugin strings in `build/TidesOfUrashima.*`
- [ ] Steam secrets in protected environment only
- [ ] Windows binary signed (or documented exception for beta)
- [ ] `LICENSES.md` + credits screen match shipped assets

---

## 9. Related docs

| Doc | Topic |
|-----|-------|
| `docs/CURSOR_SECRETS_SETUP.md` | How to obtain and store keys |
| `docs/DELIVERY_CONTROL.md` | Outbound report approval |
| `docs/PLATFORM_SUPPORT.md` | Linux + Windows ship parity |
| `docs/STEAM_RELEASE_CHECKLIST.md` | M6 technical rows |
| `docs/ASSET_COMPLIANCE.md` | Copyright-safe assets |
