# Alignment Audit — Standard Process & Stakeholder Reporting

**Version:** 1.1
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

1. **Verdict** — `ALIGNED` · `AT_RISK` · `FAIL` (CI + applicable streams)
2. **Two streams** — **Spec readiness** (design & prep) and **Build readiness** (dev & ship)
3. **Domain radar scores** (0–10) — grouped by stream, not one merged mega-radar
4. **CI summary** — gate PASS/FAIL counts
5. **Data parity** — encounters, hooks, tutorial flags, sprint board ↔ sprint pack IDs
6. **Full recommendation checklist** — P0–P3 by category
7. **Visual manifest** — stakeholder PNG packs (when bundled)

### 1b. Two streams (management view)

**Do not show one merged radar to management** — it makes spec work look incomplete when build has not started.

| Stream | ID | Primary branch | Question |
|--------|-----|----------------|----------|
| **Design & preparation** | `spec_readiness` | `main` | Can we dispatch builders? Is design truth complete? |
| **Development & shipping** | `build_readiness` | `game/development` | Does the game run, pass gates, and approach Steam? |

On **`main`**, build stream is **N/A** (no `project.godot` by design). Headline: `Spec 9.8/10 · Build N/A`.

On **`game/development`**, both streams score independently. Verdict = worst applicable stream after CI pass.

**GitHub:** `report.md` § Streams. **Local:** `dashboard.html` — two stream cards at top.

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

**Workflow integration:** After adding cross-cutting factory features, register in `game/data/qa/workflow_integration_registry.json` and verify `L0_workflow_integration` PASS — see `docs/qa/WORKFLOW_INTEGRATION.md`.

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

**Auto-generated each audit run** (from live `report.json` scores — do not hand-edit):

| File | Content |
|------|---------|
| `audit_radar_report.png` | **Primary** — side-by-side spec + build radar report |
| `audit_radar_spec.png` | Spec stream radar (6 domains) |
| `audit_radar_spec_breakdown.png` | **6-panel grid** — one sub-radar per spec domain (signal breakdown) |
| `audit_radar_spec_<domain>.png` | Individual sub-radar per domain (e.g. `data_alignment`, `narrative`, …) |
| `audit_radar_build.png` | Build stream radar on `game/development`, or **N/A card** on `main` |
| `audit_radar_build_breakdown.png` | **2-panel grid** — one sub-radar per build domain (signal breakdown) |
| `audit_radar_build_<domain>.png` | Individual sub-radar per build domain (`runtime_proof`, `steam_ship`) |

Each spec domain score rolls up **signals** (gates, parity checks, metrics). Sub-radars show those signals on a 0–10 axis; see `report.md` § Spec domain signal breakdown and § Build domain signal breakdown.

**Visual theme:** Radars use the game palette (`docs/art/ART_DIRECTION.md`) — void sky `#1A1A3A`, biolume `#4AE8D8`, fog `#8B9DAF`, lantern gold `#D4A880`, per-domain accents. Renderer: `tools/audit_radar_theme.py`.

Regenerate manually: `python3 tools/generate_audit_radar_images.py --report artifacts/alignment_audits/latest.json`

Legacy merged radars (`audit_radar_6axis.png`, `tides_mega_dashboard_all_radars.png`) remain on disk for archive but are **never shown** in audit reports.

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
