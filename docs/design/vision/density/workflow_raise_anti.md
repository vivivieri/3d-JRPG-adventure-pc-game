---
id: workflow-raise-anti
type: reference
phase: [1, 6]
audience: [narrative]
status: active
authority: vision
tokens_est: 383
summary: "Narrative Density — Workflow, raise budget, anti-patterns — covers 5. Workflow for new content; 6. When to raise a budget; 7. Anti-patterns (never ship)"
---
# Narrative Density — Workflow, raise budget, anti-patterns

**Hub:** [`NARRATIVE_DENSITY.md`](../NARRATIVE_DENSITY.md)

## When to read

Use **Narrative Density — Workflow, raise budget, anti-patterns** (roles: narrative) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [5. Workflow for new content](#5-workflow-for-new-content)
- [6. When to raise a budget](#6-when-to-raise-a-budget)
- [7. Anti-patterns (never ship)](#7-anti-patterns-never-ship)


## 5. Workflow for new content

1. **Draft** line in `chapter_01.json` or `enemies.json`
2. **Run** `python3 tools/validate_story_data.py` (schema)
3. **Run** `python3 tools/validate_narrative_density.py` (budget)
4. **If FAIL** — remove or swap an existing line in the same category; do not raise caps without design review

```bash
python3 tools/validate_story_data.py
python3 tools/validate_narrative_density.py   # L0_narrative_density
```

---


## 6. When to raise a budget

Only if **scope changes** (e.g. 4+ hour epilogue DLC). Otherwise:

- New boss → use existing boss bark slots (replace, don't stack)
- New zone → add row to `narrative_density.json` `zones` + bump one cap
- New flag callback → retire a lower-priority callback elsewhere

---


## 7. Anti-patterns (never ship)

- `battle_start` on tutorial `salt_crab`
- Third quiet beat in Act I
- Fourth callback line in SC-14 / SC-15
- `subtext_warm` outside SC-16
- Morality labels or “true ending” copy (`ENDING_DESIGN.md`)
