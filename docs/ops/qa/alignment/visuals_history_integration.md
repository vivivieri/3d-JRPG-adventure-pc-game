---
id: visuals-history-integration
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 1196
summary: "Visuals, history, stakeholder, workflow, catalog"
---
# Alignment Audit — Visuals, history, stakeholder, workflow, catalog

**Hub:** [`ALIGNMENT_AUDIT.md`](../ALIGNMENT_AUDIT.md)

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

**Store PNGs** under `docs/archive/compliance/alignment_audit_visuals/` (committed) or pass `--visuals-from <dir>` at audit time.

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

**Visual theme:** Radars use the game palette (`docs/design/art/ART_DIRECTION.md`) — void sky `#1A1A3A`, biolume `#4AE8D8`, fog `#8B9DAF`, lantern gold `#D4A880`, per-domain accents. Renderer: `tools/audit_radar_theme.py`.

Regenerate manually: `python3 tools/generate_audit_radar_images.py --report artifacts/alignment_audits/latest.json`

Legacy merged radars (`audit_radar_6axis.png`, `tides_mega_dashboard_all_radars.png`) remain on disk for archive but are **never shown** in audit reports.

Agent-generated review images can be copied into that folder before running the audit so the HTML dashboard embeds them.

---


## 8. History (committed on GitHub)

**Index:** `docs/archive/compliance/alignment_audit_history.json`

**Per-audit folder:** `docs/archive/compliance/alignment_audit_reports/<audit_id>/`

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
  --visuals-from docs/archive/compliance/alignment_audit_visuals
git add docs/archive/compliance/alignment_audit_reports/ docs/archive/compliance/alignment_audit_history.json
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
     --visuals-from docs/archive/compliance/alignment_audit_visuals
2. Read docs/archive/compliance/alignment_audit_reports/<audit_id>/report.md — cite verdict + P0 items
3. Commit docs/archive/compliance/alignment_audit_reports/<audit_id>/ and alignment_audit_history.json on main
```

---


## 11. Catalog validation

```bash
python3 tools/validate_alignment_audit_catalog.py   # L0_alignment_audit_catalog
```

Wired in `bash tools/run_docs_ci_checks.sh`.
