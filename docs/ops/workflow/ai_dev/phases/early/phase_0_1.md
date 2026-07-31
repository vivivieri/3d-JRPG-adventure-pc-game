---
id: phase-0-1
type: reference
audience: [pm, qa, architect]
status: active
authority: workflow
tokens_est: 605
summary: "AI Dev — Phases 0–1 — Task numbers match `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase 1 (not a separate numbering scheme)."
---
# AI Dev — Phases 0–1

**Hub:** [`phase_acceptance.md`](../../phase_acceptance.md)

## When to read

Use **AI Dev — Phases 0–1** (roles: pm, qa, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [Phase 0 — Dev environment ✅ (baseline)](#phase-0-dev-environment-baseline)
- [Phase 1 — Environment foundation](#phase-1-environment-foundation)


### Phase 0 — Dev environment ✅ (baseline)

| # | Criterion | Verification |
|---|-----------|--------------|
| 0.1 | `bash tools/ensure_gdai_mcp.sh` succeeds | Script exit 0; HTTP `:3571` returns tools |
| 0.2 | `python3 tools/validate_story_data.py` passes | Exit 0 |
| 0.3 | `bash tools/run_unit_tests.sh` passes | Exit 0; all registered tests green |
| 0.4 | `bash tools/run_playtest_smoke.sh` passes | Exit 0 |
| 0.5 | F5 boot screen loads; no missing-data errors in Output | GDAI MCP F5 |
| 0.6 | `.cursorrules` §0 and this doc linked from `README.md` | File review |



### Phase 1 — Environment foundation

**Task numbers match `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase 1** (not a separate numbering scheme).

| # | Criterion | Verification |
|---|-----------|--------------|
| 1.1 | `environments/*.tres` — WorldEnvironment per zone (tonemap, fog, glow) | GDAI + `RENDERING_GUIDE.md` |
| 1.2 | `zone_visuals.gd` applies palette, sky, lights at runtime | Unit test + GDAI F5 |
| 1.3 | `toon_base.gdshader` on ground meshes; single ramp family | GDAI viewport |
| 1.4 | `water_stylized.gdshader` — foam + gentle displacement | Shader compiles headless |
| 1.5 | Greybox zone scenes (Sprint1: `ruined_village`; Sprint2: beach/caves/palace) | Integration / headless load |
| 1.6 | DirectionalLight + fog values match zone table | GDAI inspector readback |
| 1.7 | ProceduralSky (no HDRI) per `RENDERING_GUIDE.md` §4 | GDAI viewport |
| 1.8 | Component scenes from `LEVEL_DESIGN.md` §1b (Phase1-Sprint2) | GDAI `.tscn` + L3 |
| 1.9 | **Vertical slice gate:** SC-02 Ruined Village passes `ART_DIRECTION.md` §10 greybox checklist | GDAI F5 + L3 |
| 1.10 | **Golden screenshot** — `phase1_ruined_village_gameplay.png` (**GR-001**) | GDAI capture |
| 1.11 | Zone composition smoke (warn) — `run_zone_composition_checks.sh` (**GR-003**) | Exit 0 warn until M5 strict |
| — | L0 + L1 + L2 + L3 pass after every commit on `game/development` | `bash tools/run_ci_checks.sh` |
