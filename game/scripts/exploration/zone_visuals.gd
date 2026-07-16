class_name ZoneVisuals
extends Node3D
## Applies per-zone palette, sky, fog, and tonemap to WorldEnvironment + lights.
## Authority: docs/art/RENDERING_GUIDE.md — data in game/data/world/zone_palettes.json

const PALETTE_PATH := "res://data/world/zone_palettes.json"

@export var zone_id: String = "ruined_village"
@export var apply_on_ready: bool = true

var _presets: Dictionary = {}


func _ready() -> void:
	_load_presets()
	if apply_on_ready:
		apply_zone_visuals()


func _load_presets() -> void:
	if not _presets.is_empty():
		return
	var file := FileAccess.get_file_as_string(PALETTE_PATH)
	if file.is_empty():
		push_warning("ZoneVisuals: missing palette data at %s" % PALETTE_PATH)
		return
	var parsed: Variant = JSON.parse_string(file)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("ZoneVisuals: invalid palette JSON")
		return
	_presets = parsed.get("zones", {})


static func hex_to_color(hex: String) -> Color:
	var cleaned := hex.strip_edges().to_upper()
	if cleaned.begins_with("#"):
		cleaned = cleaned.substr(1)
	if cleaned.length() != 6:
		return Color.MAGENTA
	var r := cleaned.substr(0, 2).hex_to_int() / 255.0
	var g := cleaned.substr(2, 2).hex_to_int() / 255.0
	var b := cleaned.substr(4, 2).hex_to_int() / 255.0
	return Color(r, g, b, 1.0)


static func get_preset(zone_key: String, presets: Dictionary) -> Dictionary:
	return presets.get(zone_key, {}) as Dictionary


func apply_zone_visuals(
	world_environment: WorldEnvironment = null,
	directional: DirectionalLight3D = null,
	fill_lights: Array[OmniLight3D] = []
) -> void:
	_load_presets()
	var preset := get_preset(zone_id, _presets)
	if preset.is_empty():
		push_warning("ZoneVisuals: unknown zone_id '%s'" % zone_id)
		return

	if world_environment == null:
		world_environment = _find_world_environment()
	if directional == null:
		directional = _find_directional_light()

	if world_environment != null:
		world_environment.environment = build_environment(preset)
	if directional != null:
		_apply_directional(directional, preset)
	for light in fill_lights:
		_apply_fill_light(light, preset)
	if fill_lights.is_empty():
		for node in get_tree().get_nodes_in_group("zone_fill_light"):
			if node is OmniLight3D:
				_apply_fill_light(node as OmniLight3D, preset)


func build_environment(preset: Dictionary) -> Environment:
	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = hex_to_color(str(preset.get("sky_horizon", "#B8D0E0")))
	env.ambient_light_energy = 0.4

	env.fog_enabled = true
	env.fog_light_color = hex_to_color(str(preset.get("fog_color", "#8B9DAF")))
	env.fog_density = float(preset.get("fog_density", 0.008))
	env.fog_sky_affect = 0.85

	env.glow_enabled = true
	env.glow_intensity = float(preset.get("glow_intensity", 0.35))
	env.glow_blend_mode = Environment.GLOW_BLEND_MODE_SOFTLIGHT

	if bool(preset.get("volumetric_fog_enabled", false)):
		env.volumetric_fog_enabled = true
		env.volumetric_fog_density = 0.02

	var sky := Sky.new()
	var proc := ProceduralSkyMaterial.new()
	proc.sky_top_color = hex_to_color(str(preset.get("sky_top", "#4A7A9A")))
	proc.sky_horizon_color = hex_to_color(str(preset.get("sky_horizon", "#B8D0E0")))
	proc.ground_horizon_color = hex_to_color(str(preset.get("ground_horizon", "#6A8A9A")))
	proc.ground_bottom_color = proc.ground_horizon_color.darkened(0.2)
	proc.sun_angle_max = 28.0
	sky.sky_material = proc
	env.sky = sky
	return env


func _apply_directional(light: DirectionalLight3D, preset: Dictionary) -> void:
	light.light_color = hex_to_color(str(preset.get("directional_color", "#B8C8D8")))
	light.shadow_enabled = true
	var rot: Array = preset.get("directional_rotation_deg", [35, -45, 0])
	if rot.size() >= 2:
		var rz := float(rot[2]) if rot.size() > 2 else 0.0
		light.rotation_degrees = Vector3(float(rot[0]), float(rot[1]), rz)


func _apply_fill_light(light: OmniLight3D, preset: Dictionary) -> void:
	light.light_color = hex_to_color(str(preset.get("fill_color", "#D4A880")))
	light.light_energy = 0.8
	light.omni_range = 12.0


func _find_world_environment() -> WorldEnvironment:
	var parent := get_parent()
	if parent == null:
		return null
	return parent.find_child("WorldEnvironment", true, false) as WorldEnvironment


func _find_directional_light() -> DirectionalLight3D:
	var parent := get_parent()
	if parent == null:
		return null
	return parent.find_child("DirectionalLight3D", true, false) as DirectionalLight3D
