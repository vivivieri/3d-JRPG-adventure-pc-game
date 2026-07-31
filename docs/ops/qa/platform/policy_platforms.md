---
id: policy-platforms
type: reference
phase: [1, 6]
audience: [release, qa, pm]
status: active
authority: qa
tokens_est: 738
summary: "Policy, platforms, dev env map"
---
# Platform Support — Policy, platforms, dev env map

**Hub:** [`PLATFORM_SUPPORT.md`](../PLATFORM_SUPPORT.md)

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

See `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md`.

---
