---
id: alignment-gates
type: how-to
phase: [1, 6]
audience: [pm, architect]
status: active
authority: qa
tokens_est: 433
summary: "Workflow Integration — Alignment coop + related gates — alignment_audit_catalog.json` → `pm_workflow` domain includes workflow integration health. On FAIL, reco"
---
# Workflow Integration — Alignment coop + related gates

**Hub:** [`WORKFLOW_INTEGRATION.md`](../WORKFLOW_INTEGRATION.md)

## When to read

Use **Workflow Integration — Alignment coop + related gates** (roles: pm, architect) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [5. Alignment audit cooperation](#5-alignment-audit-cooperation)
- [6. Related gates](#6-related-gates)


## 5. Alignment audit cooperation

`alignment_audit_catalog.json` → `pm_workflow` domain includes workflow integration health. On FAIL, recommendation **`REC_WORKFLOW_DRIFT`** points here.

PM should run alignment audit after any registry change:

```bash
bash tools/run_alignment_audit.sh --trigger post_merge --note "workflow integration update"
```

**Management visuals:** reports split **Management visuals** (status) from **Legacy visuals** (archive). Use only `audit_radar_spec.png` + `audit_radar_build.png` for executive readiness — not `tides_mega_dashboard_all_radars.png`. Auto-generated on every audit run via `generate_audit_radar_images.py`.

**Full-surface example:** `alignment_audit` is the reference registry entry — script hooks (`alignment_audit_lib.py`, `generate_audit_radar_images.py`), `visual_policy` in catalog, all `standard_agent_surfaces`, and report/HTML management sections must ship together.

---


## 6. Related gates

| Gate | Role |
|------|------|
| `L0_doc_sync` | README index + runner gate list parity |
| `L0_workflow_integration` | Factory feature hook + doc parity |
| `L0_alignment_audit_catalog` | Stakeholder audit catalog valid |

**`L0_doc_sync`** catches missing README links. **`L0_workflow_integration`** catches missing factory wiring.
