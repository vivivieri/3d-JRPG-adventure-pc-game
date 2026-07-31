---
id: branch-protection-refs
type: reference
audience: [release, qa, pm]
status: active
authority: ci-cd
tokens_est: 400
summary: "Branch protection & cross-refs"
---
# Continuous Integration — Branch protection & cross-refs

**Hub:** [`CI.md`](../CI.md)

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
