# Tides of Urashima — Save & Fail States

**Version:** 1.0 (Pre-build)
**Cross-refs:** `docs/ui/UI_UX_FLOW.md`, `docs/world/QUEST_AND_FLAGS.md`, `docs/vision/ENDING_DESIGN.md`

---

## 1. Save system

| Parameter | Value |
|-----------|-------|
| Slots | **1** run slot v1 (`user://save_slot_0.json`) + **1** profile file (`user://profile_meta.json`) |
| Autosave | **Yes** — on scene transition + quest stage complete + pre-boss |
| Manual save | Village well (`VillageWell`, full heal first visit only) + palace gate exterior SavePoint (SC-12+, no heal) — both write the same slot |
| Pause-menu Save | Writes the autosave slot; anywhere in field except mid-combat / SC-16 (`UI_UX_FLOW.md` §4) |
| Save on quit | Autosave current state |
| Mid-combat save | **No** |

**Two files, two lifetimes:**

| File | Contains | Cleared by New Game? |
|------|----------|----------------------|
| `user://save_slot_0.json` | Current run: flags, party, inventory, quests | **Yes** (overwritten) |
| `user://profile_meta.json` | Cross-run meta: ending gallery, prologue skip, playtime | **No** (persists forever) |
| `user://settings.json` | Options: locale, volume, hard_mode… (`SETTINGS_ACCESSIBILITY.md`) | **No** |

---

## 2. Save data schema

### `user://save_slot_0.json` (per run)

```json
{
  "version": 1,
  "timestamp": "ISO-8601",
  "scene": "res://scenes/world/ruined_village.tscn",
  "spawn_marker": "default",
  "flags": { "met_roku": true },
  "party": {
    "level": 5,
    "field": ["urashima", "yuzu"],
    "combat": ["urashima", "yuzu"],
    "hp": { "urashima": 168 },
    "mp": { "urashima": 42 },
    "limit": { "urashima": 40 },
    "extra_skills": { "urashima": ["returning_wave"] }
  },
  "inventory": { "items": { "sea_salve": 2 }, "key_items": ["lacquer_box"], "equipment": {}, "gold": 120 },
  "quests": { "active": ["echoes_at_torii"], "stage": { "echoes_at_torii": "enter_caves" } },
  "encounters_completed": ["enc_sc05_tutorial_crab"],
  "lore_read": ["fishing_ledger"],
  "chests_opened": ["cave_chest_ancient"],
  "tutorial_seen": ["interact", "save_point"],
  "run_ending": null
}
```

Notes: `party.level` is the shared party level (`COMBAT_SYSTEMS.md` §8); `extra_skills` holds
scroll-taught skills; `encounters_completed` / `chests_opened` prevent retrigger and re-loot on
reload or backtrack (every non-repeatable trigger persists its ID here).

**Integrity (ship builds):** `SaveSystem` adds `"_integrity": "<hmac-sha256-hex>"` via `SaveIntegrity.attach()` before write. On load, `SaveIntegrity.verify()` must pass or the slot is treated as corrupt (`docs/qa/SECURITY.md` §9.4). Spec: `game/data/qa/save_integrity.json`.

### `user://profile_meta.json` (cross-run)

```json
{
  "version": 1,
  "prologue_seen": true,
  "game_completed_once": true,
  "endings_unlocked": ["anchor"],
  "hard_cleared": false,
  "playtime_total_sec": 9200
}
```

---

## 3. What persists

| Data | Persist | Where |
|------|---------|-------|
| Story flags | ✓ per run | slot |
| Quest stages | ✓ per run | slot |
| Party level/stats | ✓ per run | slot |
| Inventory/equipment/gold | ✓ per run | slot |
| Encounter/chest completion | ✓ per run | slot |
| Lore read | ✓ per run | slot |
| Tutorial flags | ✓ per run | slot (reshown on new runs; skipped entirely if `game_completed_once`) |
| Ending gallery unlocks | ✓ **forever** | `profile_meta.json` |
| Prologue skip | ✓ **forever** | `profile_meta.json` |
| Mid-battle state | ✗ | — |

---

## 4. Continue behavior (canonical — `ENDING_DESIGN.md` §7 and `REPLAY_DESIGN.md` §3 defer here)

- **Continue** loads the run slot's latest autosave
- If save corrupt: message + New Game only
- **Post-credits:** the slot is marked complete (`run_ending` set) and shows the ending icon.
  **Continue is disabled** until the player starts a New Game. Endings are revisited via the
  gallery, not by reloading pre-ending saves.

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
