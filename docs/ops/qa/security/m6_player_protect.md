---
id: m6-player-protect
type: reference
phase: [1, 6]
audience: [release, pm, architect]
status: active
authority: qa
tokens_est: 1302
summary: "M6 checklist, anti-tamper, related"
---
# Security — M6 checklist, anti-tamper, related

**Hub:** [`SECURITY.md`](../SECURITY.md)

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
| `docs/ops/agents/CURSOR_SECRETS_SETUP.md` | How to obtain and store keys |
| `docs/ops/workflow/DELIVERY_CONTROL.md` | Outbound report approval |
| `docs/ops/qa/PLATFORM_SUPPORT.md` | Linux + Windows ship parity |
| `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` | M6 technical rows |
| `docs/design/art/ASSET_COMPLIANCE.md` | Copyright-safe assets |
