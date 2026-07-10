# GodotPrompter complete build plan

**Branch:** `cursor/godotprompt-complete-c4bf`  
**Design source:** `main` — `docs/GDD.md`, `docs/STORYBOARD.md`, `docs/ART_DIRECTION.md`  
**Tooling:** **[GodotPrompter](https://github.com/jame581/GodotPrompter) only** — do **not** use GDAI MCP on this branch.

---

## Setup (once per machine)

1. Install Godot 4.3+ — open `game/project.godot`
2. Install GodotPrompter skills:

   ```bash
   ./tools/install_godotprompter.sh
   ```

   Or in Cursor: `/add-plugin godot-prompter`

3. When prompting Cursor, reference skills explicitly, e.g. *"Using the `dialogue-system` skill, …"*

**Startup order:** no editor bridge required (unlike GDAI). GodotPrompter is a **skills framework** — Cursor writes code/scenes; you validate in Godot with F5.

---

## What this branch contains

| Included | Purpose |
|----------|---------|
| `game/project.godot` | Godot 4.3 project, autoloads per `godot-project-setup` skill |
| `game/data/*.json` | GDD-aligned content (skills, enemies, dialogue, quests) |
| `game/scenes/world/*.tscn` | All zones including SC-01 `beach_shore` |
| `game/scenes/ui/*.tscn` | Dialogue, combat HUD, field menu, endings |
| `game/scripts/` | EventBus, combat, dialogue, save, world systems |
| `tools/` | Export, audio generation, GodotPrompter installer |
| `.cursor-plugin/` | Cursor plugin manifest → GodotPrompter skills |

| **Not** included | |
|------------------|---|
| GDAI MCP plugin | **Forbidden on this branch** — use `cursor/gdai-regen-dc91` instead |
| Procedural `zone_visuals.gd` as sole art path | Use GodotPrompter `3d-essentials` + `assets-pipeline` for scene polish |

---

## GodotPrompter skills used

| Phase | Skill | Applied to |
|-------|-------|------------|
| Project shell | `godot-project-setup` | Directory layout, autoloads, input map, `.gitignore` |
| Architecture | `event-bus` | `EventBus` autoload, decoupled UI/combat/audio |
| Narrative | `dialogue-system` | `DialogueRunner`, JSON scenes, `dialogue_box.tscn` |
| Combat | `gdscript-patterns` | `CombatManager`, `SkillResolver`, data-driven AI |
| World | `3d-essentials` | Greybox zones, materials, fog per `ART_DIRECTION.md` |
| UI | `godot-ui` | Combat HUD, field menu, interaction prompt |
| Persistence | `save-load` | `SaveSystem`, well save point |
| Audio | `audio-system` | `AudioManager`, zone BGM crossfade |
| i18n | `localization` (if available) | `LocalizationManager`, `translations.csv` |
| Ship | `export-pipeline` | `tools/export_windows.sh`, Steam presets |

---

## Build order (GodotPrompter tasks)

Work top-to-bottom. After each phase, run the project (F5) and fix errors.

### Phase 1 — Project shell ✓
- [x] Autoloads: `GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager`, `AudioManager`
- [x] Main menu → New Game → `beach_shore.tscn` (SC-01)
- [x] Input map: WASD, E, Tab, confirm/cancel

### Phase 2 — Beach shore (SC-01) ✓
**Scene:** `scenes/world/beach_shore.tscn`  
- [x] Sand shore, driftwood, lacquer box, sea plane
- [x] Arrival dialogue `SC-01` via `world_scene.gd`
- [x] Transition inland → `ruined_village.tscn`

### Phase 3 — Ruined village hub (SC-02–05) ✓
**Scene:** `scenes/world/ruined_village.tscn`  
- [x] Torii, Roku shack, well save, tutorial combat, cave entrance
- [x] Dialogue hooks `SC-02` … `SC-05`

### Phase 4 — Tidal caves (SC-06–09) ✓
**Scene:** `scenes/world/tidal_caves.tscn`  
- [x] Water puzzle, wraith encounters, Shore Wraith boss
- [x] Yuzu joins party

### Phase 5 — Dragon Palace gate (SC-10+) ✓
**Scene:** `scenes/world/dragon_palace_gate.tscn`  
- [x] Palace Sentinel + Tide Keeper bosses
- [x] Three endings (`ending_rewind`, `ending_anchor`, `ending_drift`)

### Phase 6 — Combat & UI ✓
- [x] Turn-based combat with enemy intent display
- [x] Field menu (items, equipment), quest tracker
- [x] Credits roll

### Phase 7 — Polish & Steam ✓
- [x] Procedural BGM/SFX, zone materials
- [x] GodotSteam scaffold, Windows export script
- [x] Steam store copy + screenshots

---

## GodotPrompter prompt examples

```
Using GodotPrompter skills (dialogue-system + event-bus): wire SC-04 Roku dialogue 
to the RokuShack interactable and set flag caves_unlocked on complete.
```

```
Using GodotPrompter 3d-essentials: add bioluminescent algae emissive materials 
to tidal_caves.tscn per ART_DIRECTION.md deep teal / biolume cyan palette.
```

```
Using GodotPrompter gdscript-patterns: add a phase transition to shore_wraith 
boss AI when HP drops below 50% — read enemies.json phases field.
```

---

## Comparison branches

| Branch | Tooling |
|--------|---------|
| `cursor/godotprompt-complete-c4bf` | **GodotPrompter skills** (this branch) |
| `cursor/gdai-regen-dc91` | GDAI MCP editor bridge only |
| `cursor/m5-polish-dc91` | Code-driven procedural art |

```bash
git diff cursor/godotprompt-complete-c4bf cursor/m5-polish-dc91 -- game/
```

---

## Export note

GodotPrompter cache (`.godot-prompter/`) is gitignored. For Steam builds, export with `./tools/export_windows.sh` — only `godotsteam` ships in `addons/`.
