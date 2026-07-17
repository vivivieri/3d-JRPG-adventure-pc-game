# Alignment Audit — Standard Process & Stakeholder Reporting

**Version:** 1.0  
**Authority:** Run after every spec alignment pass, PR merge to `main`, or phase exit on `game/development`.  
**Cross-refs:** `docs/qa/ACCEPTANCE_CRITERIA.md`, `docs/agents/PM_STAKEHOLDER_REPORTING.md`, `game/data/qa/alignment_audit_catalog.json`

---

## 1. Purpose

Produces a **repeatable alignment audit** with:

| Output | Path |
|--------|------|
| JSON report (latest) | `artifacts/alignment_audits/latest.json` |
| Markdown report | `artifacts/alignment_audits/latest.md` |
| HTML stakeholder dashboard | `artifacts/alignment_dashboard.html` |
| **Committed history (GitHub)** | `docs/compliance/alignment_audit_reports/<audit_id>/` |
| History index | `docs/compliance/alignment_audit_history.json` |
| Timestamped artifact folder | `artifacts/alignment_audits/<audit_id>/` |

Each audit includes:

1. **Verdict** — `ALIGNED` · `AT_RISK` · `FAIL`
2. **Domain radar scores** (0–10) — nine domains + overall
3. **CI summary** — gate PASS/FAIL counts
4. **Data parity** — encounters, hooks, tutorial flags
5. **Full recommendation checklist** — P0–P3 by category
6. **Visual manifest** — stakeholder PNG packs (when bundled)

---

## 2. When to run

| Trigger | Command |
|---------|---------|
| After alignment PR merge | `bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N"` |
| End of agent session | `bash tools/run_alignment_audit.sh --trigger agent_session` |
| Before P1-00 dispatch | `bash tools/run_alignment_audit.sh --trigger pre_dispatch` |
| Phase exit | `bash tools/run_alignment_audit.sh --trigger phase_exit` |
| Manual | `bash tools/run_alignment_audit.sh` |

**PM orchestrator:** add as optional post-step alongside stakeholder report when alignment work lands.

---

## 3. How to run

```bash
# Full audit (runs docs CI or game CI based on branch)
bash tools/run_alignment_audit.sh

# With stakeholder visuals bundled from a directory
bash tools/run_alignment_audit.sh --visuals-from docs/compliance/alignment_audit_visuals

# Fast check without re-running CI (uses skip — scores approximate)
bash tools/run_alignment_audit.sh --skip-ci --trigger quick_check
```

Open dashboard for product owner:

```bash
xdg-open artifacts/alignment_dashboard.html   # Linux
open artifacts/alignment_dashboard.html       # macOS
```

---

## 4. Verdict rules

Configured in `alignment_audit_catalog.json` → `verdict_thresholds`:

| Verdict | Condition |
|---------|-----------|
| **FAIL** | Any CI gate FAIL |
| **AT_RISK** | Blocking checklist items open, or overall &lt; 8.0 |
| **ALIGNED** | CI all PASS, no blocking checklist, overall ≥ 8.0 |

---

## 5. Domain scores (radar axes)

| ID | Label | Main signals |
|----|-------|----------------|
| `overall_production` | Overall | Mean of sibling domains |
| `data_alignment` | Data Alignment | Registry parity + L0 scene/story gates |
| `narrative` | Narrative | Story spine, density, VO/hooks count |
| `gameplay` | Gameplay | Spec registry, encounters, combat data |
| `visual_spec` | Visual Spec | Zone visuals contract, palettes |
| `ux_controls` | UX & Controls | Settings/combat docs; impl scenes cap on main |
| `pm_workflow` | PM Workflow | CI pass rate, doc sync, PM orchestrator |
| `runtime_proof` | Runtime Proof | project.godot, L2/L4/L5 gates (low on `main` by design) |
| `steam_ship` | Steam Ship M6 | Ship security, asset compliance, runtime ref |

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

## 7. Stakeholder visuals

Six visual packs (33 assets) are catalogued for executive updates:

| Pack | Title | Assets |
|------|-------|--------|
| `batch_01_foundation` | Foundation review | 3 |
| `batch_02_zones` | Zones & alignment | 6 |
| `batch_03_endings_dispatch` | Endings & P1-00 | 6 |
| `batch_04_combat_audio` | Combat & audio QA | 6 |
| `batch_05_qa_flow` | Visual/model/flow QA | 6 |
| `batch_06_steam_mega` | Steam ship & mega dashboard | 6 |

**Store PNGs** under `docs/compliance/alignment_audit_visuals/` (committed) or pass `--visuals-from <dir>` at audit time.  
See `docs/compliance/alignment_audit_visuals/README.md`.

Agent-generated review images can be copied into that folder before running the audit so the HTML dashboard embeds them.

---

## 8. History (committed on GitHub)

**Index:** `docs/compliance/alignment_audit_history.json`

**Per-audit folder:** `docs/compliance/alignment_audit_reports/<audit_id>/`

| File | Purpose |
|------|---------|
| `report.json` | Full audit — scores, CI, recommendations, visual manifest |
| `report.md` | Human-readable report with embedded image links |
| `dashboard.html` | Stakeholder dashboard (open locally or download) |
| `recommendations.json` | Checklist + recommendations only (easy `git diff`) |
| `visuals/` | Optional PNG snapshot (`--archive-visual-snapshots`) |

Each entry in the history index records: `audit_id`, `commit`, `verdict`, `overall_score`, CI counts, checklist counts, paths to committed reports.

Ephemeral copies (regenerate locally): `artifacts/alignment_audits/<audit_id>/` (git-ignored).

**Commit after each audit on `main`:**

```bash
bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N" \
  --visuals-from docs/compliance/alignment_audit_visuals
git add docs/compliance/alignment_audit_reports/ docs/compliance/alignment_audit_history.json
git commit -m "chore(audit): record alignment audit <audit_id>"
```

---

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
     --visuals-from docs/compliance/alignment_audit_visuals
2. Read docs/compliance/alignment_audit_reports/<audit_id>/report.md — cite verdict + P0 items
3. Commit docs/compliance/alignment_audit_reports/<audit_id>/ and alignment_audit_history.json on main
```

---

## 11. Catalog validation

```bash
python3 tools/validate_alignment_audit_catalog.py   # L0_alignment_audit_catalog
```

Wired in `bash tools/run_docs_ci_checks.sh`.
