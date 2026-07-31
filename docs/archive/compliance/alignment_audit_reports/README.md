# Alignment audit reports (committed history)

Timestamped alignment audit snapshots for GitHub — **recommendation checklist**, **domain scores**, and **visual snapshots** per run.

## Layout

```
docs/archive/compliance/alignment_audit_reports/
  <audit_id>/                 # e.g. 20260719T061021Z_post_merge
    report.json               # full audit payload
    report.md                 # human-readable (embeds visuals/)
    dashboard.html            # stakeholder dashboard
    recommendations.json      # checklist + recommendations only (easy diff)
    visuals/                  # PNG snapshot of report_only management set (Git LFS)

docs/archive/compliance/alignment_audit_visuals/
  latest/                     # current management slides (pointers / regen target)
  style/                      # tides_* style kit + packs (templates)
```

Index: `docs/archive/compliance/alignment_audit_history.json`  
Retention: `outputs.committed_history_keep` (default **20** audit folders).

## Run and save

```bash
bash tools/run_alignment_audit.sh \
  --trigger post_merge \
  --note "PR #N" \
  --visuals-from docs/archive/compliance/alignment_audit_visuals/latest
```

This writes `<audit_id>/` including `visuals/` (enabled by `archive_visual_snapshots: true`).

```bash
git add docs/archive/compliance/alignment_audit_reports/ \
        docs/archive/compliance/alignment_audit_history.json \
        docs/archive/compliance/alignment_audit_visuals/latest/
git commit -m "chore(audit): record alignment audit <audit_id>"
```

PNGs under `visuals/`, `latest/`, and `style/` are Git LFS-tracked (see `.gitattributes` + `docs/ops/ci-cd/GIT_LFS.md`).

Authority: `docs/ops/qa/ALIGNMENT_AUDIT.md`
