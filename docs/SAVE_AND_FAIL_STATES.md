# Tides of Urashima — Save & Fail States

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/UI_UX_FLOW.md`, `docs/QUEST_AND_FLAGS.md`, `docs/ENDING_DESIGN.md`

---

## 1. Save system

| Parameter | Value |
|-----------|-------|
| Slots | **1** slot v1 (`user://save_slot_0.json`) |
| Autosave | **Yes** — on scene transition + quest stage complete |
| Manual save | Village well (`VillageWell`) — full heal first visit only |
| Save on quit | Autosave current state |
| Mid-combat save | **No** |

---

## 2. Save data schema

```json
{
  "version": 1,
  "timestamp": "ISO-8601",
  "scene": "res://scenes/world/ruined_village.tscn",
  "spawn_marker": "default",
  "flags": { "met_roku": true },
  "party": { "levels": {}, "hp": {}, "mp": {} },
  "inventory": { "items": {}, "equipment": {} },
  "quests": { "active_stage": {} },
  "lore_read": ["fishing_ledger"],
  "settings": { "locale": "en" },
  "meta": {
    "playtime_sec": 3600,
    "ending_unlocked": ["anchor"],
    "seen_cinematics": ["SC-11"]
  }
}
```

---

## 3. What persists

| Data | Persist |
|------|---------|
| Story flags | ✓ |
| Quest stages | ✓ |
| Party level/stats | ✓ |
| Inventory/equipment | ✓ |
| Lore read | ✓ |
| Ending gallery unlocks | ✓ meta |
| Tutorial flags | ✓ |
| Mid-battle state | ✗ |

---

## 4. Continue behavior

- **Continue** loads autosave
- If save corrupt: message + New Game only
- Post-credits: slot cleared or marked complete; **Continue** disabled until new run started

---

## 5. Fail states

### Party wipe (combat)

1. All party HP → 0
2. Defeat SFX + screen desaturate
3. Game Over screen
4. **Load Save** → last autosave (before encounter if autosave on transition — player retries from zone entry)

**Design:** Autosave before boss triggers so wipe does not lose >5 min.

### Soft-lock prevention

| Risk | Mitigation |
|------|------------|
| Out of salves | Roku shop restock; drops tuned |
| Out of MP | Spirit Tonic affordable |
| Stuck in puzzle | Hint after 3 min; see `PUZZLE_DESIGN.md` |
| Missing key item | Boss drops guaranteed |

---

## 6. Death vs story

- No permadeath
- No ironman mode v1
- Story choices irreversible **after** SC-16 confirm

---

## 7. Save scumming

**Allowed.** Single slot reduces abuse; players may backup `user://` file. No anti-scum for v1.

**Ending gallery** encourages natural replays over scumming.

---

## 8. QA checklist

- [ ] Autosave fires entering Tidal Caves
- [ ] Well manual save shows confirmation toast
- [ ] Game Over restores valid party HP
- [ ] Continue disabled after credits until New Game
- [ ] Flags restore correctly on load
