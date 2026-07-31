---
id: zones-box-checklists
type: reference
phase: [1, 6]
audience: [narrative, builder, visual]
status: active
authority: vision
tokens_est: 624
summary: "Per-zone story, box ladder, writer/QA checklists"
---
# Lore & Environmental Story — Per-zone story, box ladder, writer/QA checklists

**Hub:** [`LORE_AND_ENVIRONMENTAL_STORY.md`](../LORE_AND_ENVIRONMENTAL_STORY.md)

## When to read

Use **Lore & Environmental Story — Per-zone story, box ladder, writer/QA checklists** (roles: narrative, builder, visual) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [7. Environmental storytelling per zone](#7-environmental-storytelling-per-zone)
- [Beach / village (Act I)](#beach-village-act-i)
- [Tidal caves (Act II)](#tidal-caves-act-ii)
- [Palace gate (Act III)](#palace-gate-act-iii)
- [8. Box clue ladder](#8-box-clue-ladder)
- [9. Writer / level design checklist](#9-writer-level-design-checklist)
- [10. QA checklist](#10-qa-checklist)


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
- [ ] Lore readable in all ship locales (en / ja / zh / zh-Hant in `lore_entries.json`)
- [ ] SC-07 remains dialogue-free

---


## 10. QA checklist

- [ ] 8/8 lore collectible in one run
- [ ] Achievement fires on 8th read
- [ ] Inspect + lore both work at torii area
- [ ] No lore blocks main path collision
- [ ] Playtest: box understood ≥70% before SC-16
