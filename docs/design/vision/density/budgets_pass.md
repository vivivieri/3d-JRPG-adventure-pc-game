---
id: budgets-pass
type: reference
phase: [1, 6]
audience: [narrative]
status: active
authority: vision
tokens_est: 504
summary: "Narrative Density — Ship budgets + optimized pass — Source of truth: `game/data/narrative/narrative_density.json"
---
# Narrative Density — Ship budgets + optimized pass

**Hub:** [`NARRATIVE_DENSITY.md`](../NARRATIVE_DENSITY.md)

## When to read

Use **Narrative Density — Ship budgets + optimized pass** (roles: narrative) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [3. Ship budgets (enforced)](#3-ship-budgets-enforced)
- [Zone caps](#zone-caps)
- [4. What “optimized full pass” looks like (v1 ship)](#4-what-optimized-full-pass-looks-like-v1-ship)


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
