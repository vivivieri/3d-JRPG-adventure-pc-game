---
id: stakeholder-visuals
type: how-to
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 645
summary: "Six visual packs (33 assets) are catalogued for executive updates:"
---
# Alignment — Visuals / History / Integration — Stakeholder visuals

**Hub:** [`visuals_history_integration.md`](../visuals_history_integration.md)

## When to read

Use **Alignment — Visuals / History / Integration — Stakeholder visuals** (roles: pm, qa) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



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
| `audit_exec_summary.png` | **Primary presentation slide** — illustrated tides_ aesthetic |
| `audit_radar_report.png` | Side-by-side spec + build (illustrated) |
| `audit_radar_spec.png` | Spec stream radar (6 domains, illustrated) |
| `audit_radar_spec_breakdown.png` | Spec domain grid (illustrated) |
| `audit_radar_spec_<domain>.png` | Individual technical sub-radar (matplotlib fallback OK) |
| `audit_radar_build.png` | Build stream radar or **AWAITING TIDE** card (illustrated) |
| `audit_radar_build_breakdown.png` | Build domain grid (matplotlib fallback OK) |
| `audit_radar_build_<domain>.png` | Individual build sub-radar |

**Style authority:** Match `tides_audit_radar_updated.png` / `audit_radar_6axis.png` — navy parchment, gold ornate frame, moon/clouds/pagoda/waves, teal radar fill, gold circular axis icons. **Not** flat matplotlib corporate charts.

Management illustrated files are listed in `visual_policy.illustrated_locked_filenames` and are **preserved** on audit runs unless `generate_audit_radar_images.py --force`. Regenerate illustrated art via GameLab / image gen with `tides_*` references + live scores.

Matplotlib (`tools/audit_radar_theme.py`) remains for unlocked technical sub-radars only.

Agent-generated review images can be copied into that folder before running the audit so the HTML dashboard embeds them.

---
