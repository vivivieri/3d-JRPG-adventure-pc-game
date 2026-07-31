---
id: stakeholder-visuals
type: how-to
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
