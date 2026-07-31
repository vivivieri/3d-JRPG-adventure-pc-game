---
id: problem-tree
type: reference
phase: [1, 6]
audience: [narrative]
status: active
authority: vision
tokens_est: 377
summary: "Narrative Density — Problem + decision tree — This game targets 2–3 hours. Density beats coverage."
---
# Narrative Density — Problem + decision tree

**Hub:** [`NARRATIVE_DENSITY.md`](../NARRATIVE_DENSITY.md)

## When to read

Use **Narrative Density — Problem + decision tree** (roles: narrative) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. The problem](#1-the-problem)
- [2. Decision tree (add a line?)](#2-decision-tree-add-a-line)


## 1. The problem

| Over-apply | Symptom |
|------------|---------|
| Bark every skill every turn | Combat UI becomes unreadable |
| Life line on every prop | Player stops reading inspect text |
| Quiet beat every scene | Silence loses weight |
| Callback every flag | Feels like checklist homework |

This game targets **2–3 hours**. Density beats coverage.

---


## 2. Decision tree (add a line?)

```
New narrative line proposed
        │
        ▼
Does environment/camera already carry the emotion?
   YES ──► SKIP (prefer visual storytelling)
   NO
        │
        ▼
Which pattern is it?
   ├─ Combat bark ──► Boss/elite required; field mob only if guilt/theme needs it
   ├─ Hub inspect ──► Max 1 village-life line BEFORE PC speaks; 2 narrator lines total env+life
   ├─ Quiet beat ──► Max 1 per act (Act II allows up to 4 — caves/palace approach)
   ├─ Flag callback ──► Max 2 lines per scene; max 3 scenes per flag
   └─ Choice flavor ──► SC-16 subtext_warm only; mirror_choice open/break
        │
        ▼
Run: python3 tools/validate_narrative_density.py
```

---
