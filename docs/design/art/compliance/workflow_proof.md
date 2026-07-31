---
id: workflow-proof
type: reference
phase: [1, 5]
audience: [visual, builder, release]
status: active
authority: art
tokens_est: 545
summary: "Import workflow, proof tools, documentation"
---
# Asset Compliance — Import workflow, proof tools, documentation

**Hub:** [`ASSET_COMPLIANCE.md`](../ASSET_COMPLIANCE.md)

## When to read

Use **Asset Compliance — Import workflow, proof tools, documentation** (roles: visual, builder, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [4. Workflow — before importing any file](#4-workflow-before-importing-any-file)
- [5. Proof & verification tools](#5-proof-verification-tools)
- [Pre-release checklist](#pre-release-checklist)
- [6. What must be documented](#6-what-must-be-documented)


## 4. Workflow — before importing any file

```
1. Confirm license on the official source page (not a re-upload mirror)
2. Run:  python3 tools/register_asset.py add --help
3. Register the asset in docs/asset_manifest.license.json
4. Add a row to docs/design/art/LICENSES.md (human-readable log)
5. Run:  bash tools/check_asset_compliance.sh
6. Commit manifest + LICENSES.md together with the asset files
```

**Never commit an asset file without a manifest entry.**

---


## 5. Proof & verification tools

| Tool | Purpose |
|------|---------|
| `tools/verify_asset_licenses.py` | Fail CI if any media file lacks manifest entry or uses banned license |
| `tools/register_asset.py` | Add/update/remove manifest entries interactively |
| `tools/generate_compliance_report.py` | Generate `docs/archive/compliance/COMPLIANCE_REPORT.md` audit proof |
| `bash tools/check_asset_compliance.sh` | One command: verify + report |

### Pre-release checklist

```bash
# From repo root — must exit 0 before Steam upload
bash tools/check_asset_compliance.sh
```

Outputs:
- Console pass/fail
- `docs/archive/compliance/COMPLIANCE_REPORT.md` — timestamped proof for your records
- `docs/archive/compliance/COMPLIANCE_REPORT.json` — machine-readable audit

---


## 6. What must be documented

For **each** external asset:

| Field | Required |
|-------|----------|
| File path(s) | ✓ |
| License ID | ✓ |
| Source name | ✓ |
| Source URL | ✓ (official page) |
| Author | ✓ |
| Date added | ✓ |
| Used for | ✓ |
| Attribution text | If CC-BY / OFL / MIT |

---
