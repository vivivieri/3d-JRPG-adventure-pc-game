---
id: reference-machines
type: reference
phase: [1, 6]
audience: [qa, builder, release]
status: active
authority: qa
tokens_est: 976
summary: "Cloud/PC/Steam/invalid envs"
---
# Performance Baseline — Cloud/PC/Steam/invalid envs

**Hub:** [`PERFORMANCE_BASELINE.md`](../PERFORMANCE_BASELINE.md)

## 3. Reference Linux — `reference_linux_cloud`

**Primary implementation OS** — Cursor Cloud Agents on `game/development` snapshot. Linux is a **v1 ship platform** because dev and runtime QA happen here.

| Component | Spec |
|-----------|------|
| **OS** | Ubuntu 22.04+ x86_64 (cloud snapshot) |
| **CPU** | 4C/8T+ cloud or desktop |
| **RAM** | 16 GB recommended |
| **GPU** | GTX 1060 class, Vulkan (Mesa or NVIDIA) |
| **Godot profile** | Same Medium preset as §4.2 (below) |

**Snapshot required:** `build` metadata must show env-build snapshot — not JIT. `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md`.

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
| Godot | **4.7** stable | `docs/engineering/technical/TECH_STACK.md` |
| Renderer | **Forward+** | `project.godot` |
| **Graphics quality** | **Medium** | `docs/design/art/RENDERING_GUIDE.md` §10 |
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
