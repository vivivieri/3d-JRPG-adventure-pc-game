class_name ZoneVisuals
extends RefCounted
## Applies zone palette, fog, and stylized materials to greybox world scenes.


const PALETTES := {
	"ruined_village": {
		"ground": Color("#C9B89A"),
		"structure": Color("#5C4A3A"),
		"accent": Color("#8B3A2A"),
		"moss": Color("#3D5C4A"),
		"water": Color("#1A4A5A"),
		"fog": Color("#8B9DAF"),
		"sky": Color("#8B9DAF"),
		"light": Color("#D4C4A8"),
	},
	"tidal_caves": {
		"ground": Color("#3A3A45"),
		"structure": Color("#2A3238"),
		"accent": Color("#4AE8D8"),
		"water": Color("#1A4A5A"),
		"fog": Color("#1A3040"),
		"sky": Color("#0E1A22"),
		"light": Color("#6EC8C0"),
	},
	"dragon_palace_gate": {
		"ground": Color("#E8E4DC"),
		"structure": Color("#D4A55A"),
		"accent": Color("#8B2A3A"),
		"glow": Color("#F0E8D0"),
		"fog": Color("#1A1A3A"),
		"sky": Color("#1A1A3A"),
		"light": Color("#FFD890"),
	},
}


const ZONE_TEXTURES := {
	"ruined_village": {
		"ground": "res://assets/textures/zones/village_ground.png",
		"structure": "res://assets/textures/zones/village_wood.png",
	},
	"tidal_caves": {
		"ground": "res://assets/textures/zones/cave_stone.png",
		"structure": "res://assets/textures/zones/cave_stone.png",
		"accent": "res://assets/textures/zones/cave_algae.png",
	},
	"dragon_palace_gate": {
		"ground": "res://assets/textures/zones/palace_marble.png",
		"structure": "res://assets/textures/zones/palace_gold.png",
		"glow": "res://assets/textures/zones/palace_gold.png",
	},
}


static func apply_to_scene(root: Node3D, zone_id: String) -> void:
	var palette: Dictionary = PALETTES.get(zone_id, PALETTES.ruined_village)
	_apply_environment(root, palette, zone_id)
	_tint_meshes(root, palette, zone_id)
	_add_zone_props(root, zone_id, palette)


static func _apply_environment(root: Node3D, palette: Dictionary, zone_id: String) -> void:
	var env_node := root.get_node_or_null("WorldEnvironment") as WorldEnvironment
	if env_node == null:
		env_node = WorldEnvironment.new()
		env_node.name = "WorldEnvironment"
		root.add_child(env_node)
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = palette.get("sky", Color("#888888"))
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = palette.get("light", Color.WHITE) * 0.35
	env.fog_enabled = true
	env.fog_light_color = palette.get("fog", Color.GRAY)
	env.fog_density = 0.018
	env.fog_aerial_perspective = 0.4
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env_node.environment = env
	for child in root.get_children():
		if child is DirectionalLight3D:
			child.light_color = palette.get("light", Color.WHITE)
			child.light_energy = 1.0 if zone_id == "dragon_palace_gate" else 0.85


static func _tint_meshes(node: Node, palette: Dictionary, zone_id: String) -> void:
	if node is MeshInstance3D:
		var mesh := node as MeshInstance3D
		var mat := StandardMaterial3D.new()
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
		var name_lower := node.name.to_lower()
		var parent_name := node.get_parent().name.to_lower() if node.get_parent() else ""
		if "water" in name_lower or "water" in parent_name:
			mat.albedo_color = palette.get("water", Color("#1A4A5A"))
			mat.emission_enabled = true
			mat.emission = palette.get("accent", Color.CYAN) * 0.25
			mat.roughness = 0.15
			mat.metallic = 0.1
		elif "barrier" in name_lower or "flood" in parent_name:
			mat.albedo_color = palette.get("structure", Color.GRAY)
			mat.roughness = 0.9
		elif "ground" in parent_name or "floor" in parent_name or "tunnel" in parent_name:
			mat.albedo_color = palette.get("ground", Color.GRAY)
			mat.roughness = 0.85
		elif "torii" in parent_name or "shack" in parent_name or "gate" in parent_name:
			mat.albedo_color = palette.get("structure", Color.GRAY)
			mat.roughness = 0.75
		elif zone_id == "dragon_palace_gate":
			mat.albedo_color = palette.get("structure", Color.GOLD)
			mat.emission_enabled = true
			mat.emission = palette.get("glow", Color.WHITE) * 0.08
			mat.roughness = 0.45
			mat.metallic = 0.2
		elif zone_id == "tidal_caves" and ("algae" in name_lower or randf() > 0.7):
			mat.albedo_color = palette.get("ground", Color.GRAY)
			mat.emission_enabled = true
			mat.emission = palette.get("accent", Color.CYAN) * 0.35
			mat.roughness = 0.7
		else:
			mat.albedo_color = palette.get("ground", Color.GRAY).lerp(palette.get("structure", Color.GRAY), 0.35)
			mat.roughness = 0.8
		_apply_zone_texture(mat, zone_id, name_lower, parent_name)
		mesh.material_override = mat
	for child in node.get_children():
		_tint_meshes(child, palette, zone_id)


static func _add_zone_props(root: Node3D, zone_id: String, palette: Dictionary) -> void:
	if root.get_node_or_null("ZoneProps"):
		return
	var props := Node3D.new()
	props.name = "ZoneProps"
	root.add_child(props)
	match zone_id:
		"ruined_village":
			_add_torii(props, Vector3(-6, 0, -5), palette, zone_id)
			_add_shack(props, Vector3(8, 0, -3), palette, zone_id)
			_add_well(props, Vector3(5, 0, 2), palette, zone_id)
			_add_pier(props, Vector3(-12, 0, 8), palette, zone_id)
			_add_coastline(props, palette, zone_id)
			_add_rock_cluster(props, Vector3(3, 0, -8), palette, zone_id)
			_add_rock_cluster(props, Vector3(-10, 0, -2), palette, zone_id)
			_add_distant_hills(props, palette)
			_add_broken_fence(props, Vector3(2, 0, 6), palette, zone_id)
		"tidal_caves":
			_add_cave_tunnel(props, palette, zone_id)
			for i in 6:
				_add_algae_strip(props, Vector3(-5.5 + i * 2.2, 1.0, 2 - i * 0.3), palette, zone_id)
			_add_stalactites(props, Vector3(-4, 5.5, -6), palette, zone_id)
			_add_stalactites(props, Vector3(4.5, 5.5, -14), palette, zone_id)
			_add_cave_pool_glow(props, Vector3(0, 0.2, -6), palette, zone_id)
		"dragon_palace_gate":
			_add_gate_pillars(props, Vector3(0, 0, 12), palette, zone_id)
			_add_palace_banners(props, Vector3(0, 0, 12), palette, zone_id)
			_add_void_sea(props, palette, zone_id)
			_add_palace_columns(props, Vector3(0, 0, 2), palette, zone_id)
			_add_palace_lanterns(props, Vector3(0, 0, 8), palette, zone_id)


static func _add_torii(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var torii := Node3D.new()
	torii.name = "ToriiProp"
	torii.position = pos
	parent.add_child(torii)
	_add_box(torii, Vector3(-2.2, 0.25, 0), Vector3(0.7, 0.5, 0.7), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_box(torii, Vector3(2.2, 0.25, 0), Vector3(0.7, 0.5, 0.7), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_box(torii, Vector3(-2.2, 2.8, 0), Vector3(0.38, 5.6, 0.38), palette.get("accent", Color.RED), false, zone_id, "structure")
	_add_box(torii, Vector3(2.2, 2.8, 0), Vector3(0.38, 5.6, 0.38), palette.get("accent", Color.RED), false, zone_id, "structure")
	_add_box(torii, Vector3(0, 5.4, 0), Vector3(5.6, 0.32, 0.42), palette.get("accent", Color.RED), false, zone_id, "structure")
	_add_box(torii, Vector3(0, 4.35, 0), Vector3(4.6, 0.2, 0.32), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_box(torii, Vector3(0, 3.6, 0), Vector3(0.9, 0.12, 0.9), palette.get("moss", Color.GREEN), false, zone_id, "ground")


static func _add_shack(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var shack := Node3D.new()
	shack.name = "ShackProp"
	shack.position = pos
	parent.add_child(shack)
	_add_box(shack, Vector3(0, 1.15, 0), Vector3(3.6, 2.3, 3.2), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_box(shack, Vector3(0, 2.55, 0), Vector3(4.2, 0.18, 3.6), palette.get("accent", Color.GRAY), false, zone_id, "structure")
	_add_box(shack, Vector3(-1.8, 3.1, 0), Vector3(2.2, 0.12, 3.4), palette.get("accent", Color.GRAY), false, zone_id, "structure")
	_add_box(shack, Vector3(1.8, 3.1, 0), Vector3(2.2, 0.12, 3.4), palette.get("accent", Color.GRAY), false, zone_id, "structure")
	_add_box(shack, Vector3(1.9, 0.9, 1.5), Vector3(0.08, 1.8, 0.9), Color("#1A1410"), false, zone_id, "structure")


static func _add_well(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var well := Node3D.new()
	well.position = pos
	parent.add_child(well)
	_add_cylinder(well, Vector3(0, 0.55, 0), 0.85, 1.1, palette.get("structure", Color.GRAY), zone_id, "structure")
	_add_box(well, Vector3(0, 1.15, 0), Vector3(2.0, 0.15, 2.0), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_cylinder(well, Vector3(0, 0.15, 0), 0.55, 0.35, Color("#1A3040"), zone_id, "ground")


static func _add_pier(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var pier := Node3D.new()
	pier.position = pos
	parent.add_child(pier)
	for i in 5:
		_add_box(pier, Vector3(i * 1.1, 0.15, 0), Vector3(0.9, 0.3, 3.5), palette.get("structure", Color.GRAY), false, zone_id, "structure")
		_add_box(pier, Vector3(i * 1.1, -0.6, 1.2), Vector3(0.25, 1.2, 0.25), palette.get("structure", Color.GRAY).darkened(0.15), false, zone_id, "structure")
		_add_box(pier, Vector3(i * 1.1, -0.6, -1.2), Vector3(0.25, 1.2, 0.25), palette.get("structure", Color.GRAY).darkened(0.15), false, zone_id, "structure")


static func _add_coastline(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	_add_box(parent, Vector3(0, -0.35, -16), Vector3(42, 0.4, 14), palette.get("water", Color("#1A4A5A")), true, zone_id, "ground")
	_add_box(parent, Vector3(0, 0.05, -10), Vector3(38, 0.08, 2), Color("#C9B89A").lerp(Color.WHITE, 0.15), false, zone_id, "ground")


static func _add_rock_cluster(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var rocks := Node3D.new()
	rocks.position = pos
	parent.add_child(rocks)
	_add_box(rocks, Vector3(0, 0.35, 0), Vector3(1.4, 0.7, 1.0), palette.get("moss", Color.GREEN), false, zone_id, "ground")
	_add_box(rocks, Vector3(0.8, 0.25, 0.6), Vector3(0.9, 0.5, 0.8), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_box(rocks, Vector3(-0.6, 0.2, -0.4), Vector3(0.7, 0.4, 0.7), palette.get("ground", Color.GRAY), false, zone_id, "ground")


static func _add_distant_hills(parent: Node3D, palette: Dictionary) -> void:
	var hills := Node3D.new()
	hills.name = "DistantHills"
	parent.add_child(hills)
	var hill_color: Color = palette.get("fog", Color.GRAY).darkened(0.25)
	_add_box(hills, Vector3(-18, 4, -22), Vector3(14, 8, 3), hill_color)
	_add_box(hills, Vector3(-6, 5, -24), Vector3(16, 10, 3), hill_color.darkened(0.05))
	_add_box(hills, Vector3(12, 3.5, -21), Vector3(12, 7, 3), hill_color)


static func _add_broken_fence(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var fence := Node3D.new()
	fence.position = pos
	parent.add_child(fence)
	for i in 4:
		var h := 1.2 if i % 2 == 0 else 0.7
		_add_box(fence, Vector3(i * 1.3, h * 0.5, 0), Vector3(0.12, h, 0.12), palette.get("structure", Color.GRAY), false, zone_id, "structure")
	_add_box(fence, Vector3(1.95, 0.9, 0), Vector3(2.8, 0.08, 0.08), palette.get("structure", Color.GRAY), false, zone_id, "structure")


static func _add_cave_tunnel(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	for z in range(-28, 14, 3):
		_add_box(parent, Vector3(-6.2, 3.0, z), Vector3(1.4, 6.0, 2.8), palette.get("structure", Color.GRAY), false, zone_id, "structure")
		_add_box(parent, Vector3(6.2, 3.0, z), Vector3(1.4, 6.0, 2.8), palette.get("structure", Color.GRAY), false, zone_id, "structure")
		_add_box(parent, Vector3(0, 6.4, z), Vector3(12.0, 1.0, 2.8), palette.get("structure", Color.GRAY).darkened(0.1), false, zone_id, "structure")
		if z % 6 == 0:
			_add_algae_strip(parent, Vector3(-5.8, 2.0, z + 0.5), palette, zone_id)


static func _add_stalactites(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var group := Node3D.new()
	group.position = pos
	parent.add_child(group)
	for i in 3:
		_add_cylinder(group, Vector3(i * 1.4 - 1.4, -0.8, 0), 0.18 + i * 0.04, 1.6 + i * 0.3, palette.get("ground", Color.GRAY), zone_id, "structure")


static func _add_cave_pool_glow(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var pool := Node3D.new()
	pool.position = pos
	parent.add_child(pool)
	_add_box(pool, Vector3(0, 0, -2), Vector3(7, 0.2, 5), palette.get("water", Color("#1A4A5A")), true, zone_id, "accent")
	var light := OmniLight3D.new()
	light.light_color = palette.get("accent", Color.CYAN)
	light.light_energy = 0.9
	light.omni_range = 10.0
	light.position = Vector3(0, 1.5, -2)
	pool.add_child(light)


static func _add_palace_banners(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var banners := Node3D.new()
	banners.position = pos
	parent.add_child(banners)
	for x in [-5.5, 5.5]:
		_add_box(banners, Vector3(x, 4.5, 0.6), Vector3(0.08, 5.5, 0.08), palette.get("structure", Color.GOLD), true, zone_id, "structure")
		_add_box(banners, Vector3(x, 4.0, 0.9), Vector3(0.04, 3.5, 1.2), palette.get("accent", Color.RED), true, zone_id, "structure")


static func _add_void_sea(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	_add_box(parent, Vector3(0, -4, 8), Vector3(30, 0.5, 40), palette.get("sky", Color.NAVY_BLUE), true, zone_id, "ground")
	for i in 5:
		_add_box(parent, Vector3(-10 + i * 5, -3.5, 14 + i), Vector3(3, 0.05, 3), palette.get("accent", Color.CYAN), true, zone_id, "accent")


static func _add_palace_columns(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var hall := Node3D.new()
	hall.position = pos
	parent.add_child(hall)
	for x in [-5.0, -2.5, 2.5, 5.0]:
		_add_cylinder(hall, Vector3(x, 2.5, 0), 0.45, 5.0, palette.get("glow", Color.WHITE), zone_id, "structure", true)
	_add_box(hall, Vector3(0, 5.2, 0), Vector3(12, 0.5, 1.2), palette.get("structure", Color.GOLD), true, zone_id, "structure")


static func _add_palace_lanterns(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var lanterns := Node3D.new()
	lanterns.position = pos
	parent.add_child(lanterns)
	for x in [-6.0, 6.0]:
		var orb := MeshInstance3D.new()
		var sphere := SphereMesh.new()
		sphere.radius = 0.35
		sphere.height = 0.7
		orb.mesh = sphere
		orb.position = Vector3(x, 6.5, 0)
		var mat := StandardMaterial3D.new()
		mat.albedo_color = palette.get("glow", Color.WHITE)
		mat.emission_enabled = true
		mat.emission = palette.get("glow", Color.WHITE) * 0.6
		orb.material_override = mat
		lanterns.add_child(orb)


static func _add_algae_strip(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	_add_box(parent, pos, Vector3(0.18, 2.8, 1.4), palette.get("accent", Color.CYAN), true, zone_id, "accent")


static func _add_gate_pillars(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var gate := Node3D.new()
	gate.name = "PalaceGate"
	gate.position = pos
	parent.add_child(gate)
	for x in [-4.2, 4.2]:
		_add_cylinder(gate, Vector3(x, 4.2, 0), 0.75, 8.4, palette.get("structure", Color.GOLD), zone_id, "structure", true)
		_add_box(gate, Vector3(x, 8.6, 0), Vector3(1.6, 0.5, 1.6), palette.get("glow", Color.WHITE), true, zone_id, "glow")
	_add_box(gate, Vector3(0, 8.2, 0), Vector3(10.5, 0.9, 1.2), palette.get("glow", Color.WHITE), true, zone_id, "glow")
	_add_box(gate, Vector3(0, 7.2, 0), Vector3(8.5, 0.5, 0.9), palette.get("structure", Color.GOLD), true, zone_id, "structure")
	_add_box(gate, Vector3(0, 5.5, 0.8), Vector3(6, 4, 0.35), Color("#1A1A3A"), true, zone_id, "ground")


static func _add_box(
	parent: Node3D,
	pos: Vector3,
	size: Vector3,
	color: Color,
	emissive: bool = false,
	zone_id: String = "",
	tex_key: String = "structure",
) -> void:
	var mesh_inst := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mesh_inst.mesh = box
	mesh_inst.position = pos
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = 0.65
	if emissive:
		mat.emission_enabled = true
		mat.emission = color * 0.25
	if not zone_id.is_empty():
		_apply_zone_texture(mat, zone_id, tex_key, tex_key, tex_key)
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)


static func _add_cylinder(
	parent: Node3D,
	pos: Vector3,
	radius: float,
	height: float,
	color: Color,
	zone_id: String,
	tex_key: String,
	emissive: bool = false,
) -> void:
	var mesh_inst := MeshInstance3D.new()
	var cyl := CylinderMesh.new()
	cyl.top_radius = radius
	cyl.bottom_radius = radius
	cyl.height = height
	mesh_inst.mesh = cyl
	mesh_inst.position = pos
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = 0.55
	if emissive:
		mat.emission_enabled = true
		mat.emission = color * 0.3
	_apply_zone_texture(mat, zone_id, tex_key, tex_key, tex_key)
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)


static func _apply_zone_texture(mat: StandardMaterial3D, zone_id: String, name_lower: String, parent_name: String, tex_override: String = "") -> void:
	var zone_tex: Dictionary = ZONE_TEXTURES.get(zone_id, {})
	if zone_tex.is_empty():
		return
	var key := tex_override if not tex_override.is_empty() else "ground"
	if tex_override.is_empty():
		if "water" in name_lower or "water" in parent_name:
			key = "accent" if zone_tex.has("accent") else "ground"
		elif "torii" in parent_name or "shack" in parent_name or "gate" in parent_name or "pillar" in name_lower:
			key = "structure"
		elif "ground" in parent_name or "floor" in parent_name or "tunnel" in parent_name:
			key = "ground"
		elif zone_id == "dragon_palace_gate":
			key = "structure"
		elif zone_id == "tidal_caves" and ("algae" in name_lower or randf() > 0.7):
			key = "accent"
	var path: String = zone_tex.get(key, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		return
	mat.albedo_texture = load(path)
	mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	mat.uv1_scale = Vector3(2, 2, 2)
