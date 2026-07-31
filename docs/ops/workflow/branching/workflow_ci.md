---
id: workflow-ci
type: reference
phase: [0, 1, 8]
audience: [pm, architect, builder, release]
status: active
authority: workflow
tokens_est: 347
summary: "Branching Policy — Developer workflow + CI per branch — bash tools/run_docs_ci_checks.sh"
---
# Branching Policy — Developer workflow + CI per branch

**Hub:** [`BRANCHING.md`](../BRANCHING.md)

## When to read

Use **Branching Policy — Developer workflow + CI per branch** (roles: pm, architect, builder, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [3. Workflow for developers & agents](#3-workflow-for-developers-agents)
- [4. CI per branch](#4-ci-per-branch)


## 3. Workflow for developers & agents

```bash
# Documentation or story data change
git checkout main
# edit docs/ or game/data/
bash tools/run_docs_ci_checks.sh
git commit && git push && open PR → main

# Game implementation
git checkout game/development
bash tools/ensure_mcp_stack.sh          # before scene work
# GodotPrompter + GDAI MCP build loop
bash tools/run_ci_checks.sh             # full game CI
git commit && git push                  # to game/development only
```

---


## 4. CI per branch

| Branch | CI workflow(s) | CD workflow | Environment |
|--------|----------------|-------------|-------------|
| `main` | `ci.yml` | — | **design** |
| `game/development` | `ci.yml` + `game-ci.yml` + `qa-nightly.yml` | `cd-artifact.yml` · `cd-steam.yml` | **dev** / **qa** / **uat** / **preprod** / **prod** |

See `docs/ops/ci-cd/ENVIRONMENTS.md` for promotion rules (dev → qa → uat → preprod → prod).

---
