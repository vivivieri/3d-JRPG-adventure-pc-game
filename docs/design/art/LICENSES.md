---
id: licenses
type: reference
phase: [1, 5]
audience: [visual, release, audio]
status: active
authority: art
tokens_est: 237
summary: "Third-party license log — load fonts, audio, or 3D models"
---
# Licenses

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`story_engine_fonts.md`](licenses/story_engine_fonts.md) | Story, engine, fonts |
| [`audio_models.md`](licenses/audio_models.md) | Audio + 3D models |
| [`art_code_ship.md`](licenses/art_code_ship.md) | Art, ship status, code, M6 checklist |
Track every third-party asset, story source, and engine dependency.

**Policy:** All shipped art and audio must be **copyright-safe for commercial release** — no unlicensed or all-rights-reserved material. See **`docs/design/art/ASSET_COMPLIANCE.md`** for the full allow/deny list.

**Machine manifest:** `docs/asset_manifest.license.json`
**Verify before ship:** `bash tools/check_asset_compliance.sh`

