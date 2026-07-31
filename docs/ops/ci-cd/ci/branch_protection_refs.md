---
id: branch-protection-refs
type: reference
phase: [6, 8]
audience: [release, qa, pm]
status: active
authority: ci-cd
tokens_est: 388
summary: "Continuous Integration — Branch protection & cross-refs — On GitHub → Settings → Branches, or via:"
---
# Continuous Integration — Branch protection & cross-refs

**Hub:** [`CI.md`](../CI.md)

## When to read

Use **Continuous Integration — Branch protection & cross-refs** (roles: release, qa, pm) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [7. Branch protection (recommended)](#7-branch-protection-recommended)
- [8. Cross-refs](#8-cross-refs)


## 7. Branch protection (recommended)

On GitHub → Settings → Branches, or via:

```bash
export GH_TOKEN=github_pat_...   # admin PAT in Cursor Secrets
bash tools/setup_github_project.sh
```

| Branch | Required status check | PR reviews |
|--------|----------------------|------------|
| `main` | **Docs + design data gates** | **None** (CI-only merge) |
| `game/development` | **L0–L2 headless gates** | **None** (CI-only merge) |

Apply to GitHub after merge:

```bash
export GH_TOKEN=github_pat_...   # admin PAT in Cursor Secrets
bash tools/setup_github_project.sh
```

---


## 8. Cross-refs

- `docs/engineering/technical/CODE_BASE_CLASS_RULES.md` — extend-only base classes + component catalog
- `docs/ops/workflow/AI_DEV_WORKFLOW.md` §2 — test layers L0–L6
- `docs/ops/qa/ACCEPTANCE_CRITERIA.md` — full gate catalog
- `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — per-role enforcement map
- `docs/ops/ci-cd/CD.md` — continuous deployment (tags on `game/development`)
- `game/data/qa/acceptance_criteria.json` — machine-readable thresholds
- `AGENTS.md` — cloud agent bootstrap (MCP stack separate from CI)
