---
id: coverage-review
type: how-to
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 547
summary: "This plan was audited against `TECHNICAL_DESIGN.md`, `MILESTONES.md`, and `AI_DEV_WORKFLOW.md`. The following were **missing** from earlier versions and are now"
---
# Implementation Plan — Coverage review

**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)

## Coverage review (gaps closed in v1.2)

This plan was audited against `TECHNICAL_DESIGN.md`, `MILESTONES.md`, and `AI_DEV_WORKFLOW.md`. The following were **missing** from earlier versions and are now scheduled:

| Gap | Where added |
|-----|-------------|
| `VoiceLinePlayer` runtime (paths + BGM duck) | Phase 3.2 |
| VO clip **generation** (ElevenLabs batch) | Phase 7.7–7.9 |
| `AudioManager` shell (procedural audio during greybox) | Phase 2.7 |
| Settings menu (language + `vo_dialect` + volumes) | Phase 2.8 |
| SC-00 prologue + `CinematicDirector` | Phase 3.7 |
| Shop + inventory UI | Phase 3.5–3.6 |
| Written `zh-Hant` in `game/data/` + `translations.csv` | Done — expand CSV for skills/combat in Phase 3 |
| SC-08 / SC-11 / SC-12 / SC-13 story beats | Phases 5.3, 6.1–6.2 |
| SFX/ambient production | Phase 7.6 |
| Steam achievements + store assets | Phase 8.4–8.5 |
| E2E three-endings gate | Phase 6.7 |
| Golden zone gameplay screenshots (`GR-001`) | Phase 1.10, 7.12 |
| `palace_sentinel` bible boss-standard row (`GR-002`) | Phase 6.3b (before Phase 7.1 enemy meshes) |
| Zone composition strict smoke (`GR-003`) | Phase 1.11 warn → Phase 7.12 strict at M5 ship |
| Audio QA catalog + hero BGM briefs (`GR-004`) | Phase 7.5, 7.9 — `audio_qa_catalog.json`, `docs/briefs/audio/` |
| P0 VO generation briefs + jury (`GR-005`) | Phase 7.7–7.9 — `docs/briefs/vo/`, `L2_vo_technical`, `L2_vo_jury` |
| Scene audio map (`GR-006`) | Phase 7.5–7.6 — `scene_audio_map.json` |

**Traceability:** `game/data/qa/generation_readiness_backlog.json` — machine-readable **GR-*** items linked to plan tasks and gate IDs.

**Still deferred (intentional):** full dialogue VO (12 selective clips only per `VO_HIT_LIST.md`); human L6 playtest until Phase 8 after L0–L5 pass.

---

