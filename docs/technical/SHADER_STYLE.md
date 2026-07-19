# Godot Shader Style Guide — Tides of Urashima

**Version:** 1.0  
**Scope:** `game/shaders/` (`game/development`) · reference templates in `tools/godot_templates/shaders/`  
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)  
**Rendering:** [`RENDERING_GUIDE.md`](../art/RENDERING_GUIDE.md) · [`ART_DIRECTION.md`](../art/ART_DIRECTION.md)

---

## 1. NPR family rules

One **toon ramp family** project-wide — not per-zone shader languages.

| Shader | Use |
|--------|-----|
| `toon_base.gdshader` | Wood, stone, props, characters — default spatial |
| `water_stylized.gdshader` | Water meshes only |
| Zone variants | Duplicate material + uniform tweaks — not new shader files per zone |

---

## 2. Required structure

```gdshader
shader_type spatial;
render_mode diffuse_toon, specular_toon;

uniform vec4 base_color : source_color = vec4(1.0);
// …
void fragment() {
    ALBEDO = …;
    ROUGHNESS = 1.0;
    METALLIC = 0.0;
}
```

| Rule | Detail |
|------|--------|
| `shader_type` | Required first statement |
| Toon materials | `render_mode` includes `diffuse_toon, specular_toon` |
| PBR | `ROUGHNESS = 1.0`, `METALLIC = 0.0` on ship materials — no glossy skin |
| Emission | Uniform-driven — lacquer box, algae, palace trim (`RENDERING_GUIDE.md`) |
| Water | May add `blend_mix`, `depth_draw_opaque` — still toon spec/diffuse |
| File name | `snake_case.gdshader` |

---

## 3. Forbidden in ship builds

| Don't | Why |
|-------|-----|
| `StandardMaterial3D` realism in player scenes | Breaks NPR read |
| Full PBR ORM workflow | Wrong art direction |
| Per-object unique shader languages | Breaks material budget (≤8 visible / zone) |
| HDR reflections, lens flare in shader | `RENDERING_GUIDE.md` §3 |

---

## 4. Authoring workflow

1. GodotPrompter drafts `.gdshader` in Cursor  
2. GDAI MCP assigns material on mesh in zone `.tscn`  
3. F5 viewport + `run_visual_smoke_checks.sh` when assets exist  

Templates ship in `tools/godot_templates/shaders/` for porting to `game/shaders/` on `game/development`.

---

## 5. CI enforcement

```bash
python3 tools/check_gdshader_style.py   # L1_gdshader_style
```

Static checks: `shader_type`, toon `render_mode`, snake_case path, trailing newline.

Godot compile check on `game/development`: headless import via zone scenes (L2 visual gates).

---

## 6. PR checklist

- [ ] `python3 tools/check_gdshader_style.py` green
- [ ] Zone uses palette from `zone_palettes.json` / `RENDERING_GUIDE.md`
- [ ] Water shader only on water meshes
- [ ] GDAI MCP applied material in editor — no hand-edited `.tscn` on Cursor when MCP up
