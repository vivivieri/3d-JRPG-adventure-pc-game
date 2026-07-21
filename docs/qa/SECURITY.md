# Security — Ship Build, Secrets & Supply Chain

**Version:** 1.1
**Machine-readable:** `game/data/qa/ship_security.json`
**Cross-refs:** `docs/qa/PLATFORM_SUPPORT.md`, `docs/agents/CURSOR_SECRETS_SETUP.md`, `docs/workflow/DELIVERY_CONTROL.md`, `docs/art/ASSET_COMPLIANCE.md`, `docs/technical/PLUGIN_COMPATIBILITY.md`

Security for *Tides of Urashima* focuses on **not shipping the dev factory**, **not leaking secrets**, **verifying release binaries**, and **raising the bar against casual ripping/tampering** — not kernel anti-cheat (offline single-player JRPG).

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
| `L0_player_build_protection` | `bash tools/check_player_build_protection.sh` | `main` + `game/development` |

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

- [ ] `bash tools/check_player_build_protection.sh` PASS (save HMAC spec + export hooks)
- [ ] `SHIP_RELEASE=1` RC build: `GODOT_SCRIPT_ENCRYPTION_KEY` + custom encrypted templates + `GODOT_SAVE_HMAC_KEY`
- [ ] PCK encrypted on RC (`encrypt_pck=true` in export preset during ship export)
- [ ] Save slots written with `_integrity` HMAC (`SaveSystem` → `SaveIntegrity`)
- [ ] Steam DRM policy: **none** (documented in `ship_security.json`) — achievements via Steam API only
- [ ] `bash tools/check_no_secrets.sh` PASS on RC tag
- [ ] `bash tools/check_ship_build_security.sh` PASS after export
- [ ] `L2_linux_export_smoke` + `L2_windows_export_run` green on RC commit
- [ ] No dev plugin strings in `build/TidesOfUrashima.*`
- [ ] Steam secrets in protected environment only
- [ ] Windows binary signed (or documented exception for beta)
- [ ] `LICENSES.md` + credits screen match shipped assets

---

## 9. Player build protection (anti-rip / anti-tamper)

**Machine-readable:** `game/data/qa/ship_security.json` → `player_build_protection`, `game/data/qa/save_integrity.json`

**Honest goal:** A Steam download can **never** be made undecodable — the player has the binary. We **raise effort** for casual rippers and Notepad save editors, and keep **API keys out of the client**.

### 9.1 What we do not ship

| Never in player build | Why |
|-----------------------|-----|
| GDAI / Godotiq / MCP Pro | Dev factory (`§2`) |
| OpenAI / ElevenLabs / webhook keys | Abuse if extracted (`§3`) |
| Plain dev pepper for saves | Use `GODOT_SAVE_HMAC_KEY` at RC export only |

### 9.2 Release export (always)

- Export with `--export-release` (already in `export_linux.sh` / `export_windows.sh`).
- Windows: prefer **embed PCK** in `.exe` (hides loose `.pck` file; not encryption).
- Strip dev plugins before every export (`export_strip_dev_plugins_begin`).

### 9.3 PCK encryption (M6 RC — custom templates required)

Godot **official** export templates **cannot** read encrypted PCK at runtime. Encrypted ship builds need templates compiled with the same AES key:

1. Generate keys: `bash tools/generate_ship_protection_keys.sh`
2. Store in GitHub Environment `steam-production`: `GODOT_SCRIPT_ENCRYPTION_KEY`, `GODOT_SAVE_HMAC_KEY`
3. Build templates (once per key rotation):

```bash
export SCRIPT_AES256_ENCRYPTION_KEY="$GODOT_SCRIPT_ENCRYPTION_KEY"
bash tools/build_godot_export_templates_encrypted.sh
export GODOT_CUSTOM_TEMPLATE_LINUX="build/godot-templates/linux_encrypted.template_release.x86_64"
# Windows: set GODOT_CUSTOM_TEMPLATE_WINDOWS after building win template
```

4. RC export:

```bash
export SHIP_RELEASE=1
export GODOT_SCRIPT_ENCRYPTION_KEY="…"
export GODOT_SAVE_HMAC_KEY="…"
bash tools/export_linux.sh
```

`export_ship_protection_begin` enables `encrypt_pck`, writes `game/.godot/export_credentials.cfg` (gitignored), injects save pepper into `project.godot` for the export only, then restores on exit.

**Reality:** Determined reversers can still extract assets with enough effort. This blocks casual `godot-pck-extractor` browsing.

### 9.4 Save integrity (HMAC)

| Item | Detail |
|------|--------|
| Spec | `game/data/qa/save_integrity.json` |
| GDScript | `game/scripts/core/save_integrity.gd` — wire from `SaveSystem.write_slot` / `read_slot` |
| Field | `_integrity` on `user://save_slot_0.json` |
| Pepper | `application/config/save_hmac_pepper` injected at ship export from `GODOT_SAVE_HMAC_KEY` |
| On corrupt/tamper | Reject load — message + New Game only (`SAVE_AND_FAIL_STATES.md` §4) |

Validate spec locally:

```bash
python3 tools/validate_save_integrity_spec.py
```

**Reality:** Pepper lives in the binary — deters Notepad edits, not a determined reverser.

### 9.5 Steam achievements (server-side)

Register achievements in Steamworks; unlock only via **GodotSteam** API when story flags fire (`ACHIEVEMENTS.md`). Editing local saves must **not** unlock Steam achievements.

### 9.6 Steam DRM — policy: **none**

| Option | v1 decision |
|--------|-------------|
| Steam DRM wrapper | **No** — Proton/Linux compatibility, fewer AV false positives |
| Steam as distributor | **Yes** — purchase tied to Steam account |
| Code signing (Windows) | **Yes** at M6 — user trust, not anti-rip |

Documented in `ship_security.json` → `steam_drm.policy: none`.

### 9.7 CI gate

```bash
bash tools/check_player_build_protection.sh    # L0_player_build_protection
```

When `SHIP_RELEASE=1`, the gate also requires encryption keys and custom template paths.

---

## 11. Related docs

| Doc | Topic |
|-----|-------|
| `docs/agents/CURSOR_SECRETS_SETUP.md` | How to obtain and store keys |
| `docs/workflow/DELIVERY_CONTROL.md` | Outbound report approval |
| `docs/qa/PLATFORM_SUPPORT.md` | Linux + Windows ship parity |
| `docs/ci-cd/STEAM_RELEASE_CHECKLIST.md` | M6 technical rows |
| `docs/art/ASSET_COMPLIANCE.md` | Copyright-safe assets |
