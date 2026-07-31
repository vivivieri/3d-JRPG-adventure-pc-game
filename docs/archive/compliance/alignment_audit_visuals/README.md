# Alignment audit stakeholder visuals

PNG assets referenced by `game/data/qa/alignment_audit_catalog.json` visual packs.

## Layout (v1.5+)

```
alignment_audit_visuals/
  latest/     # current management status set (auto-generated / illustrated locked)
  style/      # tides_* style kit + concept/roadmap packs (rarely change)
  README.md
```

| Folder | Purpose | Updated |
|--------|---------|---------|
| `latest/` | Live stakeholder slides (`audit_exec_summary.png`, stream radars, …) | Every audit / art regen |
| `style/` | Illustrated style refs (`tides_*`, `audit_radar_6axis.png`, concepts) | Rarely |

**Per-run versioned copies** (Git LFS):  
`docs/archive/compliance/alignment_audit_reports/<audit_id>/visuals/`

## Usage

```bash
bash tools/run_alignment_audit.sh \
  --visuals-from docs/archive/compliance/alignment_audit_visuals/latest
```

Or regenerate matplotlib fallbacks only (skips illustrated locks unless `--force`):

```bash
python3 tools/generate_audit_radar_images.py \
  --report artifacts/alignment_audits/latest.json \
  --output-dir docs/archive/compliance/alignment_audit_visuals/latest
```

## Style

Match `style/tides_audit_radar_updated.png` — navy parchment, gold frame, teal radar.  
See `docs/ops/qa/alignment/visuals/stakeholder_visuals.md`.

Full manifest: `game/data/qa/alignment_audit_catalog.json` → `visual_packs`.
