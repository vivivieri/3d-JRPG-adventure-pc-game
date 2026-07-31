---
id: industry-map
type: how-to
phase: [1, 6]
audience: [qa, pm]
status: active
authority: qa
tokens_est: 962
summary: "Industry standards map"
---
# Remediation — Standards & Loop — Industry standards map

**Hub:** [`standards_loop.md`](../standards_loop.md)

## 1. Industry standards we map to

We do not ship a AAA art/audio department. These are the **industry practices** our automated gates approximate — use them when arguing *what* to fix, not *whether* to skip QA.

### 3D models & environment art

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **Production phases** (blockout → greybox → beauty → polish) | Each phase has different DoD; you do not polish a blockout | `MODEL_QA.md` rejects blockouts at beauty phase; Kenney = greybox only |
| **Technical art review (TAR) gate** | Mesh budget, UVs, pivots, naming before engine import | `check_model_technical.py` + `qa_catalog.json` tri budgets |
| **Art bible / silhouette sign-off** | Readable shape at gameplay distance before texture | Turntable jury M4 + `CHARACTER_BIBLE.md` |
| **glTF 2.0 interchange** (Khronos) | Engine-neutral asset validation | GLB parse in `model_qa_lib.py` |
| **LOD authoring** (when applicable) | Distance-based mesh swap | Future; v1 uses single hero LOD per `CHARACTER_BIBLE.md` budgets |

**References:** GDC art pipeline talks (phase gating); Khronos [glTF 2.0 spec](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html); standard game art DoD checklists (poly count, texel density, pivot at feet).

### Visual polish & look-dev

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **Golden master / visual regression** | Committed reference image; CI fails on drift | `compare_screenshots` + `artifacts/screenshots/*_golden.png` (`VISUAL_QA.md` §2F) |
| **Color script / palette lock** | Zone mood locked before final lighting | `ART_DIRECTION.md` §1 + `palette_remap.py` + `check_screenshot_palette.py` |
| **Art direction compliance review** | Bible checklist, not “looks fine to me” | Vision jury V1–V6 + zone rows in `ENVIRONMENT_KITS.md` |
| **Look-dev iteration** | Change **one** lighting/material variable per pass | Remediation lever `lighting` vs `albedo` vs `mesh` — never all at once |

**References:** Visual regression tools (Percy, Chromatic, Applitools — same *golden diff* pattern); film color-script workflow adapted to games.

### Audio polish & mastering

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **ITU-R BS.1770 / EBU R128** loudness metering | Integrated LUFS + true peak limits | `check_audio_technical.py` per-bus targets |
| **Platform loudness guidance** | Music ~−14 to −20 LUFS integrated (streaming/game) | BGM target −16 ± 4 LU (`AUDIO_QA.md`) |
| **Stem / bus mastering** | Music, SFX, VO on separate buses before final mix | `AUDIO_PRODUCTION_GUIDE.md` bus layout |
| **Loop seam QA** | 10+ min in-engine listen for clicks | Human L6; technical duration/range in A2 |
| **Reference track A/B** | Compare mood against locked brief | ACE-Step prompts in `ace_step_prompts.json` + audio jury |

**References:** [EBU R 128](https://tech.ebu.ch/loudness); ITU-R BS.1770; AES game audio loudness guidance; iZotope/FFmpeg `loudnorm` workflow.

### General QA iteration (any medium)

| Practice | Application here |
|----------|------------------|
| **PDCA / build-measure-learn** | FAIL → brief → one lever change → re-measure |
| **Root cause vs symptom** | “Too dark” may be exposure, not albedo — classify before regenerating |
| **Versioned artifacts** | `revision_log.json` per asset; never overwrite without attempt number |
| **Escalation tier** | Attempt 3+ → different tool tier or human L6, not attempt 4 of same prompt |

---
