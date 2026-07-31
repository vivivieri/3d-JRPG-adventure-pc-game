---
id: why-profiles
type: reference
phase: [1, 6]
audience: [qa, builder, release]
status: active
authority: qa
tokens_est: 415
summary: "Why + profile summary"
---
# Performance Baseline — Why + profile summary

**Hub:** [`PERFORMANCE_BASELINE.md`](../PERFORMANCE_BASELINE.md)

## 1. Why this exists

| Problem | Baseline solves |
|---------|-----------------|
| Cloud agent reports 45 FPS on unknown GPU | JIT boot invalid; **snapshot Linux** valid with `reference_linux_cloud` |
| Editor F5 vs exported `.exe` differ | Doc states which is authoritative per gate |
| Steam minimum vs recommended blur together | Two profiles: **reference** (ship) vs **minimum** (support floor) |
| Perf review has no CPU/RAM fields | Evidence schema requires hardware capture when available |

**Policy:** `L3_perf_review` PASS requires evidence on a **ship baseline** — **`reference_linux_cloud`** (cloud snapshot / Linux depot) and **`reference_pc_gtx1060`** (Windows depot before M6 prod). See `docs/ops/qa/PLATFORM_SUPPORT.md`.

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
