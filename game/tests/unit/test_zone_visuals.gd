class_name TestZoneVisuals
extends RefCounted
## Unit tests — zone palette application (P1-01).

const ZoneVisualsScript := preload("res://scripts/exploration/zone_visuals.gd")


static func _load_presets() -> Dictionary:
	var text := FileAccess.get_file_as_string("res://data/world/zone_palettes.json")
	if text.is_empty():
		return {}
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		return {}
	return parsed.get("zones", {})


static func test_hex_to_color_parses_village_fog() -> String:
	var c: Color = ZoneVisualsScript.hex_to_color("#8B9DAF")
	if c.is_equal_approx(Color("#8B9DAF")):
		return ""
	return "expected #8B9DAF, got %s" % [c]


static func test_ruined_village_preset_has_directional() -> String:
	var presets := _load_presets()
	var preset: Dictionary = ZoneVisualsScript.get_preset("ruined_village", presets)
	if preset.is_empty():
		return "ruined_village preset missing"
	if str(preset.get("directional_color")) != "#B8C8D8":
		return "directional_color mismatch"
	if float(preset.get("fog_density")) != 0.008:
		return "fog_density mismatch"
	return ""


static func test_build_environment_fog_enabled() -> String:
	var presets := _load_presets()
	var preset: Dictionary = ZoneVisualsScript.get_preset("ruined_village", presets)
	if preset.is_empty():
		return "ruined_village preset missing"
	var node = ZoneVisualsScript.new()
	var env: Environment = node.build_environment(preset)
	if env == null:
		return "build_environment returned null"
	if not env.fog_enabled:
		return "fog should be enabled"
	if env.tonemap_mode != Environment.TONE_MAPPER_FILMIC:
		return "tonemap should be Filmic"
	if not env.glow_enabled:
		return "glow should be enabled"
	return ""
