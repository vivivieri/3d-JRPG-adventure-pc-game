---
id: data-scene-shader
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 440
summary: "Data access, scenes, shaders"
---
# Code Style — Data access, scenes, shaders

**Hub:** [`CODE_STYLE.md`](../CODE_STYLE.md)

## 6. Data access patterns

```gdscript
# Load once, cache on manager
var _skills: Dictionary = GameManager.load_json("res://data/skills/skills.json")

# Story line filter
var lines: Array = StoryData.filter_dialogue_lines(
    chapter["lines"],
    GameManager.get_all_flags()
)

# Encounter by id
var enc: Dictionary = _encounters["encounters"][encounter_id]
```

**Never** embed dialogue strings or skill numbers in `.gd` except dev-only debug.

---


## 7. Scene authoring rules

| Rule | Detail |
|------|--------|
| **GDAI MCP builds `.tscn`** | No hand-editing scene trees in Cursor when GDAI is up |
| **Component scenes** | Use catalog from `LEVEL_DESIGN.md` §1b — wells, doors, triggers |
| **Groups** | `player`, `interactable`, `encounter_trigger` for queries |
| **Markers** | `SpawnMarker_default`, `CameraMarker_sc12_wide` — match `LEVEL_DESIGN.md` |
| **Layers** | Collision layers documented per zone in level design |
| **No primitives in ship** | `BoxMesh` greybox OK until M5; replace with kit meshes |

---


## 8. Shader conventions

- One **toon ramp family** project-wide (`toon_base.gdshader`)
- Zone variants = duplicate material + uniform tweaks, not separate shader languages
- Water: `water_stylized.gdshader` only on water meshes
- Emission for interactables, box, biolume — see `RENDERING_GUIDE.md`

```gdshader
shader_type spatial;
render_mode diffuse_toon, specular_toon;
# uniforms: base_color, albedo_texture, emission_strength
```

---
