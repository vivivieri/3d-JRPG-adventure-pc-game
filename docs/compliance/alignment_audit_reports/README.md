# Alignment audit reports (committed history)

Timestamped alignment audit snapshots for GitHub — **recommendation checklist**, **domain scores**, and **visual manifest** per run.

## Layout

```
docs/compliance/alignment_audit_reports/
  <audit_id>/                 # e.g. 20260717T101849Z_manual
    report.json               # full audit payload
    report.md                   # human-readable (images embedded when present)
    dashboard.html              # stakeholder dashboard
    recommendations.json        # checklist + recommendations only (easy diff)
    visuals/                    # optional PNG snapshot (--archive-visual-snapshots)
```

Index: `docs/compliance/alignment_audit_history.json`

## Run and save

```bash
bash tools/run_alignment_audit.sh \
  --trigger post_merge \
  --note "PR #92 checklist clear" \
  --visuals-from docs/compliance/alignment_audit_visuals
```

Commit the new `<audit_id>/` folder and `alignment_audit_history.json` to `main`.

Optional full PNG copy per audit (large — ~70MB):

```bash
bash tools/run_alignment_audit.sh --archive-visual-snapshots --visuals-from docs/compliance/alignment_audit_visuals
```

Default: `report.json` records which visuals were present; `report.md` links to `../../alignment_audit_visuals/`.

Authority: `docs/qa/ALIGNMENT_AUDIT.md`
