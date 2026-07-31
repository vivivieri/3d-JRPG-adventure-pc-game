---
id: p1-03-architect-water
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 407
summary: "Phase1-Sprint1 — P1-03 water shader — covers P1-03 — Architect: water_stylized shader (parallel); Acceptance gate IDs; Spec summary; Design refs"
---
# Phase1-Sprint1 — P1-03 water shader

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## When to read

Use **Phase1-Sprint1 — P1-03 water shader** (roles: pm, architect, builder, qa) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [P1-03 — Architect: water_stylized shader (parallel)](#p1-03-architect-water_stylized-shader-parallel)
- [Acceptance gate IDs](#acceptance-gate-ids)
- [Spec summary](#spec-summary)
- [Design refs](#design-refs)
- [Definition of done](#definition-of-done)


## P1-03 — Architect: water_stylized shader (parallel)

**Title:** `[DEV][P1-03] Phase 1.4 — water_stylized.gdshader (foam + displacement)`

**Labels:** `agent/architect`, `gate/L1_unit_tests`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.4** |
| Lead agent | **architect** |
| Depends on | P1-00 |
| Parallel with | P1-02 |

### Acceptance gate IDs

```
L1_unit_tests
L1_gdscript_lint
```

### Spec summary

Draft `game/shaders/water_stylized.gdshader`:

- Stylized plane water — not fluid sim
- Gentle vertex displacement + foam edge (UV or depth-based)
- Palette: surf teal `#1A6A62` (beach), pier adjacency in village
- Matches toon family — no glossy PBR

Unit test: shader compiles headless (material create smoke if project supports).

### Design refs

- `docs/design/art/ART_DIRECTION.md` §3.6
- `docs/design/world/ENVIRONMENT_KITS.md` §3 (`beach_shoreline_water`)

### Definition of done

- [ ] Shader committed + lint clean
- [ ] Note in P1-02 for Builder to assign pier water plane when pier greybox lands

---
