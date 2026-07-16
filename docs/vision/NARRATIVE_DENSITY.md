# Narrative Density — Optimized Application Guide

**Version:** 1.0  
**Audience:** Writers, combat designers, data authors  
**Cross-refs:** `docs/vision/NARRATIVE_WRITING_GUIDE.md` §12, `game/data/narrative/narrative_density.json`, `tools/validate_narrative_density.py`

**Goal:** Apply JRPG narrative steals **once per zone / once per act** — not on every node. Ship gate enforces caps automatically.

---

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

## 3. Ship budgets (enforced)

Source of truth: `game/data/narrative/narrative_density.json`

| Pattern | Budget | Notes |
|---------|--------|-------|
| **Boss barks** | Required on `boss` + `elite` tiers | Intent + emotional facet |
| **Field barks** | Max 6 enemies total | `salt_crab` = skills only, no `battle_start` |
| **Field battle_start** | Allowlist: `tide_wraith` only | Guilt echo for pool fights |
| **Quiet beats** | Act I≤2, II≤4, III≤2, total≤6 | `narrator` + `emotion: quiet` |
| **Inspect scenes** | ≥2 narrator lines before PC; ≤6 lines total | Per zone caps in JSON |
| **Flag callbacks** | ≤2 lines/scene; ≤3 uses/flag | Priority: sandal, banner, box truth, well |
| **subtext_warm** | SC-16 only; ≤2 warm variants | `mirror_choice` flavor |

### Zone caps

| Zone | Max inspect | Max quiet beats |
|------|-------------|-----------------|
| `beach_shore` | 2 | 2 |
| `ruined_village` | 4 | 1 |
| `tidal_caves` | 1 | 4 |
| `dragon_palace_gate` | 0 | 2 |

---

## 4. What “optimized full pass” looks like (v1 ship)

| Layer | Coverage | Stop here |
|-------|----------|-----------|
| All 4 zones | One pattern touch each | ✓ Done |
| All bosses | Full `combat_barks` | ✓ Done |
| Field mobs | 1–2 types only | ✓ `salt_crab`, `tide_wraith` |
| Hub inspect | Village + 1 beach | ✓ Done |
| Callbacks | 3–4 high-value flags | ✓ Done |
| Optional fights | No extra barks | Do not add |
| Lore journal | Separate system | Use `lore_entries.json`, not dialogue spam |

---

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
