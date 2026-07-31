---
id: create-branch-refs
type: reference
phase: [0, 1, 8]
audience: [pm, architect, builder, release]
status: active
authority: workflow
tokens_est: 384
summary: "Branching Policy — Creating game branch + cross-refs — git checkout -b game/development   # from last main snapshot with full game tree"
---
# Branching Policy — Creating game branch + cross-refs

**Hub:** [`BRANCHING.md`](../BRANCHING.md)

## When to read

Use **Branching Policy — Creating game branch + cross-refs** (roles: pm, architect, builder, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [5. Creating the game branch (one-time)](#5-creating-the-game-branch-one-time)
- [6. Cross-refs](#6-cross-refs)


## 5. Creating the game branch (one-time)

Already done:

```bash
git checkout -b game/development   # from last main snapshot with full game tree
git push -u origin game/development
```

New clones:

```bash
git clone <repo>
git checkout game/development   # for implementation
git checkout main               # for docs/data only
```

---


## 6. Cross-refs

- `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md` — **end-to-end lifecycle hub** (phases, sprints, env promotion, agents)
- `docs/ops/workflow/BRANCHING_DECISION_RECORD.md` — ADR: trunk + tags vs env branches + forks
- `docs/ops/workflow/IMPLEMENTATION_PLAN.md` — build phases (executed on `game/development`)
- `docs/ops/agents/MULTI_AGENT_BRANCH_STRATEGY.md` — per-issue `cursor/*` branches
- `docs/ops/ci-cd/ENVIRONMENTS.md` — dev · qa · uat · preprod · prod (logical stages, not git branches)
- `docs/ops/ci-cd/CI.md` — full game CI gate catalog
- `AGENTS.md` — agent bootstrap; design source on `main`, build on `game/development`
- `.cursorrules` §0 — GDAI MCP scene policy (applies on `game/development`)
