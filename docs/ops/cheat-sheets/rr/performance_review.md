---
id: performance-review
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 567
summary: "[`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)"
---
# R&R — performance-review-required

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## Performance review (required — not code review)

**Policy:** Every scene/visual change gets a **lightweight performance re-check**, not a heavy code review. Measure runtime; do not debate style.

**Baseline:** Ship perf on **`reference_linux_cloud`** (cloud snapshot / Linux) + **`reference_pc_gtx1060`** (Windows). Linux ship is **required** — cloud dev OS. See **`docs/ops/qa/PLATFORM_SUPPORT.md`**, **`docs/ops/qa/PERFORMANCE_BASELINE.md`**, `game/data/qa/perf_baseline.json`. JIT cloud (`build: null`) is invalid for FPS sign-off.

### When required

| Trigger | Who runs | Gate |
|---------|----------|------|
| New/changed zone scene, material, shader, mesh, light, fog | **Builder** after F5 | `L3_perf_review` |
| Bug fix in gameplay scene or rendering | **Builder** or **QA** on verify | `L3_perf_review` + post-fix regression |
| Docs/data-only PR | — | Skip |

### What to measure (thresholds in `game/data/qa/perf_thresholds.json`)

| Metric | Target / investigate |
|--------|----------------------|
| FPS @ 1080p (gameplay cam) | **≥ 60** target (GTX 1060 ref); **< 30** = investigate |
| Materials visible per view | **≤ 8** per zone |
| Draw calls | **> 1000** = investigate batching/instancing |
| Node count / memory | Steady growth during 30s walk = leak |

### How to run (agent-local)

```bash
# 1. F5 in affected zone (GDAI MCP or Godot editor)
# 2. Godotiq — game must be running
godotiq_perf_snapshot(detail="normal")
# 3. Save JSON evidence (baseline_id required — see docs/ops/qa/PERFORMANCE_BASELINE.md §7)
# artifacts/perf_reviews/<zone>_<short_sha>.json
```

**CI catalog (always):** `bash tools/run_perf_review_checks.sh` → `L2_perf_catalog`

### Post-fix regression (with perf)

When fixing a bug, re-run per `docs/ops/qa/QA_AND_BUG_PROCESS.md` §6:

1. Original repro steps
2. One scene before and after the affected scene
3. **`L3_perf_review`** if fix touched scenes/shaders/materials
4. Affected **`INT-*`** integration scenario when flows changed

**Invalid PASS:** F5 clean but no perf snapshot on a scene PR · FPS below target with no remediation brief · merging without re-running affected `INT-*` after a fix.

---

