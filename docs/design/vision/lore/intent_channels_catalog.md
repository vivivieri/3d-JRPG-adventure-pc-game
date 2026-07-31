---
id: intent-channels-catalog
type: reference
phase: [1, 6]
audience: [narrative, builder, visual]
status: active
authority: vision
tokens_est: 594
summary: "The ruined coast tells the story without NPC crowds. Emptiness is deliberate — spirits bound to objects, village erased by stolen time."
---
# Lore & Environmental Story — Intent, channels, lore catalog

**Hub:** [`LORE_AND_ENVIRONMENTAL_STORY.md`](../LORE_AND_ENVIRONMENTAL_STORY.md)

## When to read

Use **Lore & Environmental Story — Intent, channels, lore catalog** (roles: narrative, builder, visual) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [1. Design intent](#1-design-intent)
- [2. Two discovery channels](#2-two-discovery-channels)
- [3. Lore entry catalog](#3-lore-entry-catalog)


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
