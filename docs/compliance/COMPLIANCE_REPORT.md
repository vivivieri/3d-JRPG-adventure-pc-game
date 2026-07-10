# Asset Compliance Report

**Generated:** 2026-07-10 07:00:49 UTC  
**Status:** PASSED  
**Policy:** [docs/ASSET_COMPLIANCE.md](../ASSET_COMPLIANCE.md)  
**Manifest:** `docs/asset_manifest.license.json`

## Verification output

```
ASSET LICENSE CHECK PASSED
  Policy: docs/ASSET_COMPLIANCE.md
  Manifest: docs/asset_manifest.license.json
  Media files scanned: 0
  Covered by manifest: 0
  Allowed license types: 12
  Warnings: 7 (paths not present on this branch)
    - Scan path not present (no media to check): game/assets
    - Manifest entry file not on disk yet: game/assets/fonts/NotoSans-Regular.ttf
    - Manifest entry file not on disk yet: game/assets/fonts/NotoSans-Bold.ttf
    - Manifest entry file not on disk yet: game/assets/fonts/NotoSansJP-Regular.otf
    - Manifest entry file not on disk yet: game/assets/fonts/NotoSansJP-Bold.otf
    - Manifest entry file not on disk yet: game/assets/fonts/NotoSansSC-Regular.otf
    - Manifest entry file not on disk yet: game/assets/fonts/NotoSansSC-Bold.otf
```

## Statistics

| Metric | Value |
|--------|-------|
| Media files on disk | 0 |
| Unlisted files | 0 |
| Manifest entries | 13 |

### Files by license

_No media files on disk (docs-only branch or pre-asset phase)._

## Allowed license types

`APACHE-2.0`, `BSD-2-CLAUSE`, `BSD-3-CLAUSE`, `CC-BY-3.0`, `CC-BY-4.0`, `CC0-1.0`, `COMMISSIONED`, `MIT`, `MIXAMO-TOS`, `OFL-1.1`, `ORIGINAL`, `PUBLIC-DOMAIN`

## Banned license types

`ALL-RIGHTS-RESERVED`, `ASSET-STORE-DEFAULT`, `CC-BY-NC`, `CC-BY-NC-ND`, `CC-BY-NC-SA`, `CC-BY-SA`, `EDITORIAL-ONLY`, `UNKNOWN`

## Credits draft

Run `python3 tools/generate_compliance_report.py --credits` for in-game credits text.

---

*This report is generated proof of an automated license audit. Re-run before each Steam upload.*
