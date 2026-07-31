---
id: what-stack-data
type: how-to
phase: [1, 6]
audience: [pm, visual, builder]
status: active
authority: qa
tokens_est: 476
summary: "What it is, stack position, data files"
---
# Candidate Tournament — What it is, stack position, data files

**Hub:** [`CANDIDATE_TOURNAMENT.md`](../CANDIDATE_TOURNAMENT.md)

## 1. What this is (and is not)

| This **is** | This **is not** |
|-------------|-----------------|
| Industry **champion/challenger** for generation | A second ship QA stack |
| **Golden harness** — same screenshots, palette, gates every compare | Building the game N times and Frankenstein-merging |
| Optional **upstream picker** before merge | Replacement for L0–L6 |
| One **canonical winner** per scope (zone/issue) | Multiple living forks on `game/development` |

**Ship truth stays L0–L6.** `L2_candidate_select` never blocks `main` docs CI or M6 ship by itself.

---


## 2. Stack position

```
Spec + sprint issue
        │
        ▼
┌───────────────────────────┐
│  L2.5 Candidate tournament │  ← THIS (optional, max 3 tries/issue)
│  golden harness + rubric   │
└─────────────┬─────────────┘
              │ ONE winner commit
              ▼
┌───────────────────────────┐
│  L0 → L1 → L2 → L3 → L4 → L5 │  ← unchanged mandatory spine
└─────────────┬─────────────┘
              ▼
         L6 human (RC only)
```

---


## 3. Data files

| File | Role |
|------|------|
| `game/data/qa/golden_harness.json` | Per-scope capture paths, palette zone keys, hard gate veto list |
| `game/data/qa/evaluation_rubrics.json` | Soft rubric axes (tie-break only) mapped to jury criteria |
| `game/data/qa/candidate_tournament_policy.json` | Max candidates, non-ship flag, registry paths |
| `artifacts/candidates/champion_registry.json` | Current champion per scope (runtime, gitignored except samples) |
| `artifacts/candidates/<issue>/comparison_*.json` | Comparison evidence for PM / stakeholder |

---
