---
id: procedure-evidence
type: reference
phase: [1, 6]
audience: [qa, builder, release]
status: active
authority: qa
tokens_est: 1342
summary: "Procedure, evidence, gates, plan, commands"
---
# Performance Baseline — Procedure, evidence, gates, plan, commands

**Hub:** [`PERFORMANCE_BASELINE.md`](../PERFORMANCE_BASELINE.md)

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


## 9. Relationship to gates

| Gate | What it checks | Baseline needed? |
|------|----------------|------------------|
| `L2_perf_catalog` | `perf_thresholds.json` + `perf_baseline.json` valid | No — runs anywhere |
| `L3_perf_review` | FPS, draw calls, materials after F5 | **Yes** — Linux snapshot and/or Windows PC |
| `L6_human_playtest` | Feel, fun, readability | Human machine noted in report |

---


## 10. Implementation plan

### Phase 1 — P1-00 (bootstrap)

| Task | Owner | Done when |
|------|-------|-----------|
| `game/project.godot` on `game/development` | PM / Architect | CI boot gate runs |
| Medium graphics preset keys in settings | Architect | `graphics_quality` applies `RENDERING_GUIDE.md` §10 |
| Document baseline in PR template | PM | ✅ this doc + `perf_baseline.json` |

### Phase 2 — P1-02 (ruined village)

| Task | Owner | Done when |
|------|-------|-----------|
| First `ruined_village` scene playable | Builder | F5 clean |
| First perf evidence JSON | Builder | `artifacts/perf_reviews/ruined_village_*.json` on reference PC |
| Gate report cites baseline | QA | PR shows `L3_perf_review: PASS` |

### Phase 3 — M5 (art pass)

| Task | Owner | Done when |
|------|-------|-----------|
| Perf evidence per ship zone | Builder + QA | All `perf_thresholds.json` zones have JSON |
| Remediation loop for FAIL | QA | `qa_emit_remediation.sh` perf brief |
| ≤ 8 materials enforced per zone | Builder | snapshot + visual review |

### Phase 4 — M6 (Steam ship)

| Task | Owner | Done when |
|------|-------|-----------|
| Exported `.exe` perf on reference PC | Release + QA | `editor_vs_export: export` in evidence |
| `steam_minimum` spot-check | Human QA | 720p Low ≥ 30 FPS documented |
| `STEAM_RELEASE_CHECKLIST.md` §2.11 | Release | Windows hardware row checked |

### Optional automation (later)

| Item | Notes |
|------|-------|
| `tools/validate_perf_evidence.py` | Lint evidence JSON against schema |
| CI upload of perf artifacts | Store in GitHub Actions artifacts — still not valid for ship PASS |
| Dedicated reference hardware label | GitHub self-hosted runner or QA bench sticker |

---


## 11. Commands

```bash
# Validate baseline + thresholds catalogs (L2 — any environment)
bash tools/run_perf_review_checks.sh

# After capture — manual check of evidence file
python3 -m json.tool artifacts/perf_reviews/ruined_village_abc1234.json
```

---


## 12. Related docs

| Doc | Contents |
|-----|----------|
| `docs/ops/qa/PLATFORM_SUPPORT.md` | **Linux + Windows ship policy; cloud dev parity** |
| `docs/design/art/RENDERING_GUIDE.md` §10 | Low / Medium / High presets |
| `docs/design/world/ENVIRONMENT_KITS.md` §9 | LOD + material batching |
| `docs/ops/cheat-sheets/RR_CHEATSHEET.md` | Performance review workflow |
| `docs/ops/qa/QA_AND_BUG_PROCESS.md` §6 | Post-fix regression |
| `steam/STORE_PAGE.md` | Public system requirements |
| `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` | M6 hardware smoke |
