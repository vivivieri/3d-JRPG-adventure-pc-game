# Performance Baseline — Hardware, Environment & Evidence

**Version:** 1.0  
**Machine-readable:** `game/data/qa/perf_baseline.json`  
**Thresholds:** `game/data/qa/perf_thresholds.json`  
**Cross-refs:** `docs/RENDERING_GUIDE.md`, `docs/ENVIRONMENT_KITS.md` §9, `docs/RR_CHEATSHEET.md` §Performance review, `docs/ACCEPTANCE_CRITERIA.md`, `steam/STORE_PAGE.md`

This document defines **what machine and runtime profile** performance numbers mean. Without a baseline, “60 FPS” is not comparable across cloud VMs, editor play, and player hardware.

---

## 1. Why this exists

| Problem | Baseline solves |
|---------|-----------------|
| Cloud agent reports 45 FPS on unknown GPU | Evidence must cite `baseline_id`; cloud is **invalid** for ship sign-off |
| Editor F5 vs exported `.exe` differ | Doc states which is authoritative per gate |
| Steam minimum vs recommended blur together | Two profiles: **reference** (ship) vs **minimum** (support floor) |
| Perf review has no CPU/RAM fields | Evidence schema requires hardware capture when available |

**Policy:** `L3_perf_review` PASS requires evidence captured on **`reference_pc_gtx1060`** (or human-approved equivalent documented in the PR). See `game/data/qa/perf_baseline.json`.

---

## 2. Baseline profiles (summary)

| `baseline_id` | Purpose | Valid for `L3_perf_review` ship PASS? |
|---------------|---------|--------------------------------------|
| **`reference_pc_gtx1060`** | Ship target — art tuning, sprint gates, M5 zone sign-off | **Yes** |
| `steam_minimum` | Store listing floor — spot-check at M6 only | No |
| `cloud_agent_jit` | Cursor Cloud JIT VM — catalog CI only | No |
| `ci_headless` | GitHub Actions boot/integration | No |

Full field-level spec: `game/data/qa/perf_baseline.json` → `baselines`.

---

## 3. Reference PC — `reference_pc_gtx1060`

**This is the default “60 FPS @ 1080p” target** cited in `RENDERING_GUIDE.md`, `ENVIRONMENT_KITS.md`, and `perf_thresholds.json`.

### 3.1 Hardware

| Component | Spec | Notes |
|-----------|------|-------|
| **OS** | Windows 10/11 64-bit | Ship platform; Linux dev is not perf sign-off |
| **CPU** | 6-core desktop, ~2.8 GHz+ | Examples: i5-8400, Ryzen 5 2600 |
| **System RAM** | 16 GB recommended (8 GB min) | Close background apps during capture |
| **GPU** | GTX 1060 6 GB class | Examples: GTX 1060 6 GB, RX 580 8 GB |
| **VRAM** | ≥ 6 GB | 2 GB is Steam *recommended* floor, not ship target |
| **Display** | 1920×1080, 100% scaling | Single monitor |

### 3.2 Godot runtime profile (perf test)

Lock these settings for every `L3_perf_review` capture:

| Setting | Value | Source |
|---------|-------|--------|
| Godot | **4.7** stable | `docs/TECH_STACK.md` |
| Renderer | **Forward+** | `project.godot` |
| **Graphics quality** | **Medium** | `docs/RENDERING_GUIDE.md` §10 |
| Shadows | Soft, 1024 | Medium preset |
| MSAA | 2× | Medium preset |
| Glow | On | Medium preset |
| Fog density | 100% (zone default) | Zone `WorldEnvironment` |
| SSAO / SSIL | **Off** | v1 policy |
| **VSync** | **Off** during capture | Fair FPS measurement |
| **Fullscreen** | **On** @ 1080p | Match ship default |
| Windowed editor | Allowed for **dev** only | Editor min **55 FPS**; export is authoritative at M6 |

### 3.3 FPS & scene budgets

From `game/data/qa/perf_thresholds.json`:

| Metric | Target | Investigate |
|--------|--------|-------------|
| FPS (gameplay cam, 30s walk) | **≥ 60** | **< 30** |
| FPS (editor F5, same path) | **≥ 55** | < 30 |
| Materials visible per view | **≤ 8** | > 8 |
| Draw calls | — | **> 1000** |
| Node count | — | steady growth = leak |

**First gate zone:** `ruined_village` (SC-02) — vertical slice before other hubs.

---

## 4. Steam minimum — `steam_minimum`

Mirrors `steam/STORE_PAGE.md` **minimum** row. Used for:

- Store page accuracy  
- Optional M6 spot-check (720p Low, 30 FPS playable)  
- **Not** used to PASS `L3_perf_review` on ship art  

| Component | Spec |
|-----------|------|
| CPU | Dual-core 2.0 GHz+ |
| RAM | 4 GB |
| GPU | OpenGL 3.3 / Vulkan 1.0, 2 GB VRAM class |
| Resolution | 1280×720 |
| Quality | Low preset |

---

## 5. Invalid environments (do not sign off perf)

| Environment | Why invalid | Allowed use |
|-------------|-------------|-------------|
| **Cursor Cloud Agent JIT** | No pinned GPU; `build: null` VMs | `L2_perf_catalog`, docs, scripting |
| **GitHub Actions CI** | Headless, no GPU frame loop | L0–L2 boot, integration |
| **Godot editor on Mac/Linux dev** | Not ship OS | Dev iteration only — note OS in evidence |
| **Laptop power-saving mode** | Throttled CPU/GPU | Disable for capture |

Agents must **not** mark `L3_perf_review: PASS` from cloud FPS snapshots.

---

## 6. Test procedure (`L3_perf_review`)

### 6.1 When to run

See `docs/RR_CHEATSHEET.md` §Performance review — scene/shader/material/mesh/light/fog changes and post-fix regression.

### 6.2 Steps

1. **Machine:** `reference_pc_gtx1060` Windows PC (or documented equivalent in PR).  
2. **Build:** same commit SHA as PR; prefer **exported build** from M6 onward; editor F5 allowed Phase 1–5 with note.  
3. **Settings:** Medium quality, 1080p fullscreen, VSync off.  
4. **Zone:** load zone from `perf_thresholds.json` → `zones[]` (e.g. `ruined_village`).  
5. **Path:** gameplay camera — walk hub path **30s** (`test_duration_s`).  
6. **Capture:** Godotiq `godotiq_perf_snapshot(detail="normal")` with game running.  
7. **Record:** write JSON to `artifacts/perf_reviews/{zone}_{short_sha}.json` (schema §7).  
8. **PR:** paste path in gate report; cite `baseline_id: reference_pc_gtx1060`.

### 6.3 Post-fix regression

When fixing perf-related bugs, re-run §6.2 on the affected zone **plus** `docs/QA_AND_BUG_PROCESS.md` §6 (adjacent scenes, `INT-*` if flows changed).

---

## 7. Evidence schema

**Path:** `artifacts/perf_reviews/{zone}_{short_sha}.json`

**Example:**

```json
{
  "baseline_id": "reference_pc_gtx1060",
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

## 8. Relationship to gates

| Gate | What it checks | Baseline needed? |
|------|----------------|------------------|
| `L2_perf_catalog` | `perf_thresholds.json` + `perf_baseline.json` valid | No — runs anywhere |
| `L3_perf_review` | FPS, draw calls, materials after F5 | **Yes** — `reference_pc_gtx1060` |
| `L6_human_playtest` | Feel, fun, readability | Human machine noted in report |

---

## 9. Implementation plan

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

## 10. Commands

```bash
# Validate baseline + thresholds catalogs (L2 — any environment)
bash tools/run_perf_review_checks.sh

# After capture — manual check of evidence file
python3 -m json.tool artifacts/perf_reviews/ruined_village_abc1234.json
```

---

## 11. Related docs

| Doc | Contents |
|-----|----------|
| `docs/RENDERING_GUIDE.md` §10 | Low / Medium / High presets |
| `docs/ENVIRONMENT_KITS.md` §9 | LOD + material batching |
| `docs/RR_CHEATSHEET.md` | Performance review workflow |
| `docs/QA_AND_BUG_PROCESS.md` §6 | Post-fix regression |
| `steam/STORE_PAGE.md` | Public system requirements |
| `docs/STEAM_RELEASE_CHECKLIST.md` | M6 hardware smoke |
