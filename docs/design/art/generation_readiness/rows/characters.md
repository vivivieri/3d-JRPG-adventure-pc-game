---
id: characters
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 906
summary: "Generation Readiness — Characters & Zones — Character rows — Legend: ✅ / ⚠️ / ❌ as above."
---
# Generation Readiness — Characters & Zones — Character rows

**Hub:** [`characters_zones.md`](../characters_zones.md)

## When to read

Use **Generation Readiness — Characters & Zones — Character rows** (roles: visual, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [4. Character rows (`qa_catalog.json`)](#4-character-rows-qa_catalogjson)
- [Phase 1 — Vertical slice](#phase-1-vertical-slice)
- [Phase M5 — Party & enemies](#phase-m5-party-enemies)
- [Characters not yet in `qa_catalog.json`](#characters-not-yet-in-qa_catalogjson)
- [Crowd / cinematic NPCs (`qa_catalog.json` v1.3 — excluded from `hero_jury`)](#crowd-cinematic-npcs-qa_catalogjson-v13-excluded-from-hero_jury)


## 4. Character rows (`qa_catalog.json`)

Legend: ✅ / ⚠️ / ❌ as above.

### Phase 1 — Vertical slice

| ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Phase |
|----|-------------------|------------|---------------------------|-------|
| **urashima** | Silhouette, layers, box states, tri budget, rig attachments, `required_animations` floor, **generation brief** | Coat wind bones, portrait match | Walk cycle **duration** validation in CI; gameplay-cam face read golden shot | 1 |
| **village_torii_damaged** | Set-piece role, zone palette, tri budget, **generation brief** | Splinter detail in-engine | Golden in-scene screenshot at torii interact | 1 |
| **village_well_stone** | Prop role, save marker linkage, **generation brief** | Weathering variation | Interact highlight golden shot | 1 |
| **village_shack_roku** | Set-piece ID, hub layout, **generation brief** | Interior clutter | SC-04 emerge F5 verify | 1 |

### Phase M5 — Party & enemies

| ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Phase |
|----|-------------------|------------|---------------------------|-------|
| **yuzu** | Spirit lower-body material rule, anim list, portrait framing, **generation brief** | Float walk polish | `materialize` duration in CI | M5 |
| **roku** | Harpoon strap, anim list, **generation brief** | Taunt/guard polish | Harpoon drawn mesh variant QA | M5 |
| **salt_crab** | Enemy anim contract, **generation brief** | Pier arena dressing | Tutorial intent UI timing verify | M5 |
| **tide_wraith** | Standard enemy kit, **generation brief** | Particle drip polish | Z-fight smoke in caves | M5 |
| **shore_wraith** | Boss anims, BOSS_DESIGNS kit, **generation brief** | Phase transition VFX | Boss arena golden shot | M5 |
| **palace_sentinel** | Stats/skills, **generation brief**, **boss-standard bible row** | Hall intro VFX polish | 12 m hall scale golden shot | M5 |
| **tide_keeper_p1** | Phase materials, anim list, **generation brief** | P2/P3 GLB ship | Numerals unreadable jury check | M5 |
| **palace_gate_main** | Set-piece in hero_jury, **generation brief** | Pearl socket tune | SC-12 vertigo golden shot | M5 |
| **lacquer_box** | Item guide, glow states, **generation brief** | Ground prop SC-01 | 3-state emission screenshot | M5 |

### Characters not yet in `qa_catalog.json`

| ID | Action |
|----|--------|
| — | *(none — `otohime`, `villager_spirit`, `rebuilder` added v1.3)* |

### Crowd / cinematic NPCs (`qa_catalog.json` v1.3 — excluded from `hero_jury`)

| ID | Spec location | Ship scope |
|----|---------------|------------|
| `otohime` | `CHARACTER_BIBLE.md` §5 + `briefs/otohime.md` | Bust + portrait; SC-11, SC-17c |
| `villager_spirit` | `CHARACTER_BIBLE.md` §7 | 2 variants × 8–12 instances; SC-17a |
| `rebuilder` | `CHARACTER_BIBLE.md` §7 | 3 tool poses; SC-17b |

---
