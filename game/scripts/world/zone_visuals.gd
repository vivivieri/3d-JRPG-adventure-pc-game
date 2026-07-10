class_name ZoneVisuals
extends RefCounted
## Applies zone palette, fog, and stylized materials to greybox world scenes.


const PALETTES := {
	"beach_shore": {
		"ground": Color("#C9B89A"),
		"structure": Color("#5C4A3A"),
		"accent": Color("#8B3A2A"),
		"water": Color("#1A5A6A"),
		"fog": Color("#8B9DAF"),
		"sky": Color("#8B9DAF"),
		"light": Color("#F0E0C8"),
	},
	"ruined_village": {
		"ground": Color("#C9B89A"),
		"structure": Color("#5C4A3A"),
		"accent": Color("#8B3A2A"),
		"moss": Color("#3D5C4A"),
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
			_add_torii(props, Vector3(-6, 0, -5), palette)
			_add_shack(props, Vector3(8, 0, -3), palette)
		"tidal_caves":
			for i in 4:
				_add_algae_strip(props, Vector3(-5 + i * 3.5, 1.2, 4), palette)
		"dragon_palace_gate":
			_add_gate_pillars(props, Vector3(0, 0, 12), palette)


static func _add_torii(parent: Node3D, pos: Vector3, palette: Dictionary) -> void:
	var torii := Node3D.new()
	torii.position = pos
	parent.add_child(torii)
	_add_box(torii, Vector3(-2.2, 2.5, 0), Vector3(0.35, 5, 0.35), palette.get("accent", Color.RED))
	_add_box(torii, Vector3(2.2, 2.5, 0), Vector3(0.35, 5, 0.35), palette.get("accent", Color.RED))
	_add_box(torii, Vector3(0, 4.8, 0), Vector3(5.2, 0.3, 0.35), palette.get("accent", Color.RED))
	_add_box(torii, Vector3(0, 3.8, 0), Vector3(4.4, 0.22, 0.28), palette.get("structure", Color.GRAY))


static func _add_shack(parent: Node3D, pos: Vector3, palette: Dictionary) -> void:
	var shack := Node3D.new()
	shack.position = pos
	parent.add_child(shack)
	_add_box(shack, Vector3(0, 1.2, 0), Vector3(3.5, 2.4, 3), palette.get("structure", Color.GRAY))
	_add_box(shack, Vector3(0, 2.6, 0), Vector3(4, 0.2, 3.4), palette.get("accent", Color.GRAY))


static func _add_algae_strip(parent: Node3D, pos: Vector3, palette: Dictionary) -> void:
	_add_box(parent, pos, Vector3(0.15, 2.5, 1.2), palette.get("accent", Color.CYAN), true)


static func _add_gate_pillars(parent: Node3D, pos: Vector3, palette: Dictionary) -> void:
	var gate := Node3D.new()
	gate.position = pos
	parent.add_child(gate)
	for x in [-4.0, 4.0]:
		_add_box(gate, Vector3(x, 4, 0), Vector3(1.2, 8, 1.2), palette.get("structure", Color.GOLD), true)
	_add_box(gate, Vector3(0, 7.5, 0), Vector3(10, 0.8, 1), palette.get("glow", Color.WHITE), true)


static func _add_box(parent: Node3D, pos: Vector3, size: Vector3, color: Color, emissive: bool = false) -> void:
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
		mat.emission = color * 0.2
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)
