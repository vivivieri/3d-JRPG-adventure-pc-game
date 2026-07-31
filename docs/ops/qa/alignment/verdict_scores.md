---
id: verdict-scores
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 773
summary: "Verdict rules, radar axes, checklist"
---
# Alignment Audit — Verdict rules, radar axes, checklist

**Hub:** [`ALIGNMENT_AUDIT.md`](../ALIGNMENT_AUDIT.md)

## 4. Verdict rules

**Radar vs CI (read this):** Domain scores (0–10) are **indicative** — they sample weighted signals per domain, not every CI gate. The **verdict** follows CI only:

| Layer | Authority | Misread risk |
|-------|-----------|--------------|
| **Verdict** | Any CI gate FAIL → `FAIL` (when `fail_any_ci` is true) | None — this is the ship/dispatch gate |
| **Streams** | Worst applicable stream (`spec_readiness` / `build_readiness`) | Build N/A on `main` is expected, not failure |
| **Radar** | Weighted subset of signals per domain, grouped by stream | `--skip-ci` audits score ~0 on gate signals |
| **Parity** | Encounters, hooks, tutorial flags, sprint board ↔ pack | Catches data drift CI schema gates may miss |

Configured in `alignment_audit_catalog.json` → `verdict_thresholds`:

| Verdict | Condition |
|---------|-----------|
| **FAIL** | Any CI gate FAIL, or any applicable stream &lt; 6.5 (build) / &lt; 6.5 (spec) |
| **AT_RISK** | Blocking checklist items open, or any applicable stream in AT_RISK band |
| **ALIGNED** | CI all PASS, no blocking checklist, all applicable streams ≥ aligned threshold |

Stream thresholds in `alignment_audit_catalog.json` → `verdict_thresholds`: spec uses `aligned_min_overall` (8.0); build uses `build_aligned_min` (6.0) on `game/development`.

---


## 5. Domain scores (radar axes)

Domains are grouped into streams in `alignment_audit_catalog.json` → `streams`:

### Spec stream (`spec_readiness`)

| ID | Label | Main signals |
|----|-------|----------------|
| `data_alignment` | Data Alignment | Registry parity + L0 scene/story gates + sprint board ↔ pack |
| `narrative` | Narrative | Story spine, density, VO/hooks count |
| `gameplay` | Gameplay | Spec registry, encounters, combat data |
| `visual_spec` | Visual Spec | Zone visuals contract, palettes |
| `ux_controls` | UX & Controls | Settings/combat docs |
| `pm_workflow` | PM Workflow | CI pass rate, doc sync, factory gates |

### Build stream (`build_readiness`)

| ID | Label | Main signals |
|----|-------|----------------|
| `runtime_proof` | Runtime Proof | project.godot, L2/L4/L5 gates |
| `steam_ship` | Steam Ship M6 | Ship security, asset compliance, runtime ref |

### Legacy alias

| ID | Label | Notes |
|----|-------|-------|
| `overall_production` | Overall Spec (legacy) | Equals `spec_readiness` score — hidden from dashboard; do not use for management |

---


## 6. Recommendation checklist categories

| Category | Priority | Clear before P1-00? |
|----------|----------|---------------------|
| `blocking` | P0 | **Yes** |
| `before_dispatch` | P1 | Review |
| `implementation` | P1 | No |
| `ship_path` | P2 | No |
| `stakeholder` | P2 | No |
| `doc_nit` | P3 | No |

Rules are data-driven in `alignment_audit_catalog.json` → `recommendation_rules`.

---
