---
id: m6-perf-faq
type: reference
phase: [1, 6]
audience: [release, qa, pm]
status: active
authority: qa
tokens_est: 573
summary: "M6 deliverables, perf matrix, FAQ, related"
---
# Platform Support — M6 deliverables, perf matrix, FAQ, related

**Hub:** [`PLATFORM_SUPPORT.md`](../PLATFORM_SUPPORT.md)

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

Same FPS targets (60 @ 1080p Medium) on both — see `docs/ops/qa/PERFORMANCE_BASELINE.md`.

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
| `docs/design/vision/GDD.md` §Platform | Linux + Windows |
| `docs/ops/qa/PERFORMANCE_BASELINE.md` | `reference_linux_cloud` |
| `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` | Linux depot rows |
| `docs/ops/qa/SECURITY.md` | Secrets + ship strip policy |
| `steam/STORE_PAGE.md` | Linux system requirements (Phase 8) |
