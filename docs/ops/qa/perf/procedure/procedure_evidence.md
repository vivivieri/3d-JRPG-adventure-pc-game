---
id: procedure-evidence
type: how-to
phase: [1, 6]
audience: [qa, release, builder]
status: active
authority: qa
tokens_est: 596
summary: "Procedure + evidence schema"
---
# Perf — Procedure & Evidence — Procedure + evidence schema

**Hub:** [`procedure_evidence.md`](../procedure_evidence.md)

## 7. Test procedure (`L3_perf_review`)

### 7.1 When to run

See `docs/ops/cheat-sheets/RR_CHEATSHEET.md` §Performance review — scene/shader/material/mesh/light/fog changes and post-fix regression.

### 7.2 Steps

1. **Machine:** `reference_linux_cloud` (cloud snapshot) **or** `reference_pc_gtx1060` (Windows PC).
2. **Build:** same commit SHA as PR; Linux native export from M6; editor F5 allowed Phase 1–5.
3. **Settings:** Medium quality, 1080p fullscreen, VSync off.
4. **Zone:** load zone from `perf_thresholds.json` → `zones[]` (e.g. `ruined_village`).
5. **Path:** gameplay camera — walk hub path **30s** (`test_duration_s`).
6. **Capture:** Godotiq `godotiq_perf_snapshot(detail="normal")` with game running.
7. **Record:** write JSON to `artifacts/perf_reviews/{zone}_{short_sha}.json` (schema §7).
8. **PR:** paste path in gate report; cite `baseline_id` (`reference_linux_cloud` or `reference_pc_gtx1060`).

### 7.3 Post-fix regression

When fixing perf-related bugs, re-run §7.2 on the affected zone **plus** `docs/ops/qa/QA_AND_BUG_PROCESS.md` §6 (adjacent scenes, `INT-*` if flows changed).

---



## 8. Evidence schema

**Path:** `artifacts/perf_reviews/{zone}_{short_sha}.json`

**Example:**

```json
{
  "baseline_id": "reference_linux_cloud",
  "commit_sha": "9f93a10",
  "zone_id": "ruined_village",
  "captured_at": "2026-07-16T12:00:00Z",
  "resolution": "1920x1080",
  "graphics_quality": "medium",
  "vsync": false,
  "fullscreen": true,
  "fps_avg": 62.4,
  "fps_min": 58.1,
  "draw_calls": 412,
  "node_count": 1847,
  "materials_visible": 6,
  "tool": "godotiq_perf_snapshot",
  "gpu_name": "NVIDIA GeForce GTX 1060 6GB",
  "cpu_name": "Intel Core i5-8400",
  "ram_gb": 16,
  "godot_version": "4.7.stable",
  "editor_vs_export": "editor",
  "notes": "Phase 1 vertical slice — hub walk torii to well"
}
```

**Required fields:** `game/data/qa/perf_baseline.json` → `evidence_schema.required_fields`

**Invalid PASS:** missing `baseline_id` · `baseline_id` = `cloud_agent_jit` or `ci_headless` · no `zone_id` · FPS below target with no remediation brief

---
