---
id: credits-violations
type: reference
phase: [1, 5]
audience: [visual, builder, release]
status: active
authority: art
tokens_est: 335
summary: "Credits, cross-refs, violations"
---
# Asset Compliance — Credits, cross-refs, violations

**Hub:** [`ASSET_COMPLIANCE.md`](../ASSET_COMPLIANCE.md)

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

- Human log: `docs/design/art/LICENSES.md`
- Machine manifest: `docs/asset_manifest.license.json`
- Art sourcing: `docs/design/art/ART_DIRECTION.md` §6
- Character imports: `docs/design/art/CHARACTER_BIBLE.md` §10
- Environment imports: `docs/design/world/ENVIRONMENT_KITS.md` §11
- Audio imports: `docs/design/audio/AUDIO_DIRECTION.md` §6
- Risk register: `docs/design/vision/GDD.md` §16

---


## 9. Policy violations

If `verify_asset_licenses.py` fails:

1. **Remove** the unlisted file, or
2. **Register** it with correct license + update LICENSES.md, or
3. **Replace** with documented AI-generated, CC0, or repo procedural work

Do not ship until the checker passes with zero errors.
