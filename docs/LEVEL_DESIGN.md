# Tides of Urashima — Level Design Breakdown

**Version:** 1.0  
**Scope:** Blockouts, pathways, interactables, encounters, camera beats per zone  
**Cross-refs:** [WORLD_MAP_AND_FLOW.md](WORLD_MAP_AND_FLOW.md) (zone graph), [ENVIRONMENT_KITS.md](ENVIRONMENT_KITS.md) (art modules), [QUEST_AND_FLAGS.md](QUEST_AND_FLAGS.md) (flags), `game/data/story/scenes.json`

**Use this doc when:** Placing nodes in Godot, wiring triggers, or validating player path.

---

## 1. Global level rules

| Rule | Value |
|------|-------|
| World structure | Linear hub + dungeon + palace — **no world map screen** |
| Backtracking | Allowed until ending choice |
| Fast travel | None v1 |
| Lost time target | Player not lost >2 min without hint (`WORLD_MAP_AND_FLOW.md` §8) |
| Save points | Village well, palace gate exterior |
| Autosave | Zone transition, quest stage, pre-boss |
| Greybox | Godot primitive meshes only, editor/dev builds Phase 1–6 — replaced by M5 art; never shipped (`.cursorrules` §0 forbids Kenney packs in player-facing builds) |

### Standard node names (all zones)

| Node type | Naming | Script |
|-----------|--------|--------|
| Player spawn | `SpawnMarker_{id}` | `Marker3D` |
| Zone exit | `ZoneTransition_{to_zone}` | `ZoneTransition.gd` |
| Inspectable | `Interactable_{id}` | `Interactable.gd` |
| NPC / dialogue | `Interactable_{scene_id}` | `Interactable.gd` |
| Combat trigger | `EncounterTrigger_{encounter_id}` | `EncounterTrigger.gd` |
| Save | `SavePoint_{name}` | `SavePoint.gd` |
| Cinematic | `CinematicTrigger_{hook_id}` | calls `CinematicDirector` |

---

## 2. Zone: `beach_shore` (SC-01)

**Scene:** `res://scenes/world/beach_shore.tscn`  
**Act:** I · **BGM:** `bgm_village` · **Fog:** light coastal

### Blockout

| Metric | Target |
|--------|--------|
| Playable area | ~80m × 40m strip |
| Path | Linear shore → village gate visible ahead |
| Duration | 2–4 min first visit |

### Layout (top-down)

```
[Ocean]  ~~~~~  [Driftwood scatter]
                    |
              [Player spawn SC-01]
                    |
              [Path to gate]
                    |
         [ZoneTransition → ruined_village]
```

### Interactables & triggers

| Node | Scene ID | Sets flag | Notes |
|------|----------|-----------|-------|
| `SpawnMarker_default` | — | — | Post-prologue or continue spawn |
| `ZoneTransition_ruined_village` | — | `tutorial_movement_done` | After SC-01 dialogue |
| `Interactable_SC-01` | SC-01 | `tutorial_movement_done`, `game_started` | Optional auto on enter |

### Encounters

None.

### Camera

Wide establishing → follow cam (`CINEMATICS.md` SC-01). No authored pan v1.

---

## 3. Zone: `ruined_village` (SC-02–05 hub)

**Scene:** `res://scenes/world/ruined_village.tscn`  
**Act:** I · **BGM:** `bgm_village` · **Fog:** heavy `#8B9DAF`

### Blockout

| Metric | Target |
|--------|--------|
| Hub size | ~120m × 120m |
| Vertical | Mostly flat; pier −2m to water |
| First-enter pan | 4s torii silhouette (`CINEMATICS.md` SC-02) |

### Layout

```
        [Torii — SC-03 Yuzu]
              |
    [Banner inspect] — [Festival ground]
              |
    [Well save] — [Shack — Roku SC-04 shop]
              |
         [Pier / SC-05 crab arena]
              |
         [Cave entrance ↓ tidal_caves]
```

### Interactables & triggers

| Node | Scene ID | Sets flag | Requirement |
|------|----------|-----------|-------------|
| `CinematicTrigger_hub_pan` | SC-02 | `village_arrival_seen` | First enter only |
| `Interactable_SC-02-BANNER` | SC-02-BANNER | `inspected_banner` | — |
| `Interactable_SC-02-SANDAL` | SC-02-SANDAL | `inspected_sandal` | — |
| `SavePoint_well` | SC-02-WELL | `inspected_well` | Manual save + first heal |
| `Interactable_SC-03` | SC-03 | `met_yuzu_spirit` | None (freely reachable) — soft quest arrow appears after 2 inspects (`GAME_FEEL.md`) |
| `Interactable_SC-04` | SC-04 | `met_roku`, `cave_entrance_unlocked` | Grants `cave_map` |
| `EncounterTrigger_enc_sc05_tutorial_crab` | SC-05 | `tutorial_combat_done` | Near pier |
| `ZoneTransition_tidal_caves` | — | `caves_entered` | Requires `cave_entrance_unlocked` |

### Encounters

| Trigger | Encounter ID | Enemy |
|---------|--------------|-------|
| Pier arena | `enc_sc05_tutorial_crab` | Salt Crab (tutorial) |

### Shop

Roku shack — `shop/roku_shop.json`; opens after SC-04.

### Lore placements

See `game/data/lore/lore_placements.json` — banner, well, pier.

---

## 4. Zone: `tidal_caves` (SC-06–11)

**Scene:** `res://scenes/world/tidal_caves.tscn`  
**Act:** II · **BGM:** `bgm_caves` · **Fog:** distance fog per `RENDERING_GUIDE.md` §6 (density 0.028); **no volumetric fog** (interior)

### Blockout

| Metric | Target |
|--------|--------|
| Structure | Linear main path + one optional chest branch |
| Puzzle room | SC-07 flooded chamber ~40m × 30m |
| Boss arena | SC-09 circular ~25m diameter |

### Layout

```
[Entrance SC-06]
      ↓
[Flooded chamber SC-07] ← PUZZLE_DESIGN.md
      ↓ (requires water_puzzle_solved)
[Deep pool SC-08] + vignette hook
      ↓
[Boss arena SC-09 Shore Wraith]
      ↓
[Shrine alcove SC-10 Yuzu join]
      ↓
[Flashback wall SC-11]
      ↓
[Exit → dragon_palace_gate SC-12]
```

### Interactables & triggers

| Node | Scene ID / hook | Sets flag | Requirement |
|------|-----------------|-----------|-------------|
| `EncounterTrigger_enc_sc06_cave_crab` | SC-06 | — | Optional trash mob |
| `PuzzleRoom_sc07` | SC-07 | `water_puzzle_solved` | Silent — no dialogue |
| `EncounterTrigger_enc_sc08_deep_pool` | SC-08 | `deep_pool_seen` | `water_puzzle_solved` |
| `CinematicTrigger_sc08_deep_pool_vignette` | hook | `deep_pool_vignette_seen` | After pool enter |
| `EncounterTrigger_enc_sc09_shore_wraith` | SC-09 | `shore_wraith_defeated` | Boss |
| `Interactable_SC-10` | SC-10 | `yuzu_joined` | Post-boss |
| `CinematicTrigger_SC-11` | SC-11 | `saw_palace_vision` | Letterbox flashback |
| `ZoneTransition_dragon_palace_gate` | SC-12 | `gate_reached` | `yuzu_joined`, `wraith_pearl` |

### Encounters

| ID | Scene | Type |
|----|-------|------|
| `enc_sc06_cave_crab` | SC-06 | Trash |
| `enc_sc08_deep_pool` | SC-08 | Mob |
| `enc_sc09_shore_wraith` | SC-09 | Boss |

### Puzzle SC-07

Full spec: [PUZZLE_DESIGN.md](PUZZLE_DESIGN.md). Water plane Y toggles LOW/HIGH; latch reachable only HIGH.

---

## 5. Zone: `dragon_palace_gate` (SC-12–16)

**Scene:** `res://scenes/world/dragon_palace_gate.tscn`  
**Act:** II–III · **BGM:** `bgm_palace` · **Sky:** void `#1A1A3A`

### Blockout

| Metric | Target |
|--------|--------|
| Hero mesh | `palace_gate_main` ~18k tris (M5) |
| Interior | Mirror hall → sentinel arena → throne |
| SC-12 cinematic | 12–15s gate reveal (`CINEMATICS.md`) |

### Layout

```
[Exterior gate SC-12] — SavePoint_gate
      ↓ (wraith_pearl insert)
[Mirror chamber SC-13]
      ↓
[Sentinel hall SC-14]
      ↓
[Throne arena SC-15 → SC-16 choice]
```

### Interactables & triggers

| Node | Scene ID / hook | Sets flag | Requirement |
|------|-----------------|-----------|-------------|
| `CinematicTrigger_sc12_gate_reveal` | hook | — | First visit; markers `CameraMarker_sc12_*` |
| `SavePoint_gate` | — | — | Manual save |
| `EncounterTrigger_enc_sc12_palace_wraiths` | SC-12 | `roku_combat_active` | Gate approach |
| `Interactable_SC-13` | SC-13 | `knows_box_truth` | Mirror |
| `EncounterTrigger_enc_sc14_sentinel` | SC-14 | `sentinel_defeated` | Boss |
| `EncounterTrigger_enc_sc15_tide_keeper` | SC-15 | `tide_keeper_defeated` | Boss |
| `Interactable_SC-16` | SC-16 | `ending_chosen` | Three-way choice UI |

### Camera markers (SC-12)

| Marker | Beat |
|--------|------|
| `CameraMarker_sc12_wide` | Party at cave exit 0–3s |
| `CameraMarker_sc12_tilt_mid` | Mid vertigo 3–10s |
| `CameraMarker_sc12_gate_hero` | Hero hold 10–15s |

---

## 6. Ending zones (SC-17a/b/c)

| Zone ID | Scene | Ending | BGM |
|---------|-------|--------|-----|
| `ending_rewind` | SC-17a | Rewind | `bgm_ending_rewind` + `cine_ending_rewind_hero` |
| `ending_anchor` | SC-17b | Anchor | `bgm_ending_anchor` + `cine_ending_anchor_hero` |
| `ending_drift` | SC-17c | Drift | `bgm_ending_drift` + `cine_ending_drift_hero` |

Each: single authored space, no combat, cinematic camera only, credits handoff.

**Entry:** `GameManager.load_ending(ending_id)` from SC-16 choice — not walk-back from palace.

---

## 7. Encounter index (all zones)

| Encounter ID | Zone | Scene | Boss? |
|--------------|------|-------|-------|
| `enc_sc05_tutorial_crab` | ruined_village | SC-05 | No |
| `enc_sc06_cave_crab` | tidal_caves | SC-06 | No |
| `enc_sc08_deep_pool` | tidal_caves | SC-08 | No |
| `enc_sc09_shore_wraith` | tidal_caves | SC-09 | **Yes** |
| `enc_sc12_palace_wraiths` | dragon_palace_gate | SC-12 | No |
| `enc_sc14_sentinel` | dragon_palace_gate | SC-14 | **Yes** |
| `enc_sc15_tide_keeper` | dragon_palace_gate | SC-15 | **Yes** |

Source: `game/data/encounters/story_encounters.json`.

---

## 8. Flag gates summary

| Gate | Flag / item | Blocks |
|------|---------------|--------|
| Cave entrance | `cave_entrance_unlocked` | `ruined_village` → `tidal_caves` |
| Deep pool | `water_puzzle_solved` | SC-08 onward |
| Palace exterior | `yuzu_joined`, `wraith_pearl` | SC-12 zone load |
| Ending branch | `ending_chosen` value | SC-17a/b/c |

Full registry: `game/data/story/flags.json`.

---

## 9. QA checklist (level design)

- [ ] Every `Interactable_*` has matching `chapter_01.json` key or inspect sub-scene
- [ ] Every `EncounterTrigger_*` exists in `story_encounters.json`
- [ ] Spawn markers tested for Continue load
- [ ] No soft-lock: SC-07 hint after 3 min stuck (`PUZZLE_DESIGN.md` §5)
- [ ] Zone transitions show 2s area name toast
- [ ] Backtrack village → caves → village works after Yuzu join
- [ ] SC-12 cinematic skippable after 3s on replay

---

## 10. Related docs (don't duplicate here)

| Topic | Doc |
|-------|-----|
| Zone graph & connections | `WORLD_MAP_AND_FLOW.md` |
| Kit meshes & poly budgets | `ENVIRONMENT_KITS.md` |
| Boss patterns | `BOSS_DESIGNS.md` |
| Water puzzle logic | `PUZZLE_DESIGN.md` |
| Runtime wiring | `TECHNICAL_DESIGN.md` |
| Scene spine JSON | `DATA_ARCHITECTURE.md` |
