---
id: antipatterns-pr
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 276
summary: "Bash Style — Anti-patterns + PR checklist — covers 8. Anti-patterns; 9. PR checklist (shell)"
---
# Bash Style — Anti-patterns + PR checklist

**Hub:** [`BASH_STYLE.md`](../BASH_STYLE.md)

## When to read

Use **Bash Style — Anti-patterns + PR checklist** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [8. Anti-patterns](#8-anti-patterns)
- [9. PR checklist (shell)](#9-pr-checklist-shell)


## 8. Anti-patterns

| Don't | Why |
|-------|-----|
| `set +e` without comment | Hides failures |
| Unquoted `$var` | Word splitting / glob bugs |
| `eval` on user input | Injection risk |
| Hardcoded `/workspace` only paths | Use `ROOT` |
| Duplicate gate IDs in runner | `check_doc_sync.py` fails CI |
| Long business logic in bash | Implement in `tools/*.py` |

---


## 9. PR checklist (shell)

- [ ] `#!/usr/bin/env bash` + `set -euo pipefail`
- [ ] `ROOT` resolution matches other scripts
- [ ] Quoted variable expansions
- [ ] New gate ID registered in `acceptance_criteria.json`
- [ ] `python3 tools/check_doc_sync.py` if runner changed
- [ ] `bash tools/check_shell_scripts.sh` green
