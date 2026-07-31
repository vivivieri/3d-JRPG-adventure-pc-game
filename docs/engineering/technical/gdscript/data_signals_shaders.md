---
id: data-signals-shaders
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 605
summary: "GDScript Style — Data access, signals, shaders — var _skills: Dictionary = GameManager.load_json('res://data/skills/skills.json')"
---
# GDScript Style — Data access, signals, shaders

**Hub:** [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md)

## When to read

Use **GDScript Style — Data access, signals, shaders** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [9. Data access](#9-data-access)
- [10. Signals & EventBus](#10-signals-eventbus)
- [Same feature area — direct connect](#same-feature-area-direct-connect)
- [Cross-system — EventBus autoload](#cross-system-eventbus-autoload)
- [11. Shaders (`.gdshader`)](#11-shaders-gdshader)


## 9. Data access

```gdscript
# Load once, cache on manager
var _skills: Dictionary = GameManager.load_json("res://data/skills/skills.json")

# Story filter — data-driven
var lines: Array = StoryData.filter_dialogue_lines(
    chapter["lines"],
    GameManager.get_all_flags()
)
```

**Never** embed dialogue strings, skill numbers, or flag names as magic literals without a JSON source — except dev-only debug guarded by `OS.is_debug_build()`.

---


## 10. Signals & EventBus

### Same feature area — direct connect

```gdscript
func _ready() -> void:
    combat_ui.skill_selected.connect(_on_skill_selected)
```

### Cross-system — EventBus autoload

```gdscript
# event_bus.gd
signal flag_changed(flag_name: String, value: Variant)
signal combat_ended(victory: bool)

# game_manager.gd
func set_flag(name: String, value: Variant = true) -> void:
    _flags[name] = value
    EventBus.flag_changed.emit(name, value)
```

Disconnect when nodes are freed if connections span scenes (`Callable` + `is_connected` checks).

---


## 11. Shaders (`.gdshader`)

One **toon ramp family** project-wide. See [`CODE_STYLE.md`](../CODE_STYLE.md) §8 · [`RENDERING_GUIDE.md`](../../../design/art/RENDERING_GUIDE.md).

```gdshader
shader_type spatial;
render_mode diffuse_toon, specular_toon;

uniform vec4 base_color : source_color;
uniform sampler2D albedo_texture : source_color, filter_linear_mipmap;

void fragment() {
    vec4 tex = texture(albedo_texture, UV);
    ALBEDO = tex.rgb * base_color.rgb;
    ROUGHNESS = 1.0;
    METALLIC = 0.0;
}
```

| Rule | Detail |
|------|--------|
| File naming | `snake_case.gdshader` |
| Zone variants | Duplicate material + uniform tweaks |
| Water only | `water_stylized.gdshader` on water meshes |
| No full PBR | Avoid `StandardMaterial3D` in ship scenes |

---
