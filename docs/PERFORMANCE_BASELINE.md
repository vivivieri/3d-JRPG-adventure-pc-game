# Performance Baseline — Hardware, Environment & Evidence

**Version:** 1.1  
**Machine-readable:** `game/data/qa/perf_baseline.json`  
**Platform policy:** `docs/PLATFORM_SUPPORT.md` — **Linux ship required** (cloud dev OS)  
**Thresholds:** `game/data/qa/perf_thresholds.json`  
**Cross-refs:** `docs/RENDERING_GUIDE.md`, `docs/ENVIRONMENT_KITS.md` §9, `docs/RR_CHEATSHEET.md` §Performance review, `docs/ACCEPTANCE_CRITERIA.md`, `steam/STORE_PAGE.md`

This document defines **what machine and runtime profile** performance numbers mean. Without a baseline, “60 FPS” is not comparable across cloud VMs, editor play, and player hardware.

---

## 1. Why this exists

| Problem | Baseline solves |
|---------|-----------------|
| Cloud agent reports 45 FPS on unknown GPU | JIT boot invalid; **snapshot Linux** valid with `reference_linux_cloud` |
| Editor F5 vs exported `.exe` differ | Doc states which is authoritative per gate |
| Steam minimum vs recommended blur together | Two profiles: **reference** (ship) vs **minimum** (support floor) |
| Perf review has no CPU/RAM fields | Evidence schema requires hardware capture when available |

**Policy:** `L3_perf_review` PASS requires evidence on a **ship baseline** — **`reference_linux_cloud`** (cloud snapshot / Linux depot) and **`reference_pc_gtx1060`** (Windows depot before M6 prod). See `docs/PLATFORM_SUPPORT.md`.

---

## 2. Baseline profiles (summary)

| `baseline_id` | Purpose | Valid for `L3_perf_review` ship PASS? |
|---------------|---------|--------------------------------------|
| **`reference_linux_cloud`** | **Primary dev** — Cursor Cloud snapshot, Linux Steam depot | **Yes** (snapshot boot only) |
| **`reference_pc_gtx1060`** | Windows Steam depot | **Yes** |
| `steam_minimum` | Store listing floor — spot-check at M6 only | No |
| `cloud_agent_jit` | JIT VM (`build: null`) — no Godot snapshot | No |
| `ci_headless` | GitHub Actions boot/integration | No |

Full field-level spec: `game/data/qa/perf_baseline.json` → `baselines`.

---

## 3. Reference Linux — `reference_linux_cloud`

**Primary implementation OS** — Cursor Cloud Agents on `game/development` snapshot. Linux is a **v1 ship platform** because dev and runtime QA happen here.

| Component | Spec |
|-----------|------|
| **OS** | Ubuntu 22.04+ x86_64 (cloud snapshot) |
| **CPU** | 4C/8T+ cloud or desktop |
| **RAM** | 16 GB recommended |
| **GPU** | GTX 1060 class, Vulkan (Mesa or NVIDIA) |
| **Godot profile** | Same Medium preset as §4.2 (below) |

**Snapshot required:** `build` metadata must show env-build snapshot — not JIT. `docs/CLOUD_SNAPSHOT_LAUNCH.md`.

---

## 4. Reference PC — `reference_pc_gtx1060`

**Windows Steam depot** — same FPS/material targets as Linux; separate evidence file before Windows prod tag.

### 4.1 Hardware

| Component | Spec | Notes |
|-----------|------|-------|
| **OS** | Windows 10/11 64-bit | Windows Steam depot |
| **CPU** | 6-core desktop, ~2.8 GHz+ | Examples: i5-8400, Ryzen 5 2600 |
| **System RAM** | 16 GB recommended (8 GB min) | Close background apps during capture |
| **GPU** | GTX 1060 6 GB class | Examples: GTX 1060 6 GB, RX 580 8 GB |
| **VRAM** | ≥ 6 GB | 2 GB is Steam *recommended* floor, not ship target |
| **Display** | 1920×1080, 100% scaling | Single monitor |

### 4.2 Godot runtime profile (perf test — both Linux + Windows)

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

### 4.3 FPS & scene budgets

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

## 5. Steam minimum — `steam_minimum`

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

## 6. Invalid environments (do not sign off perf)

| Environment | Why invalid | Allowed use |
|-------------|-------------|-------------|
| **Cursor Cloud JIT** (`build: null`) | No snapshot Godot/MCP stack | `L2_perf_catalog`, docs on `main` |
| **GitHub Actions CI** | Headless, no GPU frame loop | L0–L2 boot, integration |
| **macOS dev** | Not v1 ship OS | Local only until v1.1 |
| **Laptop power-saving mode** | Throttled CPU/GPU | Disable for capture |

**Valid cloud perf:** `game/development` **snapshot** boot → `baseline_id: reference_linux_cloud`.

Agents must **not** mark `L3_perf_review: PASS` with `baseline_id: cloud_agent_jit`.

---

## 7. Test procedure (`L3_perf_review`)

### 7.1 When to run

See `docs/RR_CHEATSHEET.md` §Performance review — scene/shader/material/mesh/light/fog changes and post-fix regression.

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

When fixing perf-related bugs, re-run §7.2 on the affected zone **plus** `docs/QA_AND_BUG_PROCESS.md` §6 (adjacent scenes, `INT-*` if flows changed).

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
| `docs/PLATFORM_SUPPORT.md` | **Linux + Windows ship policy; cloud dev parity** |
| `docs/RENDERING_GUIDE.md` §10 | Low / Medium / High presets |
| `docs/ENVIRONMENT_KITS.md` §9 | LOD + material batching |
| `docs/RR_CHEATSHEET.md` | Performance review workflow |
| `docs/QA_AND_BUG_PROCESS.md` §6 | Post-fix regression |
| `steam/STORE_PAGE.md` | Public system requirements |
| `docs/STEAM_RELEASE_CHECKLIST.md` | M6 hardware smoke |
