---
id: ship-checklist
type: how-to
phase: [1, 6]
audience: [release, pm]
status: active
authority: qa
tokens_est: 315
summary: "Security — M6 Player Protect — M6 ship security checklist — - [ ] `bash tools/check_player_build_protection.sh` PASS (save HMAC spec + export hooks)"
---
# Security — M6 Player Protect — M6 ship security checklist

**Hub:** [`m6_player_protect.md`](../m6_player_protect.md)

## When to read

Use **Security — M6 Player Protect — M6 ship security checklist** (roles: release, pm) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



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
