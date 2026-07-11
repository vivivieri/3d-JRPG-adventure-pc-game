# Asset Compliance Report

**Generated:** 2026-07-11 21:07:40 UTC  
**Status:** PASSED  
**Policy:** [docs/ASSET_COMPLIANCE.md](../ASSET_COMPLIANCE.md)  
**Manifest:** `docs/asset_manifest.license.json`

## Verification output

```
ASSET LICENSE CHECK PASSED
  Policy: docs/ASSET_COMPLIANCE.md
  Manifest: docs/asset_manifest.license.json
  Media files scanned: 33
  Covered by manifest: 33
  Allowed license types: 12
  Warnings: 6 (paths not present on this branch)
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
| Media files on disk | 33 |
| Unlisted files | 0 |
| Manifest entries | 46 |

### Files by license

| License | File count |
|---------|------------|
| ORIGINAL | 33 |

## Allowed license types

`APACHE-2.0`, `BSD-2-CLAUSE`, `BSD-3-CLAUSE`, `CC-BY-3.0`, `CC-BY-4.0`, `CC0-1.0`, `COMMISSIONED`, `MIT`, `MIXAMO-TOS`, `OFL-1.1`, `ORIGINAL`, `PUBLIC-DOMAIN`

## Banned license types

`ALL-RIGHTS-RESERVED`, `ASSET-STORE-DEFAULT`, `CC-BY-NC`, `CC-BY-NC-ND`, `CC-BY-NC-SA`, `CC-BY-SA`, `EDITORIAL-ONLY`, `UNKNOWN`

## Credits draft

Run `python3 tools/generate_compliance_report.py --credits` for in-game credits text.

---

*This report is generated proof of an automated license audit. Re-run before each Steam upload.*
