---
id: characters-zones
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 1132
summary: "Character + zone readiness rows"
---
# Generation Readiness — Character + zone readiness rows

**Hub:** [`GENERATION_READINESS.md`](../GENERATION_READINESS.md)

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


## 5. Zone rows (`ENVIRONMENT_KITS.md`)

| Zone ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Build phase |
|---------|-------------------|------------|---------------------------|-------------|
| **beach_shore** (SC-01) | Mood, palette, kit table, spawn path, **generation brief** | Water foam polish | Golden screenshot capture | 2 |
| **ruined_village** (SC-02 hub) | Full kit + layout + lighting + **generation brief** | Pier submerge depth | Golden screenshot + `L2_visual_jury` PASS | **1** |
| **tidal_caves** (SC-06–10) | Biolume palette, modular kit, **generation brief** | Face decal polish | Puzzle state screenshots | 5 |
| **dragon_palace_gate** (SC-12+) | Palace void sky, gold trim, **generation brief** | Mirror chamber polish | SC-12 vertigo golden shot | 6 |

### Per-zone composition contract (to add to `ENVIRONMENT_KITS.md` or `game/data/qa/zone_composition.json`)

| Field | Example (`ruined_village`) | Why humans care |
|-------|---------------------------|-----------------|
| `min_path_width_m` | 2.0 | No stuck on geometry |
| `max_props_per_100m2` | 12 | Clutter vs clarity |
| `vista_anchor` | Torii at end of main path | Direction without UI compass |
| `gameplay_cam_height_m` | 1.6 | Validates door/well scale |
| `golden_screenshot` | `artifacts/screenshots/phase1_ruined_village_gameplay.png` | Visual regression |

---
