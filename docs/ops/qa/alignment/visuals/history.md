---
id: history
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 390
summary: "`docs/archive/compliance/alignment_audit_history.json`"
---
# Alignment — Visuals / History / Integration — Committed history

**Hub:** [`visuals_history_integration.md`](../visuals_history_integration.md)

## When to read

Use **Alignment — Visuals / History / Integration — Committed history** (roles: pm, qa) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



## 8. History (committed on GitHub)

**Index:** `docs/archive/compliance/alignment_audit_history.json`

**Per-audit folder:** `docs/archive/compliance/alignment_audit_reports/<audit_id>/`

| File | Purpose |
|------|---------|
| `report.json` | Full audit — scores, CI, recommendations, visual manifest |
| `report.md` | Human-readable report with embedded image links |
| `dashboard.html` | Stakeholder dashboard (open locally or download) |
| `recommendations.json` | Checklist + recommendations only (easy `git diff`) |
| `visuals/` | PNG snapshot of management set (always on; Git LFS) |

Each entry in the history index records: `audit_id`, `commit`, `verdict`, `overall_score`, CI counts, checklist counts, paths to committed reports.

Ephemeral copies (regenerate locally): `artifacts/alignment_audits/<audit_id>/` (git-ignored).

**Shared packs (not versioned per run):**

| Path | Role |
|------|------|
| `…/alignment_audit_visuals/latest/` | Current management slides |
| `…/alignment_audit_visuals/style/` | `tides_*` style kit |

**Commit after each audit on `main`:**

```bash
bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N" \
  --visuals-from docs/archive/compliance/alignment_audit_visuals/latest
git add docs/archive/compliance/alignment_audit_reports/ \
        docs/archive/compliance/alignment_audit_history.json \
        docs/archive/compliance/alignment_audit_visuals/latest/
git commit -m "chore(audit): record alignment audit <audit_id>"
```

---
