# Alignment audit stakeholder visuals

PNG assets referenced by `game/data/qa/alignment_audit_catalog.json` visual packs.

## Usage

1. Run alignment audit (auto-generates `audit_radar_spec.png` + `audit_radar_build.png` from live scores):

```bash
bash tools/run_alignment_audit.sh --visuals-from docs/compliance/alignment_audit_visuals
```

Or regenerate radars only from the latest report:

```bash
python3 tools/generate_audit_radar_images.py --report artifacts/alignment_audits/latest.json
```

2. Copy other review / agent-generated PNGs into this directory using the filenames in the catalog.
3. Open `artifacts/alignment_dashboard.html` for the stakeholder gallery.

## Auto-generated (each audit)

| File | Source |
|------|--------|
| `audit_radar_spec.png` | Live spec stream domain scores |
| `audit_radar_build.png` | Build stream radar or N/A card on `main` |

**Do not use** legacy merged radars (`audit_radar_6axis.png`, mega dashboard) for management status — they are static art from an earlier phase.

## Packs (6 batches, 33 assets)

| Batch | Prefix / files |
|-------|----------------|
| 1 Foundation | `concept_ruined_village.png`, `audit_radar_spec.png`, `audit_radar_build.png`, `audit_radar_6axis.png` (legacy), `roadmap_6phase.png` |
| 2 Zones | `tides_concept_beach_shore.png`, `tides_concept_palace_gate.png`, … |
| 3 Endings | `tides_concept_tidal_caves.png`, `tides_concept_three_endings.png`, … |
| 4 Combat/audio | `tides_combat_*.png`, `tides_audit_combat_*.png`, … |
| 5 QA flow | `tides_visualqa_*.png`, `tides_audit_visual_qa.png`, … |
| 6 Steam | `tides_steam_*.png`, `tides_mega_dashboard_all_radars.png` |

Full manifest: `game/data/qa/alignment_audit_catalog.json` → `visual_packs`.

**Note:** Images are optional for CI. Missing files show as placeholders in the HTML dashboard until bundled.
