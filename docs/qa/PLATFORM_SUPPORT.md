# Platform Support — Windows + Linux (Cloud Dev Parity)

**Version:** 1.0  
**Authority:** Resolves cloud-dev vs ship-platform mismatch  
**Machine-readable:** `game/data/qa/perf_baseline.json`  
**Cross-refs:** `docs/qa/PERFORMANCE_BASELINE.md`, `docs/agents/CLOUD_SNAPSHOT_LAUNCH.md`, `AGENTS.md`, `docs/workflow/IMPLEMENTATION_PLAN.md` Phase 8

---

## 1. Policy (read this first)

**If the primary implementation environment is Linux (Cursor Cloud Agents), Linux must be a supported ship platform.**

| Statement | Rule |
|-----------|------|
| Cloud agents run **Linux** | `install_cloud_dev.sh` installs `Godot_*_linux.x86_64` |
| GDAI + Godot editor + F5 + perf run on that OS | Scene work is **not** Windows-native in cloud |
| Windows-only ship + Linux-only dev | **Forbidden** — untestable primary workflow |
| **v1 ship targets** | **Linux + Windows** (Steam PC) |
| **macOS** | Deferred to v1.1+ (not required for cloud dev) |

**Corollary:** Cross-compiling Windows `.exe` from Linux cloud is allowed for **M6 Windows depot**, but **Linux build must be playable and perf-signed on the same cloud stack** used for daily dev.

---

## 2. Supported platforms (v1)

| Platform | Ship (Steam) | Primary dev | `L3_perf_review` baseline |
|----------|--------------|-------------|---------------------------|
| **Linux x86_64** | **Yes** — required | **Yes** — Cursor Cloud snapshot | `reference_linux_cloud` |
| **Windows x86_64** | **Yes** — required | Optional (local desktop) | `reference_pc_gtx1060` |
| **macOS** | No (v1.1+) | Optional (local desktop) | TBD |

### Why both Linux and Windows ship

| Need | Platform |
|------|----------|
| AI factory / cloud agents / CI Godot | **Linux** |
| Steam player majority (PC) | **Windows** |
| Honest perf + F5 in dev | **Linux** (same OS as cloud) |

---

## 3. Development environment map

```
┌─────────────────────────────────────────────────────────────┐
│  Cursor Cloud Agent (game/development snapshot)             │
│  OS: Linux x86_64 · Godot 4.7 · GDAI · Godotiq · MCP Pro   │
│  ✅ Build scenes · F5 · L3_perf_review (Linux baseline)     │
│  ✅ export Linux binary · export Windows .exe (cross-compile) │
└─────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
  Linux Steam depot              Windows Steam depot
  (native — dev parity)          (cross-export + Windows QA)
```

### What cloud cannot replace

| Task | Where |
|------|-------|
| Windows-only runtime bugs | Windows machine or Steam Play test |
| `reference_pc_gtx1060` perf evidence | Windows PC before Windows depot ship |
| macOS build / notarization | Mac hardware (v1.1+) |

### JIT cloud boot (`build: null`)

| Boot type | Scene/MCP work | Linux `L3_perf_review` |
|-----------|----------------|------------------------|
| **Snapshot** (`game/development`) | Required | **Valid** |
| **JIT** (`main` or failed snapshot) | Blocked | **Invalid** |

See `docs/agents/CLOUD_SNAPSHOT_LAUNCH.md`.

---

## 4. M6 deliverables (Phase 8)

| # | Item | Owner |
|---|------|-------|
| 8.1a | `tools/export_linux.sh` | Release | ✅ |
| 8.1b | `tools/export_windows.sh` | Release | ✅ |
| 8.1c | `tools/run_linux_export_smoke.sh` | QA / CI | ✅ ubuntu CI |
| 8.1d | `tools/run_windows_export_run.sh` | QA / CI | ✅ windows-latest CI |
| 8.2a | Steam **Linux** depot | Release |
| 8.2b | Steam **Windows** depot | Release |
| 8.3 | Store page — Linux + Windows requirements | PM |
| 8.4 | `L3_perf_review` per zone — **Linux** (cloud) + **Windows** (before prod) | Builder + QA |
| 8.5 | GodotSteam — `linux64` + `windows` libs | Architect |
| 8.6 | `L0_no_secrets` + `L0_ship_build_security` in CI | QA | ✅ |

**macOS:** backlog — not a blocker for cloud factory.

---

## 5. Performance sign-off matrix

| Gate | Linux evidence | Windows evidence |
|------|----------------|------------------|
| Sprint scene PR (P1+) | `baseline_id: reference_linux_cloud` on snapshot | Optional until Windows depot |
| M5 zone complete | Required | Recommended |
| M6 Steam prod tag | Required | **Required** |

Same FPS targets (60 @ 1080p Medium) on both — see `docs/qa/PERFORMANCE_BASELINE.md`.

---

## 6. FAQ

**Can we dev on Linux but ship Windows only?**  
No — that makes cloud the factory but invalidates its runtime QA. Either support Linux ship or move implementation off cloud (not planned).

**Does Linux ship mean Steam Deck?**  
Best-effort via Proton; no separate Deck verification in v1 unless added to QA matrix later.

**Is macOS required for cloud?**  
No. Cloud is Linux. macOS is a separate local/CI target for a future release.

---

## 7. Related docs

| Doc | Update |
|-----|--------|
| `docs/vision/GDD.md` §Platform | Linux + Windows |
| `docs/qa/PERFORMANCE_BASELINE.md` | `reference_linux_cloud` |
| `docs/ci-cd/STEAM_RELEASE_CHECKLIST.md` | Linux depot rows |
| `docs/qa/SECURITY.md` | Secrets + ship strip policy |
| `steam/STORE_PAGE.md` | Linux system requirements (Phase 8) |
