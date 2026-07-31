---
id: implementation-plan
type: how-to
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 669
summary: "open the phase pack for the active sprint; do not preload all phases."
---
# Tides of Urashima — Implementation Plan

**Hub** — open the phase pack for the active sprint; do not preload all phases.

| Pack | Topic |
|------|-------|
| [`phase_0.md`](implementation/phase_0.md) | Phase 0 |
| [`phase_1.md`](implementation/phase_1.md) | Phase 1 |
| [`phase_2.md`](implementation/phase_2.md) | Phase 2 |
| [`phase_3.md`](implementation/phase_3.md) | Phase 3 |
| [`phase_4.md`](implementation/phase_4.md) | Phase 4 |
| [`phase_5.md`](implementation/phase_5.md) | Phase 5 |
| [`phase_6.md`](implementation/phase_6.md) | Phase 6 |
| [`phase_7.md`](implementation/phase_7.md) | Phase 7 |
| [`phase_8.md`](implementation/phase_8.md) | Phase 8 |
| [`zone_build_order.md`](implementation/zone_build_order.md) | Zone build order |
| [`validation_commands.md`](implementation/validation_commands.md) | Validation commands |
| [`coverage_review.md`](implementation/coverage_review.md) | Coverage review |
# Tides of Urashima — Implementation Plan

**Version:** 1.2 (Fresh rebuild)
**Branch:** `main` (documentation + `game/data/` only) · **`game/development`** (Godot implementation)
**Source of truth:** `main` design docs + `game/data/` JSON + `game/data/code/*_registry.json`
**Spec-first:** See `docs/engineering/technical/SPEC_FIRST_DEVELOPMENT.md` — no ship `.gd`/`.tscn` on `main`; build on `game/development` after `SPEC_DEV_START`.
**Workflow:** GodotPrompter + full MCP toolchain — see `docs/ops/agents/MCP_STACK.md`.
**Milestone checklist:** `docs/ops/workflow/MILESTONES.md` (M5 art → M6 Steam).

Previous full implementation on `main` was **stripped** (boot shell + data only). Phases 1–6 rebuild from documentation via GDAI MCP on **`game/development`**.

**All Phase 1–8 implementation work happens on `game/development`.** Do not merge to `main` until M6 ship-ready.

**Sprint execution:** Phase-gated Agile — 2-week Linear cycles inside each phase (`docs/ops/workflow/AGILE_WITHIN_PHASES.md`, `game/data/qa/sprint_phases.json`).

### Phase ↔ milestone map

| Phase | Milestone | Focus |
|-------|-----------|-------|
| 0 | M0, M0c–M0h | Dev environment + design/data baseline ✅ |
| 1 | — | Environment foundation + SC-02 vertical slice gate |
| 2–3 | M1 | Core systems + narrative exploration |
| 4 | M2 | Combat vertical slice |
| 5 | M3 | Chapter 1 dungeons |
| 6 | M4 | Full story + three endings |
| 7 | **M5** | Art rebuild (NPR zones, hero meshes, curated audio) |
| 8 | **M6** | Steam export, compliance, playtest |

---
