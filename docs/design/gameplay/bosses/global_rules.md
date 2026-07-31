---
id: global-rules
type: reference
audience: [builder, builder_combat, qa]
phase: [2]
status: active
authority: gameplay
tokens_est: 620
summary: "Borrowed from **Ni no Kuni** (grief externalized), **Persona** (harm as felt experience), **XC3 / Expedition 33** (bonds under inevitability). Bosses are **name"
---
# Boss Designs — Global boss rules

**Hub:** [`BOSS_DESIGNS.md`](../BOSS_DESIGNS.md)

## When to read

Use **Boss Designs — Global boss rules** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [1. Global boss rules](#1-global-boss-rules)
- [Bosses as emotional facets (v1 — not “evil for evil”)](#bosses-as-emotional-facets-v1-not-evil-for-evil)
- [Intent icon mapping](#intent-icon-mapping)


## 1. Global boss rules

| Rule | Detail |
|------|--------|
| Intent UI | Every non-basic action telegraphed 1 turn ahead (icon + label) |
| Phases | HP threshold triggers; banner + short animation |
| Adds | Max 1 add on field for v1 (performance + readability) |
| Escape | Disabled for all bosses |
| Normal mode | Story completable without grinding |
| Hard mode | Optional; faster patterns, less intent delay (post-normal unlock or menu toggle) |
| Limit gauge | Fills on damage dealt/taken; boss fights teach by SC-09 |

### Bosses as emotional facets (v1 — not “evil for evil”)

Borrowed from **Ni no Kuni** (grief externalized), **Persona** (harm as felt experience), **XC3 / Expedition 33** (bonds under inevitability). Bosses are **named feelings** made fightable — not cartoon villains.

| Boss | Emotional facet | What the fight *means* | Writer rule |
|------|-----------------|------------------------|-------------|
| **Shore Wraith** | Collective **guilt** | Faces under the cloth = villagers Urashima abandoned | Barks accuse, don't taunt; defeat = release, not victory lap |
| **Palace Sentinel** | **Duty frozen** | Oath of stillness — paradise that forbids change | Minimal dialogue; armor speaks; Yuzu's Spirit pierces rigidity |
| **Tide Keeper** | **Temptation to erase pain** | Time offers paradise at cost of the living world | Speaks in tides/clock motifs, not essays; phase 3 shrinks — tragic, not monstrous |

**Combat UI:** Intent label + one bark line should reinforce the facet (see intent table above).
**Defeat lines:** Tragic, not *"You win!"* — `NARRATIVE_WRITING_GUIDE.md` §11.E.

**Do not add:** Mid-fight lore dumps, moral scoring, or a fourth “secret” boss ending.

### Intent icon mapping

| Icon | Meaning |
|------|---------|
| Sword | Physical attack |
| Skull | High damage / debuff |
| Shield | Defensive buff |
| Sparkles | Spirit / magic |
| Waves | Water AoE |
| Clock | Time manipulation (Tide Keeper only) |

---
