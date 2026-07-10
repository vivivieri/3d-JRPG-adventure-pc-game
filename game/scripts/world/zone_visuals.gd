extends RefCounted
## Applies zone palette, sky, fog, lights, and toon materials per docs/RENDERING_GUIDE.md.

const ShaderFactoryLib = preload("res://scripts/shaders/shader_factory.gd")


const PALETTES: Dictionary = {
	"beach_shore": {
		"ground": Color("#C9B89A"),
		"structure": Color("#6A5A48"),
		"accent": Color("#1A6A62"),
		"water_shallow": Color(0.1, 0.42, 0.38, 0.7),
		"water_deep": Color(0.04, 0.18, 0.22, 0.85),
		"fog": Color("#9AB8C8"),
		"sky_top": Color("#5A98B0"),
		"sky_horizon": Color("#C8E0EC"),
		"ground_horizon": Color("#3A7888"),
		"light": Color("#F0E8D0"),
		"fill": Color("#D4C4A8"),
	},
	"ruined_village": {
		"ground": Color("#7A6A52"),
		"structure": Color("#5C4A3A"),
		"accent": Color("#8B3A2A"),
		"moss": Color("#3D5C4A"),
		"water_shallow": Color(0.08, 0.28, 0.32, 0.65),
		"water_deep": Color(0.04, 0.15, 0.2, 0.8),
		"fog": Color("#8B9DAF"),
		"sky_top": Color("#4A7A9A"),
		"sky_horizon": Color("#B8D0E0"),
		"ground_horizon": Color("#6A8A9A"),
		"light": Color("#B8C8D8"),
		"fill": Color("#D4A880"),
	},
	"tidal_caves": {
		"ground": Color("#2A3238"),
		"structure": Color("#222830"),
		"accent": Color("#4AE8D8"),
		"water_shallow": Color(0.05, 0.25, 0.28, 0.75),
		"water_deep": Color(0.02, 0.12, 0.16, 0.9),
		"fog": Color("#0A141C"),
		"sky_top": Color("#060C14"),
		"sky_horizon": Color("#1A3048"),
		"ground_horizon": Color("#142838"),
		"light": Color("#6EC8C0"),
		"fill": Color("#4AE8D8"),
	},
	"dragon_palace_gate": {
		"ground": Color("#E8E4DC"),
		"structure": Color("#D4A55A"),
		"accent": Color("#8B2A3A"),
		"glow": Color("#F0E8D0"),
		"water_shallow": Color(0.08, 0.1, 0.2, 0.6),
		"water_deep": Color(0.04, 0.05, 0.12, 0.85),
		"fog": Color("#1A1A3A"),
		"sky_top": Color("#080818"),
		"sky_horizon": Color("#3A2868"),
		"ground_horizon": Color("#1A2858"),
		"light": Color("#FFD890"),
		"fill": Color("#D4A55A"),
	},
	"ending_rewind": {
		"ground": Color("#C9B89A"),
		"structure": Color("#6A5A48"),
		"accent": Color("#8B3A2A"),
		"water_shallow": Color(0.1, 0.42, 0.38, 0.7),
		"water_deep": Color(0.04, 0.18, 0.22, 0.85),
		"fog": Color("#B8D8E8"),
		"sky_top": Color("#7AB0C8"),
		"sky_horizon": Color("#E8F4FA"),
		"ground_horizon": Color("#5A98B0"),
		"light": Color("#FFF8E8"),
		"fill": Color("#D4C4A8"),
	},
	"ending_anchor": {
		"ground": Color("#7A6A52"),
		"structure": Color("#5C4A3A"),
		"accent": Color("#3D5C4A"),
		"water_shallow": Color(0.08, 0.28, 0.32, 0.65),
		"water_deep": Color(0.04, 0.15, 0.2, 0.8),
		"fog": Color("#9AA8A0"),
		"sky_top": Color("#5A7A6A"),
		"sky_horizon": Color("#C8D8C8"),
		"ground_horizon": Color("#6A8A7A"),
		"light": Color("#D8E8D0"),
		"fill": Color("#A8B898"),
	},
	"ending_drift": {
		"ground": Color("#2A3848"),
		"structure": Color("#1A2838"),
		"accent": Color("#4A6888"),
		"water_shallow": Color(0.05, 0.2, 0.35, 0.75),
		"water_deep": Color(0.02, 0.08, 0.18, 0.9),
		"fog": Color("#1A3048"),
		"sky_top": Color("#0A1420"),
		"sky_horizon": Color("#2A4868"),
		"ground_horizon": Color("#142838"),
		"light": Color("#88B8D8"),
		"fill": Color("#4A6888"),
	},
}


static func apply_to_scene(root: Node3D, zone_id: String) -> void:
	var palette: Dictionary = PALETTES.get(zone_id, PALETTES.ruined_village)
	_apply_environment(root, palette, zone_id)
	_apply_directional_light(root, palette, zone_id)
	_apply_fill_lights(root, palette, zone_id)
	_tint_greybox_meshes(root, palette)


static func _apply_environment(root: Node3D, palette: Dictionary, zone_id: String) -> void:
	var env_node := root.get_node_or_null("WorldEnvironment") as WorldEnvironment
	if env_node == null:
		env_node = WorldEnvironment.new()
		env_node.name = "WorldEnvironment"
		root.add_child(env_node)
		if root.owner:
			env_node.owner = root.owner

	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	env.sky = _make_zone_sky(palette, zone_id)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = palette.light * 0.35
	env.fog_enabled = true
	env.fog_light_color = palette.fog
	env.fog_sky_affect = 0.85
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.glow_enabled = zone_id in ["tidal_caves", "dragon_palace_gate"]
	if env.glow_enabled:
		env.glow_intensity = 0.35
		env.glow_bloom = 0.18
		env.glow_blend_mode = Environment.GLOW_BLEND_MODE_SOFTLIGHT

	match zone_id:
		"beach_shore":
			env.fog_density = 0.010
			env.fog_aerial_perspective = 0.78
		"ruined_village":
			env.fog_density = 0.008
			env.fog_aerial_perspective = 0.72
		"tidal_caves":
			env.fog_density = 0.028
			env.fog_aerial_perspective = 0.48
			env.ambient_light_color = palette.light * 0.22
		"dragon_palace_gate":
			env.fog_density = 0.012
			env.fog_aerial_perspective = 0.68
			env.ambient_light_color = palette.light * 0.55
		_:
			env.fog_density = 0.012
			env.fog_aerial_perspective = 0.5

	if SettingsManager:
		SettingsManager.apply_to_environment(env)

	env_node.environment = env


static func _make_zone_sky(palette: Dictionary, zone_id: String) -> Sky:
	var sky := Sky.new()
	var mat := ProceduralSkyMaterial.new()
	mat.sky_top_color = palette.sky_top
	mat.sky_horizon_color = palette.sky_horizon
	mat.ground_horizon_color = palette.ground_horizon
	mat.ground_bottom_color = Color(palette.get("ground_horizon", Color("#0E2838")))
	mat.sky_curve = 0.18
	mat.ground_curve = 0.04
	match zone_id:
		"beach_shore":
			mat.sun_angle_max = 32.0
		"ruined_village":
			mat.sun_angle_max = 28.0
		"tidal_caves", "dragon_palace_gate":
			mat.sun_angle_max = 8.0
	sky.sky_material = mat
	return sky


static func _apply_directional_light(root: Node3D, palette: Dictionary, zone_id: String) -> void:
	var light := root.get_node_or_null("DirectionalLight3D") as DirectionalLight3D
	if light == null:
		light = DirectionalLight3D.new()
		light.name = "DirectionalLight3D"
		root.add_child(light)
		if root.owner:
			light.owner = root.owner

	light.shadow_enabled = true
	light.light_color = palette.light
	light.light_energy = 1.05 if zone_id == "dragon_palace_gate" else 0.9

	match zone_id:
		"beach_shore", "ruined_village":
			light.rotation_degrees = Vector3(-48, -35, 0)
		"dragon_palace_gate":
			light.rotation_degrees = Vector3(-62, 22, 0)
			light.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
			light.shadow_opacity = 0.42
		"tidal_caves":
			light.rotation_degrees = Vector3(-70, 15, 0)
			light.light_energy = 0.45

	if SettingsManager:
		SettingsManager.apply_to_directional_light(light)


static func _apply_fill_lights(root: Node3D, palette: Dictionary, zone_id: String) -> void:
	var fill := root.get_node_or_null("FillLight") as OmniLight3D
	if zone_id == "ruined_village":
		if fill == null:
			fill = OmniLight3D.new()
			fill.name = "FillLight"
			root.add_child(fill)
			if root.owner:
				fill.owner = root.owner
		fill.light_color = palette.fill
		fill.light_energy = 0.8
		fill.omni_range = 14.0
		fill.position = Vector3(6, 2.5, -4)
	elif fill:
		fill.queue_free()


static func _tint_greybox_meshes(root: Node3D, palette: Dictionary) -> void:
	for node in root.find_children("*", "MeshInstance3D", true, false):
		_apply_mesh_material(node as MeshInstance3D, palette)


static func _apply_mesh_material(mesh: MeshInstance3D, palette: Dictionary) -> void:
	var role := mesh.get_meta("greybox_role", mesh.name.to_lower()) as String
	var color: Color = palette.ground
	var emission := Color.BLACK
	var emission_strength := 0.0

	if role.contains("water") or mesh.name.to_lower().contains("water"):
		mesh.material_override = ShaderFactoryLib.make_water(palette.water_shallow, palette.water_deep)
		return
	if role.contains("structure") or role.contains("torii") or role.contains("shack") or role.contains("pier") or role.contains("pillar") or role.contains("gate"):
		color = palette.structure
	elif role.contains("accent") or role.contains("banner") or role.contains("crimson"):
		color = palette.accent
	elif role.contains("moss") or role.contains("algae"):
		color = palette.get("moss", palette.accent)
		emission = palette.accent
		emission_strength = 0.45
	elif role.contains("glow") or role.contains("gold"):
		color = palette.get("glow", palette.structure)
		emission = palette.get("glow", palette.structure)
		emission_strength = 0.25

	mesh.material_override = ShaderFactoryLib.make_toon(color, emission, emission_strength)
	mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
