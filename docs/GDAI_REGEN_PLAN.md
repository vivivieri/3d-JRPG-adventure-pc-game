# GDAI MCP regeneration plan

**Branch:** `cursor/gdai-regen-dc91`  
**Design source:** `main` — `docs/GDD.md`, `docs/STORYBOARD.md`, `docs/ART_DIRECTION.md`  
**Tooling:** **GDAI MCP only** — do **not** use GodotPrompter, prompt-skills, or copy `zone_visuals.gd` from other branches unless you explicitly choose to compare.

---

## Setup (once per machine)

1. Install `uv` — see `docs/GDAI_CLOUD_SETUP.md`
2. Copy commercial plugin → `game/addons/gdai-mcp-plugin-godot/` (gitignored)
3. Open `game/project.godot` in Godot 4.3+
4. Enable **GDAI MCP** plugin → **Start** server
5. Configure Cursor MCP (`~/.cursor/mcp.json` from `.cursor/mcp.json.example`)
6. Open Godot **before** Cursor when using GDAI tools

---

## What this branch contains

| Included | Purpose |
|----------|---------|
| `game/project.godot` | Godot 4.3 project, 5 core autoloads |
| `game/data/*.json` | GDD-aligned content stubs |
| `game/scenes/world/*.tscn` | Greybox zones + gameplay markers |
| `game/scripts/` | Minimal systems (movement, dialogue, combat logic) |

| **Not** included (build with GDAI) | |
|-----------------------------------|---|
| Art, materials, lighting polish | Editor scenes |
| UI scenes (dialogue box, combat HUD) | GDAI node/scene creation |
| Procedural `ZoneVisuals` | Intentionally omitted on this branch |
| GodotPrompter | **Forbidden on this branch** |

---

## Build order (GDAI MCP tasks)

Work top-to-bottom. After each phase, run the project (F5) and fix errors via GDAI’s script/output tools.

### Phase 1 — Project shell
- [x] Verify autoloads load (`GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager`)
- [x] Dialogue + interaction prompt UI autoloads
- [x] New Game → `beach_shore.tscn` (SC-01 arrival)

### Phase 2 — Beach shore (SC-01)
- [x] Sky/fog/water per art bible (scene-authored materials)
- [x] Driftwood, rocks, lacquer box props
- [x] `SceneTransition` to ruined village

### Phase 3 — Ruined village hub (SC-02–05)
- [x] Torii, shack, well, banner inspect meshes (scene-authored)
- [x] Visible sea plane toward -Z
- [x] Dialogue hooks SC-03 / SC-04 on torii + Roku
- [x] `CaveEntrance` → `tidal_caves.tscn`

### Phase 4 — Tidal caves (SC-06–08)
**Scene:** `scenes/world/tidal_caves.tscn`  
**Gameplay nodes (do not move):** `WaterPuzzle`, floor markers, `DeepPoolEncounter`, `ShoreWraithBoss`

GDAI tasks:
- Cave tunnel mesh, bioluminescent algae materials
- Flood pool basin at `WaterPuzzle`
- Water level puzzle (raise/lower) — wire existing flags if present, else implement with GDAI
- Boss arena at z ≈ -28

### Phase 5 — Dragon Palace gate (SC-09+)
**Scene:** `scenes/world/dragon_palace_gate.tscn`  
**Markers:** `GateArrival`, `PalaceVision`, `MirrorChamber`, `PalaceSentinel`, `TideKeeperBoss`, `ExitToCaves`

GDAI tasks:
- Grand court on void sea (gold/coral vs grey hub)
- Gate, columns, banners, mirror chamber prop
- Throne approach / final boss arena

### Phase 6 — Combat & UI
- [ ] `scenes/ui/dialogue_box.tscn` + hook `DialogueRunner`
- [ ] `scenes/ui/combat_ui.tscn` + enemy intent display
- [ ] `scenes/ui/interaction_prompt_hud.tscn`
- [ ] Combat transition VFX

### Phase 7 — Localization (optional)
- [ ] `locale/translations.csv` + `LocalizationManager` per `docs/LOCALIZATION.md`

---

## GDAI prompt examples

Use these in Cursor **with Godot open and GDAI server running**:

```
Using GDAI MCP only: open beach_shore.tscn and replace the greybox ground with a 
30x20 sand plane, add a DirectionalLight3D matching ART_DIRECTION.md coastal fog, 
and parent driftwood CSG/log meshes near (3, 0, 6). Do not use GodotPrompter.
```

```
Using GDAI MCP: read errors from the Godot editor and fix any script errors in 
game_manager.gd after adding scene_transition.gd to CaveEntrance.
```

```
Using GDAI MCP: create scenes/ui/dialogue_box.tscn with speaker label, body label, 
and advance-on-confirm wired to DialogueRunner signals. Reference SC-03 dialogue test.
```

---

## Comparison branch

To diff against the procedural code-driven build:

```bash
git diff cursor/gdai-regen-dc91 cursor/japanese-environment-dc91 -- game/
```

---

## Export note

Before any Steam build: disable GDAI plugin and remove `game/addons/gdai-mcp-plugin-godot/`.
