---
id: summary-why
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 483
summary: "Summary & why hybrid"
---
# Agile Within Phases — Summary & why hybrid

**Hub:** [`AGILE_WITHIN_PHASES.md`](../AGILE_WITHIN_PHASES.md)

## 1. Summary

| Layer | Style | Tool | Changes when? |
|-------|-------|------|----------------|
| **Roadmap** | Waterfall | `IMPLEMENTATION_PLAN.md` Phases 0–8 | Major milestone only |
| **Scope** | Fixed (GDD + `game/data/`) | `docs/` + JSON | Data PRs to `main` |
| **Sprint execution** | Agile | **Linear** cycles (optional) + GitHub Issues | Per agent batch (§12.1); ≤1 week calendar ceiling |
| **Task delivery** | Agile | Multi-agent handoffs | Daily / per session |
| **Quality** | Gated | CI + acceptance criteria | Every commit / phase exit |
| **Release** | Staged waterfall | UAT → preprod → prod | RC / beta / ship tags |

**Rule:** Sprints optimize **how** we build the current phase. They do **not** reorder phases (e.g. M5 art still follows Phase 7; Steam still Phase 8).

---


## 2. Why not full Agile or full Waterfall?

### Full waterfall would mean

- No CI until phase end
- No playtest until ship
- No iteration within a zone

**We reject that** — CI runs every push; vertical slice (SC-02) comes first; remediation loops exist.

### Full Agile would mean

- Emergent story design in sprints
- Ship MVP with one ending, discover the rest
- Art and gameplay co-evolve from sprint 1

**We reject that for this project** — 3 endings, fixed scene IDs, and M5 art rebuild are planned upfront (`GDD.md`, `story/scenes.json`).

### Phase-gated Agile (this project)

```
[ Phase N scope frozen from IMPLEMENTATION_PLAN ]
        │
        ├── Sprint A ──► issues ──► agents ──► CI
        ├── Sprint B ──► issues ──► agents ──► CI
        └── Sprint C ──► phase exit gates ──► tag RC (optional UAT)
        │
[ Phase N+1 only after phase gates PASS ]
```

---
