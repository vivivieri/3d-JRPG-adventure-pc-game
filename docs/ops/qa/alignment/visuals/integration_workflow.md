---
id: integration-workflow
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 422
summary: "Alignment — Visuals / History / Integration — PM integration + workflow + catalog — Run both at phase exit: stakeholder report for schedule; alignment audit."
---
# Alignment — Visuals / History / Integration — PM integration + workflow + catalog

**Hub:** [`visuals_history_integration.md`](../visuals_history_integration.md)

## When to read

Use **Alignment — Visuals / History / Integration — PM integration + workflow + catalog** (roles: pm, qa) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [9. Integration with PM stakeholder reporting](#9-integration-with-pm-stakeholder-reporting)
- [10. Agent workflow (mandatory after alignment work)](#10-agent-workflow-mandatory-after-alignment-work)
- [11. Catalog validation](#11-catalog-validation)


## 9. Integration with PM stakeholder reporting

| Report | Audience | Focus |
|--------|----------|-------|
| `pm_emit_stakeholder_report.sh` | Product owner | Sprint/phase/factory cycle |
| `run_alignment_audit.sh` | Product owner + tech lead | Spec alignment, data parity, ship readiness |

Run **both** at phase exit: stakeholder report for schedule; alignment audit for technical debt and dispatch readiness.

---



## 10. Agent workflow (mandatory after alignment work)

```
1. bash tools/run_alignment_audit.sh --trigger post_merge --note "<PR or commit summary>" \
     --visuals-from docs/archive/compliance/alignment_audit_visuals/latest
2. Read docs/archive/compliance/alignment_audit_reports/<audit_id>/report.md — cite verdict + P0 items
3. Commit docs/archive/compliance/alignment_audit_reports/<audit_id>/ and alignment_audit_history.json on main
```

---



## 11. Catalog validation

```bash
python3 tools/validate_alignment_audit_catalog.py   # L0_alignment_audit_catalog
```

Wired in `bash tools/run_docs_ci_checks.sh`.
