# Asset Compliance Policy — No Copyright Violations

**Project:** Tides of Urashima  
**Applies to:** All art, audio, fonts, 3D models, textures, plugins, and marketing media shipped with the game or on Steam.

---

## 1. Golden rule

> **Every file used in the shipped game must be copyright-safe for commercial PC release.**

That means you must have a **documented permissive license** or **documented AI service ToS** that allows commercial use and redistribution. Production is **fully automated** — no human artist commission path (`docs/ART_AUTOMATION_PIPELINE.md`).

**If you cannot prove the license, do not import the file.**

---

## 2. Allowed licenses (ship-safe)

| License | Commercial OK | Redistribution OK | Attribution | Notes |
|---------|---------------|-------------------|-------------|-------|
| **Public Domain** | ✓ | ✓ | No | Folklore, expired works |
| **CC0 1.0** | ✓ | ✓ | Appreciated | Poly Haven, Kenney |
| **MIT** | ✓ | ✓ | Yes | Godot, repo code, procedural tools |
| **Apache 2.0** | ✓ | ✓ | Yes | Some plugins |
| **BSD 2/3-Clause** | ✓ | ✓ | Yes | |
| **SIL OFL 1.1** | ✓ | ✓ | Yes | Noto fonts — no sold-by-itself |
| **CC-BY 4.0** | ✓ | ✓ | **Required** | Log author + credit screen |
| **AI-generated (documented ToS)** | ✓ | ✓ | Per service | Meshy, GameLab, ACE-Step, ElevenLabs — register in `LICENSES.md` |
| **Original / repo procedural** | ✓ | ✓ | Optional | `tools/generate_*` scripts |

---

## 3. Banned / not allowed without legal review

| Category | Examples | Why |
|----------|----------|-----|
| **All Rights Reserved** | Random Google images, Pinterest, ArtStation downloads | No redistribution right |
| **CC-BY-NC** | Many Freesound / OGA tracks | Non-commercial only |
| **CC-BY-NC-SA** | Sketchfab NC models | NC + SA |
| **CC-BY-SA** | Wikipedia SA photos | Share-alike infects project |
| **Editorial only** | Stock photo editorial licenses | Not for games |
| **Unity/Unreal Asset Store default** | Unless license explicitly allows standalone game | Usually restricted |
| **Anime / franchise IP** | Ghibli style traces, named characters | Trademark/copyright |
| **Mixamo** | ✓ Allowed with [Adobe terms](https://www.adobe.com/legal/terms.html) | Must comply with ToS; document in manifest |
| **AI-generated from copyrighted datasets** | Unclear training data | Avoid for ship without legal sign-off |

**When in doubt, reject the asset.**

---

## 4. Workflow — before importing any file

```
1. Confirm license on the official source page (not a re-upload mirror)
2. Run:  python3 tools/register_asset.py add --help
3. Register the asset in docs/asset_manifest.license.json
4. Add a row to docs/LICENSES.md (human-readable log)
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
| `tools/generate_compliance_report.py` | Generate `docs/compliance/COMPLIANCE_REPORT.md` audit proof |
| `bash tools/check_asset_compliance.sh` | One command: verify + report |

### Pre-release checklist

```bash
# From repo root — must exit 0 before Steam upload
bash tools/check_asset_compliance.sh
```

Outputs:
- Console pass/fail
- `docs/compliance/COMPLIANCE_REPORT.md` — timestamped proof for your records
- `docs/compliance/COMPLIANCE_REPORT.json` — machine-readable audit

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

## 7. Credits screen (ship requirement)

The in-game credits must list:

- Godot Engine (MIT)
- GodotSteam (MIT)
- Noto fonts (OFL)
- Every **CC-BY** asset (author + link)
- Optional appreciation for CC0 sources (Kenney, Poly Haven)

Generate draft text:

```bash
python3 tools/generate_compliance_report.py --credits
```

---

## 8. Cross-references

- Human log: `docs/LICENSES.md`
- Machine manifest: `docs/asset_manifest.license.json`
- Art sourcing: `docs/ART_DIRECTION.md` §6
- Character imports: `docs/CHARACTER_BIBLE.md` §10
- Environment imports: `docs/ENVIRONMENT_KITS.md` §11
- Audio imports: `docs/AUDIO_DIRECTION.md` §6
- Risk register: `docs/GDD.md` §16

---

## 9. Policy violations

If `verify_asset_licenses.py` fails:

1. **Remove** the unlisted file, or
2. **Register** it with correct license + update LICENSES.md, or
3. **Replace** with documented AI-generated, CC0, or repo procedural work

Do not ship until the checker passes with zero errors.
