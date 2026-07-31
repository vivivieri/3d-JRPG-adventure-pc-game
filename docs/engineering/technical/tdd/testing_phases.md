---
id: testing-phases
type: reference
audience: [architect, builder]
phase: [1, 6]
status: active
authority: engineering
tokens_est: 406
summary: "Technical Design — Testing hooks, phase map, related — Headless boot does not replace GDAI for `.tscn` work (`MCP_STACK.md`)."
---
# Technical Design — Testing hooks, phase map, related

**Hub:** [`TECHNICAL_DESIGN.md`](../TECHNICAL_DESIGN.md)

## When to read

Use **Technical Design — Testing hooks, phase map, related** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [11. Testing hooks](#11-testing-hooks)
- [12. Phase implementation map](#12-phase-implementation-map)
- [13. Related docs (do not duplicate)](#13-related-docs-do-not-duplicate)


## 11. Testing hooks

| Layer | Tool | Validates |
|-------|------|-----------|
| L1 | `game/tests/unit/` | JSON paths, parse |
| L2 | `validate_story_data.py` | Cross-refs |
| L3 | GDAI F5 + screenshot | Visual smoke |
| L4 | Godot MCP Pro | Menu/combat scenarios |
| L5 | `run_e2e_playthrough.sh` | Three endings (Phase 6) |

Headless boot does **not** replace GDAI for `.tscn` work (`MCP_STACK.md`).

---


## 12. Phase implementation map

| TDD section | Implementation phase |
|-------------|---------------------|
| §2 autoloads (core) | Phase 2 |
| §8 exploration + ZoneVisuals | Phase 1 + 3 |
| §6 narrative | Phase 3 |
| §7 combat | Phase 4 |
| §5 save (full) | Phase 2–3 |
| §9 audio manager | Phase 2+ |
| Steam save cloud | Phase 8 |

---


## 13. Related docs (do not duplicate)

| Topic | Doc |
|-------|-----|
| Math formulas | `COMBAT_SYSTEMS.md`, `PROGRESSION_TUNING.md` |
| JSON file layout | `DATA_ARCHITECTURE.md` |
| GDScript naming | `CODE_STYLE.md` |
| Zone blockouts | `LEVEL_DESIGN.md` |
| Camera shots | `CINEMATICS.md` |
| Build order | `IMPLEMENTATION_PLAN.md` |
