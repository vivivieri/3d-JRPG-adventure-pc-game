# Tides of Urashima — Lore & Environmental Storytelling

**Version:** 1.0 (Pre-build)  
**Story reference:** `docs/STORYBOARD.md`, `game/data/lore/lore_entries.json`, `game/data/lore/lore_placements.json`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md`, `docs/QUEST_AND_FLAGS.md`, `docs/ACHIEVEMENTS.md`

---

## 1. Design intent

The ruined coast tells the story **without NPC crowds**. Emptiness is deliberate — spirits bound to objects, village erased by stolen time.

| Goal | Method |
|------|--------|
| Guilt before palace | Village inspect + lore |
| Box mystery | Layer clues until SC-13 |
| Optional depth | 8 lore entries + achievement |
| No encyclopedia | Short entries; 2–4 sentences |

**Target:** ≥70% players understand box stakes before SC-16 (`NARRATIVE_WRITING_GUIDE.md` §8).

---

## 2. Two discovery channels

| Channel | Trigger | Content | Data |
|---------|---------|---------|------|
| **Scene inspect** | E on story object during scene flow | Immediate dialogue | `dialogue/chapter_01.json` (`SC-02-*`) |
| **Lore pickup** | E on placed journal object in field | Journal entry (read later in Tab → Lore) | `lore/lore_entries.json` |

Both reinforce the same themes; inspect = emotional beat, lore = archival detail.

---

## 3. Lore entry catalog

| ID | Zone | Title (EN) | Theme |
|----|------|------------|-------|
| `fishing_ledger` | `ruined_village` | Fishing Ledger | Urashima didn't return with tide |
| `festival_banner` | `ruined_village` | Faded Festival Banner | Festival the week he vanished |
| `yuzu_prayer` | `ruined_village` | Prayer Slip at Torii | Yuzu waited |
| `roku_dive_log` | `ruined_village` | Roku's Dive Log | Caves breathe |
| `cave_inscription` | `tidal_caves` | Cave Wall Inscription | Palace takes years |
| `sailor_charm` | `tidal_caves` | Sailor's Charm | Grants `spirit_bell` equip |
| `palace_seal` | `dragon_palace_gate` | Palace Invitation Seal | Paradise demands abandonment |
| `otohime_letter` | `dragon_palace_gate` | Letter Fragment | Don't open the box |

**Achievement:** `ACH_LORE_COMPLETE` — read all 8 (`ACHIEVEMENTS.md`). Optional; not required for endings.

---

## 4. Placement map

From `lore_placements.json` + zone kits:

| Lore ID | Zone | Near landmark | Act |
|---------|------|---------------|-----|
| `fishing_ledger` | Village | Near pier / ledger prop | I |
| `festival_banner` | Village | Festival grounds (near SC-02-BANNER inspect) | I |
| `yuzu_prayer` | Village | Cracked torii (`SC-03` area) | I |
| `roku_dive_log` | Village | Roku shack exterior | I |
| `cave_inscription` | Caves | Mid-path wall | II |
| `sailor_charm` | Caves | Deep path before boss branch | II |
| `palace_seal` | Palace gate | Exterior walkway | III |
| `otohime_letter` | Palace gate | Interior antechamber | III |

**Visual:** Lore objects use subtle cyan interact glow (`ART_DIRECTION.md` cave palette).

---

## 5. Inspect scenes vs lore (village)

| Story beat | Inspect dialogue | Related lore |
|------------|------------------|--------------|
| Rotting banner | `SC-02-BANNER` | `festival_banner` |
| Child sandal | `SC-02-SANDAL` | — |
| Choked well (save) | `SC-02-WELL` | — |
| Torii spirit | `SC-03` | `yuzu_prayer` |

Player may hit inspect first, find lore later — both valid.

---

## 6. Hub emptiness (by design)

| Choice | Rationale |
|--------|-----------|
| No living villagers | Time took them; spirits remain |
| Ambient cats/dogs | Silhouette life only (`CHARACTER_BIBLE.md` §7) |
| Wind + rot | Primary "NPC" in Act I |
| Roku only elder | Living witness; anchor |

**Do not add** chatty town NPCs in v1 — breaks dread (`PACING_CHART.md`).

---

## 7. Environmental storytelling per zone

### Beach / village (Act I)

| Element | Story |
|---------|-------|
| Submerged homes | Sea reclaimed land |
| Faded banners | Interrupted festival |
| Child sandal | Innocence lost |
| Well save point | Last communal place |

### Tidal caves (Act II)

| Element | Story |
|---------|-------|
| Biolume algae | Wrong beauty |
| SC-07 silence | Tide logic without words |
| Drowned faces (SC-08) | Collective guilt |
| Inscription | Palace steals years |

### Palace gate (Act III)

| Element | Story |
|---------|-------|
| Floating architecture | Impossible time |
| Mirror chamber | Young + old Urashima |
| Lacquer armor | Ryūgū not European |
| Void sea sky | Paradise isolated from world |

---

## 8. Box clue ladder

| Order | Source | Clue |
|-------|--------|------|
| 1 | SC-00 / SC-04 | Box from palace; don't open |
| 2 | `fishing_ledger` | Village waited |
| 3 | `cave_inscription` | Years stolen like shells |
| 4 | SC-11 | Paradise bargain |
| 5 | SC-13 | Box holds **their** years |
| 6 | SC-16 | Player chooses price |

---

## 9. Writer / level design checklist

- [ ] All 8 lore IDs have placements in zone
- [ ] `sailor_charm` grants `spirit_bell` on read
- [ ] Inspect scenes don't duplicate lore text verbatim
- [ ] Journal Tab shows unread indicator
- [ ] Lore readable in all 3 languages
- [ ] SC-07 remains dialogue-free

---

## 10. QA checklist

- [ ] 8/8 lore collectible in one run
- [ ] Achievement fires on 8th read
- [ ] Inspect + lore both work at torii area
- [ ] No lore blocks main path collision
- [ ] Playtest: box understood ≥70% before SC-16
