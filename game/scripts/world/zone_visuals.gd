class_name ZoneVisuals
extends RefCounted
## Applies zone palette, fog, and stylized materials to greybox world scenes.


const PALETTES := {
	"beach_shore": {
		"ground": Color("#E4D4B0"),
		"structure": Color("#6A5A48"),
		"accent": Color("#2A8A7A"),
		"water": Color("#1A6A62"),
		"fog": Color("#9AB8C8"),
		"sky": Color("#8BB8C8"),
		"sky_top": Color("#5A98B0"),
		"sky_horizon": Color("#C8E0EC"),
		"ground_horizon": Color("#3A7888"),
		"light": Color("#F0E8D0"),
	},
	"ruined_village": {
		"ground": Color("#7A6A52"),
		"structure": Color("#5C4A3A"),
		"accent": Color("#8B3A2A"),
		"moss": Color("#4A6A48"),
		"water": Color("#1A4A5A"),
		"fog": Color("#8B9DAF"),
		"sky": Color("#8B9DAF"),
		"sky_top": Color("#4A7A9A"),
		"sky_horizon": Color("#B8D0E0"),
		"ground_horizon": Color("#6A8A9A"),
		"light": Color("#D4C4A8"),
	},
	"tidal_caves": {
		"ground": Color("#2A3238"),
		"structure": Color("#222830"),
		"accent": Color("#4AE8D8"),
		"water": Color("#1A4A5A"),
		"fog": Color("#0A141C"),
		"sky": Color("#0E1A22"),
		"sky_top": Color("#060C14"),
		"sky_horizon": Color("#1A3048"),
		"ground_horizon": Color("#142838"),
		"light": Color("#6EC8C0"),
	},
	"dragon_palace_gate": {
		"ground": Color("#E8E4DC"),
		"structure": Color("#D4A55A"),
		"accent": Color("#8B2A3A"),
		"glow": Color("#F0E8D0"),
		"fog": Color("#1A1A3A"),
		"sky": Color("#1A1A3A"),
		"sky_top": Color("#080818"),
		"sky_horizon": Color("#3A2868"),
		"ground_horizon": Color("#1A2858"),
		"light": Color("#FFD890"),
	},
}


const ZONE_TEXTURES := {
	"beach_shore": {
		"ground": "res://assets/textures/zones/beach_sand.png",
	},
	"ruined_village": {
		"ground": "res://assets/textures/zones/village_mud.png",
		"structure": "res://assets/textures/zones/village_wood.png",
	},
	"tidal_caves": {
		"ground": "res://assets/textures/zones/cave_wet_floor.png",
		"structure": "res://assets/textures/zones/cave_stone.png",
		"accent": "res://assets/textures/zones/cave_algae.png",
	},
	"dragon_palace_gate": {
		"ground": "res://assets/textures/zones/palace_marble.png",
		"structure": "res://assets/textures/zones/palace_gold.png",
		"glow": "res://assets/textures/zones/palace_gold.png",
	},
}


static func _screenshot_mode() -> bool:
	return OS.has_environment("SCREENSHOT_MODE")


static func apply_to_scene(root: Node3D, zone_id: String) -> void:
	var palette: Dictionary = PALETTES.get(zone_id, PALETTES.ruined_village)
	_apply_environment(root, palette, zone_id)
	_hide_greybox_meshes(root)
	_refine_water_meshes(root)
	_upgrade_water_boxes(root)
	_hide_all_box_meshes(root)
	_tint_meshes(root, palette, zone_id)
	_add_zone_props(root, zone_id, palette)
	_add_ground_cover(root, zone_id, palette)
	_add_zone_backdrop(root, zone_id, palette)


static func _hide_greybox_meshes(node: Node) -> void:
	if node is MeshInstance3D:
		var mesh := node as MeshInstance3D
		if _is_greybox_mesh(mesh):
			mesh.visible = false
			mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for child in node.get_children():
		_hide_greybox_meshes(child)


static func _is_greybox_mesh(mesh: MeshInstance3D) -> bool:
	var self_name := mesh.name.to_lower()
	var parent_name := mesh.get_parent().name.to_lower() if mesh.get_parent() else ""
	if self_name != "mesh" and self_name != "water":
		return false
	if parent_name == "ground" or "floor" in parent_name or "tunnel" in parent_name:
		return true
	if "flood" in parent_name or "barrier" in parent_name:
		return true
	if parent_name == "waterpuzzle" and self_name == "water":
		return false
	return false


static func _refine_water_meshes(node: Node) -> void:
	if node is MeshInstance3D and node.get_parent() and node.get_parent().name == "Water":
		var box := node.mesh as BoxMesh
		if box:
			box.size.y = 0.06
	if node is MeshInstance3D and "water" in node.name.to_lower():
		var box := node.mesh as BoxMesh
		if box:
			box.size.y = minf(box.size.y, 0.08)
	for child in node.get_children():
		_refine_water_meshes(child)


static func _make_water_plane(size: Vector2) -> PlaneMesh:
	var plane := PlaneMesh.new()
	plane.size = size
	plane.orientation = PlaneMesh.FACE_Y
	return plane


static func _upgrade_water_boxes(node: Node) -> void:
	if node is MeshInstance3D and node.name == "Water":
		var box := node.mesh as BoxMesh
		if box:
			var puzzle_parent := node.get_parent()
			if puzzle_parent and puzzle_parent.name == "WaterPuzzle":
				node.mesh = TerrainShapes.flood_pool_mesh(box.size.x * 0.46, box.size.z * 0.46)
			else:
				node.mesh = _make_water_plane(Vector2(box.size.x, box.size.z))
			node.rotation_degrees = Vector3.ZERO
	for child in node.get_children():
		_upgrade_water_boxes(child)


static func _hide_all_box_meshes(node: Node) -> void:
	if node is MeshInstance3D:
		var inst := node as MeshInstance3D
		if inst.mesh is BoxMesh:
			inst.visible = false
			inst.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for child in node.get_children():
		_hide_all_box_meshes(child)


static func _add_ground_cover(root: Node3D, zone_id: String, palette: Dictionary) -> void:
	if root.get_node_or_null("GroundCover"):
		return
	var cover := Node3D.new()
	cover.name = "GroundCover"
	root.add_child(cover)
	match zone_id:
		"beach_shore":
			_add_organic_ground(cover, palette, zone_id, "beach")
			_add_wet_sand_band(cover, palette)
			_scatter_beach_flora(cover, Vector3(0, 0, 6), 9.0, 6.0, 6 if _screenshot_mode() else 10)
			_scatter_rocks(cover, Vector3(0, 0, 3), 8.0, 5.5, 10 if _screenshot_mode() else 16, false)
			_add_beach_shoreline_dressing(cover, palette)
		"ruined_village":
			_add_organic_ground(cover, palette, zone_id, "hub")
			_add_village_planting_groups(cover)
			_scatter_rocks(cover, Vector3(0, 0, 0), 15.0, 18.0, 2 if _screenshot_mode() else 4, false)
			_add_ground_edge_breakup(cover, Vector2(21, 21), palette, zone_id)
		"tidal_caves":
			_add_organic_ground(cover, palette, zone_id, "cave")
			_scatter_cave_flora(cover, Vector3(0, 0, -8), 6.0, 21.0, 4 if _screenshot_mode() else 9)
			_scatter_cave_boulders(cover, Vector3(0, 0, -10), 6.0, 24.0, 2 if _screenshot_mode() else 5)
			_add_cave_wet_patches(cover, palette, zone_id)
		"dragon_palace_gate":
			_add_organic_ground(cover, palette, zone_id, "palace")
			_add_palace_court_plaza(cover, palette)


static func _scatter_path_strip(
	parent: Node3D,
	origin: Vector3,
	count: int,
	spacing: float,
	rot_y: float = 0.0,
) -> void:
	var tangent := Vector3.FORWARD.rotated(Vector3.UP, deg_to_rad(rot_y))
	for i in count:
		var jitter := Vector3(randf_range(-0.25, 0.25), 0, randf_range(-0.25, 0.25))
		var kind := "rock_small_a" if i % 2 == 0 else "log"
		PropLibrary.spawn(
			kind,
			parent,
			origin + tangent * (i - count * 0.5) * spacing + jitter,
			rot_y + randf_range(-8, 8),
			randf_range(0.75, 1.0),
			true,
		)


static func _add_playable_ground(parent: Node3D, palette: Dictionary, zone_id: String, size: Vector2) -> void:
	var mesh_inst := MeshInstance3D.new()
	mesh_inst.name = "PlayableGround"
	var plane := PlaneMesh.new()
	plane.size = size
	mesh_inst.mesh = plane
	mesh_inst.position = Vector3(0, -0.22, -6 if zone_id == "tidal_caves" else 0)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = palette.get("ground", Color.GRAY)
	mat.roughness = 0.88
	_apply_zone_texture(mat, zone_id, "ground", "ground", "ground")
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)


static func _add_organic_ground(
	parent: Node3D,
	palette: Dictionary,
	zone_id: String,
	shape: String,
) -> void:
	var mesh_inst := MeshInstance3D.new()
	mesh_inst.name = "PlayableGround"
	match shape:
		"beach":
			mesh_inst.mesh = TerrainShapes.beach_sand_mesh(13.0, 14.0, -5.0)
			mesh_inst.position = Vector3(0, 0.02, 0)
		"hub":
			mesh_inst.mesh = TerrainShapes.hub_ground_mesh(22.0, 22.0)
			mesh_inst.position = Vector3(0, 0.03, 0)
		"cave":
			mesh_inst.mesh = TerrainShapes.cave_path_mesh(-30.0, 15.0)
			mesh_inst.position = Vector3(0, -0.2, -7.5)
		"palace":
			mesh_inst.mesh = TerrainShapes.palace_court_mesh(10.0, 28.0)
			mesh_inst.position = Vector3(0, 0.02, -6)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = palette.get("ground", Color.GRAY)
	mat.roughness = 0.88
	if shape == "beach":
		mat.albedo_color = palette.get("ground", Color.GRAY).lerp(Color("#F0E4C8"), 0.45)
		mat.roughness = 0.78
	elif shape == "hub":
		mat.albedo_color = palette.get("ground", Color.GRAY).lerp(Color("#6A5A42"), 0.25)
		mat.roughness = 0.92
	elif shape == "cave":
		mat.albedo_color = Color("#3A4448")
		mat.roughness = 0.62
		mat.metallic = 0.02
	elif shape == "palace":
		mat.albedo_color = Color("#F2EDE4")
		mat.roughness = 0.4
		mat.metallic = 0.06
	_apply_zone_texture(mat, zone_id, "ground", "ground", "ground")
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)


static func _add_dry_sand_field(parent: Node3D, palette: Dictionary) -> void:
	var sand := MeshInstance3D.new()
	sand.name = "DrySandField"
	var plane := PlaneMesh.new()
	plane.size = Vector2(20, 14)
	plane.orientation = PlaneMesh.FACE_Y
	sand.mesh = plane
	sand.position = Vector3(0, 0.04, 6.5)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("#E2D2A8")
	mat.roughness = 0.9
	_apply_zone_texture(mat, "beach_shore", "ground", "ground", "ground")
	sand.material_override = mat
	parent.add_child(sand)


static func _add_palace_court_plaza(parent: Node3D, palette: Dictionary) -> void:
	var plaza := MeshInstance3D.new()
	plaza.name = "PalaceCourtPlaza"
	var plane := PlaneMesh.new()
	plane.size = Vector2(22, 34)
	plane.orientation = PlaneMesh.FACE_Y
	plaza.mesh = plane
	plaza.position = Vector3(0, 0.06, 2)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("#F0EBE0")
	mat.roughness = 0.35
	mat.metallic = 0.08
	_apply_zone_texture(mat, "dragon_palace_gate", "ground", "ground", "ground")
	plaza.material_override = mat
	parent.add_child(plaza)


static func _add_wet_sand_band(parent: Node3D, palette: Dictionary) -> void:
	var wet := MeshInstance3D.new()
	wet.name = "WetSandBand"
	wet.mesh = TerrainShapes.wet_sand_band_mesh(13.0, 0.85, 32)
	wet.position = Vector3(0, 0.035, 0)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("#B8A880")
	mat.roughness = 0.35
	mat.metallic = 0.02
	_apply_zone_texture(mat, "beach_shore", "ground", "ground", "ground")
	wet.material_override = mat
	parent.add_child(wet)


static func _add_village_mud_patches(parent: Node3D, palette: Dictionary) -> void:
	for patch in [Vector3(-3, 0.02, 5), Vector3(6, 0.02, -4), Vector3(-8, 0.02, -2)]:
		var mud := MeshInstance3D.new()
		var plane := PlaneMesh.new()
		plane.size = Vector2(5.5, 4.5)
		plane.orientation = PlaneMesh.FACE_Y
		mud.mesh = plane
		mud.position = patch
		var mat := StandardMaterial3D.new()
		mat.albedo_color = Color("#6A5A42")
		mat.roughness = 0.95
		_apply_zone_texture(mat, "ruined_village", "ground", "ground", "ground")
		mud.material_override = mat
		parent.add_child(mud)


static func _add_cave_wet_patches(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	for spot in [Vector3(-4.6, 0.03, -18)]:
		var puddle := MeshInstance3D.new()
		puddle.mesh = TerrainShapes.flood_pool_mesh(0.9, 0.65, 12)
		puddle.position = spot
		WaterMaterial.apply_to_mesh(puddle, palette, zone_id, true)
		parent.add_child(puddle)


static func _add_village_planting_groups(parent: Node3D) -> void:
	var groups := [
		{
			"center": Vector3(-6.0, 0, 6.5),
			"spots": [Vector3(-0.8, 0, -0.6), Vector3(0.2, 0, -0.9), Vector3(0.9, 0, -0.2), Vector3(-0.2, 0, 0.6)],
		},
		{
			"center": Vector3(8.8, 0, -5.6),
			"spots": [Vector3(-0.9, 0, 0.2), Vector3(0.1, 0, -0.5), Vector3(1.0, 0, 0.4)],
		},
		{
			"center": Vector3(4.4, 0, 3.7),
			"spots": [Vector3(-0.7, 0, 0.4), Vector3(0.4, 0, 0.7), Vector3(0.8, 0, -0.4)],
		},
	]
	for group in groups:
		var center: Vector3 = group["center"]
		for spot in group["spots"]:
			PropLibrary.spawn("grass_small", parent, center + spot, randf_range(-18, 18), randf_range(0.7, 0.95), false)


static func _add_ground_edge_breakup(
	parent: Node3D,
	half_size: Vector2,
	palette: Dictionary,
	zone_id: String,
) -> void:
	for i in 24:
		var edge := i % 4
		var t := randf()
		var pos := Vector3.ZERO
		match edge:
			0:
				pos = Vector3(lerpf(-half_size.x, half_size.x, t), 0, -half_size.y)
			1:
				pos = Vector3(lerpf(-half_size.x, half_size.x, t), 0, half_size.y)
			2:
				pos = Vector3(-half_size.x, 0, lerpf(-half_size.y, half_size.y, t))
			3:
				pos = Vector3(half_size.x, 0, lerpf(-half_size.y, half_size.y, t))
		pos += Vector3(randf_range(-0.6, 0.6), 0, randf_range(-0.6, 0.6))
		var kind := "rock_small_b" if i % 2 == 0 else "rock_small_a"
		if PropLibrary.has_prop(kind):
			PropLibrary.spawn(kind, parent, pos, randf_range(0, 360), randf_range(0.8, 1.05), not _screenshot_mode())


static func _add_beach_shoreline_dressing(parent: Node3D, palette: Dictionary) -> void:
	for x in range(-11, 12):
		var sx := float(x) * 1.05
		var shore := TerrainShapes.beach_shore_pos(sx)
		var rock_z := shore.y - 0.35
		PropLibrary.spawn("rock_small_a", parent, Vector3(shore.x, 0, rock_z + 0.1), float(x * 13), randf_range(0.8, 0.95), false)
		if x % 3 == 0:
			PropLibrary.spawn("rock_large_a", parent, Vector3(shore.x, 0, rock_z), float(x * 11), randf_range(0.9, 1.15), false)
		if x % 5 == 0:
			PropLibrary.spawn("rock_large_b", parent, Vector3(shore.x + 0.4, 0, rock_z - 0.3), float(x * 7), randf_range(0.85, 1.05), false)
	for offset in [Vector3(-5, 0, 2.5), Vector3(4, 0, 1.8), Vector3(0, 0, 4.0)]:
		PropLibrary.spawn("log", parent, offset, randf_range(-20, 20), randf_range(0.75, 0.95), false)
		PropLibrary.spawn("rock_small_a", parent, offset + Vector3(0.5, 0, 0.3), randf_range(0, 360), 0.85, false)
	_add_wet_sand_ribbon(parent)


static func _spawn_vertical_log(parent: Node3D, pos: Vector3, scale_factor: float) -> void:
	var log_node := PropLibrary.spawn("log", parent, pos, 0.0, scale_factor, true)
	if log_node:
		log_node.rotation_degrees.x = 90.0


static func _add_palisade_enclosure(parent: Node3D, center: Vector3, half_x: float, half_z: float) -> void:
	var fence := Node3D.new()
	fence.name = "PalisadeEnclosure"
	fence.position = center
	parent.add_child(fence)
	var corners: Array = [
		Vector3(-half_x, 0, -half_z),
		Vector3(half_x, 0, -half_z),
		Vector3(half_x, 0, half_z),
		Vector3(-half_x, 0, half_z),
	]
	for i in 4:
		var a: Vector3 = corners[i]
		var b: Vector3 = corners[(i + 1) % 4]
		var edge_len := a.distance_to(b)
		var posts := maxi(2, int(edge_len / 0.85))
		for p in posts + 1:
			var t := float(p) / float(posts)
			var post_pos := a.lerp(b, t)
			_spawn_vertical_log(fence, post_pos + Vector3(0, 0.4, 0), 0.3)
		var mid := (a + b) * 0.5
		var yaw := rad_to_deg(atan2(b.x - a.x, b.z - a.z))
		PropLibrary.spawn("log", fence, mid + Vector3(0, 0.72, 0), yaw + 90.0, 0.72, false)
		PropLibrary.spawn("log", fence, mid + Vector3(0, 0.48, 0), yaw + 90.0, 0.68, false)


static func _add_village_pets(parent: Node3D) -> void:
	_spawn_village_pet(parent, Vector3(7.2, 0, -1.2), "cat")
	_spawn_village_pet(parent, Vector3(-4.8, 0, 8.5), "dog")


static func _spawn_village_pet(parent: Node3D, pos: Vector3, kind: String) -> void:
	var pet := Node3D.new()
	pet.name = "VillagePet_%s" % kind
	pet.position = pos
	parent.add_child(pet)
	match kind:
		"cat":
			_add_pet_part(pet, "body", Vector3(0, 0.09, 0), 0.1, Color("#A88A68"))
			_add_pet_part(pet, "head", Vector3(0.1, 0.15, 0), 0.065, Color("#B89470"))
			_add_pet_part(pet, "tail", Vector3(-0.12, 0.12, 0), 0.035, Color("#8A6A4A"))
		"chicken":
			_add_pet_part(pet, "body", Vector3(0, 0.1, 0), 0.1, Color("#E8D8B8"))
			_add_pet_part(pet, "head", Vector3(0.08, 0.16, 0), 0.06, Color("#F0E0C0"))
			_add_pet_part(pet, "comb", Vector3(0.08, 0.22, 0), 0.03, Color("#C04030"))
		"dog":
			_add_pet_part(pet, "body", Vector3(0, 0.11, 0), 0.12, Color("#7A5A3A"))
			_add_pet_part(pet, "head", Vector3(0.12, 0.17, 0), 0.075, Color("#8A6848"))
			_add_pet_part(pet, "ear", Vector3(0.1, 0.21, 0.04), 0.03, Color("#5C422C"))


static func _add_pet_part(parent: Node3D, part_name: String, pos: Vector3, radius: float, color: Color) -> void:
	var mesh_inst := MeshInstance3D.new()
	mesh_inst.name = part_name
	var sphere := SphereMesh.new()
	sphere.radius = radius
	sphere.height = radius * 2.0
	mesh_inst.mesh = sphere
	mesh_inst.position = pos
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = 0.82
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)


static func _add_wet_sand_ribbon(parent: Node3D) -> void:
	for x in range(-10, 11):
		var sx := float(x) * 1.05
		var shore := TerrainShapes.beach_shore_pos(sx)
		var wet_z := shore.y + 0.55
		if x % 2 == 0:
			PropLibrary.spawn("grass_leafs", parent, Vector3(shore.x + 0.25, 0, wet_z), float(x * 9), 0.85, false)
		PropLibrary.spawn("rock_small_b", parent, Vector3(shore.x, 0, wet_z - 0.15), float(x * 11), 0.7, false)


static func _is_beach_inland(pos: Vector3) -> bool:
	return pos.z > TerrainShapes.beach_shoreline_z(pos.x) + 0.85


static func _is_cave_dry_ground(pos: Vector3) -> bool:
	if pos.z > -2.0 and absf(pos.x) < 2.8:
		return false
	if pos.z > -12.5 and pos.x > 1.8 and pos.x < 6.8 and pos.z > -11.5 and pos.z < -4.5:
		return false
	return true


static func _scatter_grass_field(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
	prefer_hd: bool = true,
) -> void:
	_scatter_flora_kinds(parent, center, radius_x, radius_z, count, ["grass_small", "grass", "grass_leafs"], prefer_hd)


static func _scatter_beach_flora(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
) -> void:
	_scatter_flora_kinds(
		parent,
		center,
		radius_x,
		radius_z,
		count,
		["grass_leafs", "grass_small"],
		false,
		0.7,
		0.95,
		Callable(ZoneVisuals, "_is_beach_inland"),
	)


static func _scatter_cave_flora(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
) -> void:
	_scatter_flora_kinds(
		parent,
		center,
		radius_x,
		radius_z,
		count,
		["grass", "grass_leafs", "grass"],
		false,
		1.05,
		1.45,
		Callable(ZoneVisuals, "_is_cave_dry_ground"),
	)


static func _scatter_village_flora(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
) -> void:
	_scatter_flora_kinds(
		parent,
		center,
		radius_x,
		radius_z,
		count,
		["grass_small", "grass"],
		false,
		0.85,
		1.15,
	)


static func _scatter_flora_kinds(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
	kinds: Array,
	prefer_hd: bool = true,
	scale_min: float = 0.9,
	scale_max: float = 1.35,
	placement_filter: Callable = Callable(),
) -> void:
	if kinds.is_empty():
		return
	var placed := 0
	var attempts := 0
	var max_attempts := count * 6
	while placed < count and attempts < max_attempts:
		attempts += 1
		var kind: String = kinds[placed % kinds.size()]
		if not PropLibrary.has_prop(kind):
			continue
		var x := center.x + randf_range(-radius_x, radius_x)
		var z := center.z + randf_range(-radius_z, radius_z)
		var pos := Vector3(x, 0, z)
		if placement_filter.is_valid() and not placement_filter.call(pos):
			continue
		PropLibrary.spawn(
			kind,
			parent,
			pos,
			randf_range(0, 360),
			randf_range(scale_min, scale_max),
			prefer_hd,
		)
		placed += 1


static func _scatter_cave_boulders(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
) -> void:
	var kinds := ["rock_tall_a", "rock_tall_b", "rock_large_a", "rock_large_b"]
	for i in count:
		var kind: String = kinds[i % kinds.size()]
		if not PropLibrary.has_prop(kind):
			continue
		var x := center.x + randf_range(-radius_x, radius_x)
		var z := center.z + randf_range(-radius_z, radius_z)
		var pos := Vector3(x, 0, z)
		if absf(pos.x) < 4.0:
			pos.x = signf(randf_range(-1.0, 1.0)) * randf_range(4.2, 6.5)
		PropLibrary.spawn(kind, parent, pos, randf_range(0, 360), randf_range(0.9, 1.25), false)


static func _scatter_rocks(
	parent: Node3D,
	center: Vector3,
	radius_x: float,
	radius_z: float,
	count: int,
	prefer_hd: bool = true,
) -> void:
	var kinds := ["rock_small_a", "rock_small_b", "rock_large_a", "stump"]
	for i in count:
		var kind: String = kinds[i % kinds.size()]
		if not PropLibrary.has_prop(kind):
			continue
		var x := center.x + randf_range(-radius_x, radius_x)
		var z := center.z + randf_range(-radius_z, radius_z)
		PropLibrary.spawn(kind, parent, Vector3(x, 0, z), randf_range(0, 360), randf_range(0.75, 1.2), prefer_hd)


static func _apply_environment(root: Node3D, palette: Dictionary, zone_id: String) -> void:
	var env_node := root.get_node_or_null("WorldEnvironment") as WorldEnvironment
	if env_node == null:
		env_node = WorldEnvironment.new()
		env_node.name = "WorldEnvironment"
		root.add_child(env_node)
	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	env.sky = _make_zone_sky(palette, zone_id)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = palette.get("light", Color.WHITE) * 0.4
	env.fog_enabled = true
	env.fog_light_color = palette.get("fog", Color.GRAY)
	env.fog_sky_affect = 0.85
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	match zone_id:
		"beach_shore":
			env.fog_density = 0.01
			env.fog_aerial_perspective = 0.78
		"ruined_village":
			env.fog_density = 0.008
			env.fog_aerial_perspective = 0.72
		"tidal_caves":
			env.fog_density = 0.028
			env.fog_aerial_perspective = 0.48
			env.ambient_light_color = palette.get("light", Color.WHITE) * 0.22
		"dragon_palace_gate":
			env.fog_density = 0.012
			env.fog_aerial_perspective = 0.68
			env.glow_enabled = true
			env.glow_intensity = 0.35
			env.glow_bloom = 0.18
		_:
			env.fog_density = 0.012
			env.fog_aerial_perspective = 0.5
	env_node.environment = env
	for child in root.get_children():
		if child is DirectionalLight3D:
			child.light_color = palette.get("light", Color.WHITE)
			child.light_energy = 1.05 if zone_id == "dragon_palace_gate" else 0.9
			if zone_id == "ruined_village" or zone_id == "beach_shore":
				child.rotation_degrees = Vector3(-48, -35, 0)


static func _make_zone_sky(palette: Dictionary, zone_id: String) -> Sky:
	var sky := Sky.new()
	var mat := ProceduralSkyMaterial.new()
	mat.sky_top_color = palette.get("sky_top", palette.get("sky", Color("#4A7A9A")))
	mat.sky_horizon_color = palette.get("sky_horizon", palette.get("sky", Color("#A8C4D4")))
	mat.ground_horizon_color = palette.get("ground_horizon", palette.get("water", Color("#1A4A5A")))
	mat.ground_bottom_color = palette.get("water", Color("#0E2838"))
	mat.sky_curve = 0.18
	mat.ground_curve = 0.04
	match zone_id:
		"beach_shore":
			mat.sun_angle_max = 32.0
			mat.sun_curve = 0.1
		"ruined_village":
			mat.sun_angle_max = 28.0
			mat.sun_curve = 0.12
			mat.ground_horizon_color = palette.get("ground", Color("#7A6A52")).lerp(
				palette.get("sky_horizon", Color("#B8D0E0")),
				0.35,
			)
			mat.ground_bottom_color = palette.get("ground", Color("#6A5A42")).lerp(
				palette.get("moss", Color("#4A6A48")),
				0.2,
			)
		"tidal_caves":
			mat.sun_angle_max = 0.0
			mat.sky_curve = 0.08
			mat.ground_horizon_color = Color("#111C24")
			mat.ground_bottom_color = Color("#071017")
		"dragon_palace_gate":
			mat.sun_angle_max = 8.0
			mat.sun_curve = 0.25
	sky.sky_material = mat
	return sky


static func _add_zone_backdrop(root: Node3D, zone_id: String, palette: Dictionary) -> void:
	if root.get_node_or_null("ZoneBackdrop"):
		return
	var backdrop := Node3D.new()
	backdrop.name = "ZoneBackdrop"
	root.add_child(backdrop)
	match zone_id:
		"beach_shore":
			_add_beach_backdrop(backdrop, palette)
		"ruined_village":
			_add_village_backdrop(backdrop, palette)
		"tidal_caves":
			_add_cave_backdrop(backdrop, palette)
		"dragon_palace_gate":
			_add_palace_backdrop(backdrop, palette)


static func _add_village_backdrop(parent: Node3D, palette: Dictionary) -> void:
	_add_horizon_plane(
		parent,
		Vector3(0, -1.2, -72),
		Vector2(240, 8),
		palette.get("ground", Color("#6A5A42")).lerp(palette.get("moss", Color("#4A6A48")), 0.25),
		0.92,
	)
	_add_horizon_plane(
		parent,
		Vector3(0, -1.35, -78),
		Vector2(260, 14),
		palette.get("water", Color("#1A4A5A")),
		0.45,
	)
	_add_distant_hills(parent, palette)
	if _screenshot_mode():
		return
	var hd_trees := ["tree_coastal_a", "tree_coastal_b"]
	for i in 2:
		var tree_id: String = hd_trees[i % hd_trees.size()]
		if not PropLibrary.has_prop(tree_id):
			continue
		var angle := float(i) / 2.0 * TAU + 0.6
		var radius := 46.0
		var x := cos(angle) * radius
		var z := sin(angle) * radius - 10.0
		PropLibrary.spawn(tree_id, parent, Vector3(x, 0, z), rad_to_deg(angle) + 90.0, randf_range(1.1, 1.35))


static func _add_coastal_backdrop(parent: Node3D, palette: Dictionary) -> void:
	_add_horizon_plane(parent, Vector3(0, -0.72, -62), Vector2(220, 6), palette.get("water", Color("#142E38")), 0.5)
	if _screenshot_mode():
		return
	var hd_trees := ["tree_coastal_a", "tree_coastal_b"]
	for i in 2:
		var tree_id: String = hd_trees[i % hd_trees.size()]
		if not PropLibrary.has_prop(tree_id):
			continue
		var angle := float(i) / 2.0 * TAU + 0.6
		var radius := 46.0
		var x := cos(angle) * radius
		var z := sin(angle) * radius - 10.0
		PropLibrary.spawn(tree_id, parent, Vector3(x, 0, z), rad_to_deg(angle) + 90.0, randf_range(1.1, 1.35))


static func _add_cave_backdrop(parent: Node3D, palette: Dictionary) -> void:
	for z in range(-40, 12, 18):
		PropLibrary.spawn("rock_large_b", parent, Vector3(-15, 0, z), 20.0, 1.0, true)
		PropLibrary.spawn("rock_large_a", parent, Vector3(15, 0, z), -20.0, 1.05, true)
	for x in [-16, 16]:
		for z in [-34, -10]:
			PropLibrary.spawn("rock_small_b", parent, Vector3(x, 0, z), randf_range(0, 360), randf_range(0.75, 0.9), true)
	_add_horizon_plane(parent, Vector3(0, -0.5, -44), Vector2(80, 20), palette.get("sky", Color("#0E1A22")), 0.9)


static func _add_palace_backdrop(parent: Node3D, palette: Dictionary) -> void:
	_add_horizon_plane(
		parent,
		Vector3(0, -10.0, -42),
		Vector2(140, 90),
		palette.get("ground_horizon", Color("#1A2858")),
		0.35,
		false,
	)
	for side in [-1, 1]:
		for z in [-28, -8, 12]:
			PropLibrary.spawn(
				"castle_tower_base",
				parent,
				Vector3(side * 22.0, 0, z),
				90.0 if side > 0 else -90.0,
				1.15,
			)
	for i in 8:
		_add_star_glow(
			parent,
			Vector3(randf_range(-35, 35), randf_range(20, 32), randf_range(-35, 20)),
		)


static func _add_horizon_plane(
	parent: Node3D,
	pos: Vector3,
	size: Vector2,
	color: Color,
	roughness: float,
	emissive: bool = false,
	emission: Color = Color.BLACK,
) -> void:
	var mesh_inst := MeshInstance3D.new()
	var plane := PlaneMesh.new()
	plane.size = size
	mesh_inst.mesh = plane
	mesh_inst.position = pos
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = roughness
	mat.metallic = 0.05
	if emissive:
		mat.emission_enabled = true
		mat.emission = emission
	mesh_inst.material_override = mat
	parent.add_child(mesh_inst)


static func _add_star_glow(parent: Node3D, pos: Vector3) -> void:
	var orb := MeshInstance3D.new()
	var sphere := SphereMesh.new()
	sphere.radius = 0.12
	sphere.height = 0.24
	orb.mesh = sphere
	orb.position = pos
	var mat := StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = Color("#FFF8E8")
	mat.emission_enabled = true
	mat.emission = Color("#FFD890") * 0.8
	orb.material_override = mat
	parent.add_child(orb)


static func _tint_meshes(node: Node, palette: Dictionary, zone_id: String) -> void:
	if node is MeshInstance3D:
		var mesh := node as MeshInstance3D
		if not mesh.visible:
			for child in node.get_children():
				_tint_meshes(child, palette, zone_id)
			return
		var mat := StandardMaterial3D.new()
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_PER_PIXEL
		var name_lower := node.name.to_lower()
		var parent_name := node.get_parent().name.to_lower() if node.get_parent() else ""
		if "water" in name_lower or "water" in parent_name:
			WaterMaterial.apply_to_mesh(mesh, palette, zone_id, "puddle" in parent_name)
			for child in node.get_children():
				_tint_meshes(child, palette, zone_id)
			return
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
		elif zone_id == "tidal_caves" and "algae" in name_lower:
			mat.albedo_color = palette.get("ground", Color.GRAY)
			mat.emission_enabled = true
			mat.emission = palette.get("accent", Color.CYAN) * 0.18
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
		"beach_shore":
			_add_beach_set(props, palette, zone_id)
		"ruined_village":
			_add_village_set(props, palette, zone_id)
		"tidal_caves":
			_add_caves_set(props, palette, zone_id)
		"dragon_palace_gate":
			_add_palace_set(props, palette, zone_id)


static func _add_village_set(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	_add_torii(parent, Vector3(-6, 0, -5), palette, zone_id)
	_add_shack(parent, Vector3(8, 0, -3), palette, zone_id)
	_add_palisade_enclosure(parent, Vector3(8, 0, -3), 2.8, 2.2)
	_add_well(parent, Vector3(5, 0, 2), palette, zone_id)
	_add_pier(parent, Vector3(-8, 0, 6), palette, zone_id)
	_add_coastline(parent, palette, zone_id)
	_add_rock_cluster(parent, Vector3(-12, 0, -3), palette, zone_id)
	_add_rock_cluster(parent, Vector3(-6, 0, 11), palette, zone_id)
	_add_broken_fence(parent, Vector3(12, 0, 8), palette, zone_id)
	_add_festival_banner_prop(parent, Vector3(-2, 0, 6), palette, zone_id)
	_add_sandal_puddle(parent, Vector3(1.5, 0, 3.5), palette, zone_id)
	_add_village_pets(parent)
	var hero_trees: Array = []
	if _screenshot_mode():
		hero_trees = [
			["tree_pine", -14, 4, 25.0, 1.35],
			["tree_pine", 12, -6, -40.0, 1.25],
			["tree_pine", -8, -10, 15.0, 1.3],
			["tree_pine", 14, 2, -55.0, 1.2],
		]
	else:
		hero_trees = [
			["pine_hd", -14, 4, 25.0, 1.35],
			["fir_hd", 12, -6, -40.0, 1.25],
			["pine_hd", -8, -10, 15.0, 1.3],
			["tree_coastal_a", 14, 2, -55.0, 1.2],
		]
	for spot in hero_trees:
		if PropLibrary.has_prop(spot[0]):
			PropLibrary.spawn(spot[0], parent, Vector3(spot[1], 0, spot[2]), spot[3], spot[4], not _screenshot_mode())

static func _add_caves_set(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	_add_cave_tunnel_walls(parent, palette, zone_id)
	_add_cave_wall_flora(parent)
	_add_cave_big_leaf_clusters(parent)
	for i in 2:
		_add_algae_strip(parent, Vector3(-5.0 + i * 5.0, 0.45, -1.5 - i * 4.0), palette, zone_id)
	_add_flood_pool_frame(parent, Vector3(4.0, 0, -7.5), palette, zone_id)
	_add_flood_chamber_wetness(parent, Vector3(4.0, 0, -7.5), palette, zone_id)
	_add_deep_pool_faces(parent, Vector3(0, 0, -16), palette)
	_add_shrine_alcove(parent, Vector3(0, 0, -28), palette, zone_id)
	for z in range(-24, 10, 16):
		PropLibrary.spawn("rock_tall_a", parent, Vector3(-6.5, 0, z), 20.0, 1.0, false)
		PropLibrary.spawn("rock_tall_b", parent, Vector3(6.5, 0, z - 1), -20.0, 1.05, false)
		PropLibrary.spawn("mushroom_tan", parent, Vector3(-4.8, 0, z + 0.5), 0.0, 0.75, false)


static func _add_cave_wall_flora(parent: Node3D) -> void:
	for z in range(-24, 10, 12):
		PropLibrary.spawn("grass", parent, Vector3(-5.9, 0, z), 25.0, 0.95, false)
		PropLibrary.spawn("grass_leafs", parent, Vector3(5.8, 0, z + 1.0), -20.0, 0.9, false)


static func _add_cave_big_leaf_clusters(parent: Node3D) -> void:
	for spot in [Vector3(-5.0, 0, -13), Vector3(5.0, 0, -20)]:
		PropLibrary.spawn("grass", parent, spot, randf_range(0, 360), 1.15, false)
		PropLibrary.spawn("grass_leafs", parent, spot + Vector3(0.6, 0, 0.4), randf_range(0, 360), 1.0, false)


static func _add_flood_chamber_wetness(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var chamber := Node3D.new()
	chamber.name = "FloodChamberWetness"
	chamber.position = pos
	parent.add_child(chamber)
	for offset in [Vector3(-1.2, 0.02, 0.8), Vector3(0.8, 0.02, -0.6), Vector3(0, 0.02, 1.2)]:
		var drip := MeshInstance3D.new()
		drip.mesh = _make_water_plane(Vector2(0.9, 0.7))
		drip.position = offset
		WaterMaterial.apply_to_mesh(drip, palette, zone_id, true)
		chamber.add_child(drip)
	var light := OmniLight3D.new()
	light.light_color = palette.get("accent", Color.CYAN)
	light.light_energy = 0.45
	light.omni_range = 6.0
	light.position = Vector3(0, 1.2, 0)
	chamber.add_child(light)


static func _add_flood_pool_frame(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var frame := Node3D.new()
	frame.name = "FloodPoolFrame"
	frame.position = pos
	parent.add_child(frame)
	for angle_deg in [35.0, 145.0, 215.0]:
		var angle := deg_to_rad(angle_deg)
		PropLibrary.spawn("rock_large_b", frame, Vector3(cos(angle) * 2.4, 0, sin(angle) * 1.8), angle_deg, 0.85, false)
		PropLibrary.spawn("rock_small_a", frame, Vector3(cos(angle) * 1.5, 0, sin(angle) * 1.1), angle_deg + 20.0, 0.8, false)
	PropLibrary.spawn("rock_large_a", frame, Vector3(-1.8, 0, 1.6), 60.0, 0.75, false)
	PropLibrary.spawn("mushroom_tan", frame, Vector3(2.0, 0, 1.4), -10.0, 0.9, false)
	PropLibrary.spawn("mushroom", frame, Vector3(-1.2, 0, -1.5), 30.0, 0.85, false)


static func _add_palace_set(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	_add_void_sea(parent, palette, zone_id)
	_add_gate_pillars(parent, Vector3(0, 0, 12), palette, zone_id)
	_add_palace_banners(parent, Vector3(0, 0, 12), palette, zone_id)
	_add_palace_lanterns(parent, Vector3(0, 0, 10), palette, zone_id)
	PropLibrary.spawn("castle_bridge", parent, Vector3(0, -0.35, 7), 0.0, 1.05)
	PropLibrary.spawn("castle_stairs", parent, Vector3(-4.5, 0, 9), 90.0, 1.05)
	PropLibrary.spawn("castle_stairs", parent, Vector3(4.5, 0, 9), -90.0, 1.05)
	PropLibrary.spawn("knight_red", parent, Vector3(-2.2, 0, 4), 35.0, 1.1)
	PropLibrary.spawn("knight_red", parent, Vector3(2.2, 0, 4), -35.0, 1.1)
	_add_palace_columns(parent, Vector3(0, 0, 2), palette, zone_id)
	_add_palace_banners(parent, Vector3(0, 0, 2), palette, zone_id)
	_add_palace_lanterns(parent, Vector3(0, 0, 2), palette, zone_id)
	_add_mirror_chamber(parent, Vector3(-4, 0, -8), palette, zone_id)
	_add_palace_section(parent, Vector3(0, 0, -18), palette, zone_id, true)
	_add_palace_section(parent, Vector3(0, 0, -30), palette, zone_id, false)


static func _add_torii(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var torii := Node3D.new()
	torii.name = "ToriiProp"
	torii.position = pos
	parent.add_child(torii)
	_spawn_vertical_log(torii, Vector3(-1.4, 0.9, 0), 0.42)
	_spawn_vertical_log(torii, Vector3(1.4, 0.9, 0), 0.42)
	PropLibrary.spawn("log", torii, Vector3(0, 2.6, 0), 90.0, 1.05, true)
	PropLibrary.spawn("log", torii, Vector3(0, 2.1, 0), 90.0, 0.95, true)
	PropLibrary.spawn("bush", torii, Vector3(0, 0, 0.8), 0.0, 0.9, true)


static func _add_shack(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var shack := Node3D.new()
	shack.name = "ShackProp"
	shack.position = pos
	parent.add_child(shack)
	PropLibrary.spawn("log_stack", shack, Vector3(-1.0, 0, -0.8), 0.0, 0.85, true)
	PropLibrary.spawn("log_stack", shack, Vector3(1.0, 0, -0.8), 180.0, 0.85, true)
	PropLibrary.spawn("log", shack, Vector3(-1.0, 0.6, 0.6), 25.0, 0.95, true)
	PropLibrary.spawn("log", shack, Vector3(1.0, 0.6, 0.6), -25.0, 0.95, true)
	PropLibrary.spawn("log", shack, Vector3(0, 1.1, 0.2), 0.0, 1.0, true)
	PropLibrary.spawn("bush", shack, Vector3(0, 0, 1.0), 0.0, 0.95, true)


static func _add_well(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var well := Node3D.new()
	well.name = "VillageWellProp"
	well.position = pos
	parent.add_child(well)
	for i in 6:
		var angle := float(i) / 6.0 * TAU
		PropLibrary.spawn("rock_small_a", well, Vector3(cos(angle) * 0.85, 0, sin(angle) * 0.85), rad_to_deg(angle), 0.9, true)
	var water := MeshInstance3D.new()
	water.name = "WellWater"
	water.mesh = _make_water_plane(Vector2(1.0, 1.0))
	water.position = Vector3(0, 0.04, 0)
	WaterMaterial.apply_to_mesh(water, palette, zone_id, true)
	well.add_child(water)
	PropLibrary.spawn("rock_large_b", well, Vector3(0.55, 0, 0.35), 20.0, 0.45, true)


static func _add_pier(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var pier := Node3D.new()
	pier.position = pos
	parent.add_child(pier)
	for i in 3:
		PropLibrary.spawn("log", pier, Vector3(i * 1.0, 0.06, 0), 90.0, 0.9, true)
	PropLibrary.spawn("bush", pier, Vector3(4.2, 0, 0.6), 0.0, 0.85, true)


static func _add_coastline(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	for x in range(-5, 6, 2):
		PropLibrary.spawn("rock_small_a", parent, Vector3(x * 2.2, 0, -11.5), float(x * 17), 0.75, true)
		if x % 4 == 0:
			PropLibrary.spawn("grass_small", parent, Vector3(x * 2.0, 0, -10.2), float(x * 23), 0.75, false)


static func _add_rock_cluster(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var rocks := Node3D.new()
	rocks.position = pos
	parent.add_child(rocks)
	PropLibrary.spawn("rock_large_a", rocks, Vector3(0, 0, 0), 20.0, 0.95, true)
	PropLibrary.spawn("rock_small_a", rocks, Vector3(1.2, 0, 0.8), -15.0, 0.85, true)
	PropLibrary.spawn("rock_small_b", rocks, Vector3(-0.8, 0, -0.5), 35.0, 0.8, true)


static func _add_distant_hills(parent: Node3D, palette: Dictionary) -> void:
	var hills := Node3D.new()
	hills.name = "DistantHills"
	parent.add_child(hills)
	for spot in [[-20, -28, 1.4], [18, -27, 1.3]]:
		PropLibrary.spawn("tree_coastal_b", hills, Vector3(spot[0], 0, spot[1]), float(spot[0]), spot[2]) if PropLibrary.has_prop("tree_coastal_b") else PropLibrary.spawn("tree_pine", hills, Vector3(spot[0], 0, spot[1]), float(spot[0]), spot[2], false)


static func _add_broken_fence(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var fence := Node3D.new()
	fence.name = "BrokenFenceProp"
	fence.position = pos
	parent.add_child(fence)
	PropLibrary.spawn("stump", fence, Vector3(0, 0, 0), 15.0, 0.75, true)
	PropLibrary.spawn("log", fence, Vector3(2.5, 0.05, 0.2), 15.0, 0.85, true)
	PropLibrary.spawn("log", fence, Vector3(4.0, 0, -0.3), 80.0, 0.9, true)
	PropLibrary.spawn("rock_small_b", fence, Vector3(1.2, 0, 0.5), 20.0, 0.85, true)


static func _add_cave_tunnel_walls(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	for z in range(-28, 14, 5):
		PropLibrary.spawn("rock_large_b", parent, Vector3(-9.0, 0, z), 90.0, 0.75, true)
		PropLibrary.spawn("rock_large_a", parent, Vector3(9.0, 0, z), -90.0, 0.8, true)
		PropLibrary.spawn("rock_small_a", parent, Vector3(-7.5, 0, z + 1.5), 30.0, 0.9, true)
		PropLibrary.spawn("rock_small_b", parent, Vector3(7.5, 0, z - 1.5), -30.0, 0.85, true)


static func _add_cave_pool_glow(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var pool := Node3D.new()
	pool.position = pos
	parent.add_child(pool)
	var water := MeshInstance3D.new()
	water.name = "PoolWater"
	water.mesh = TerrainShapes.flood_pool_mesh(3.6, 2.4, 20)
	water.position = Vector3(0, -0.04, -2)
	WaterMaterial.apply_to_mesh(water, palette, zone_id)
	pool.add_child(water)
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
	for side in [-5.5, 5.5]:
		_spawn_vertical_log(banners, Vector3(side, 1.2, 0.6), 0.35)
		PropLibrary.spawn("branches", banners, Vector3(side + 0.15, 2.0, 0.7), 0.0 if side < 0 else 180.0, 1.05, true)


static func _add_void_sea(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	var sea := Node3D.new()
	sea.name = "VoidSea"
	parent.add_child(sea)
	for z in [12, 2, -8, -18, -30]:
		var light := OmniLight3D.new()
		light.light_color = palette.get("accent", Color.CYAN)
		light.light_energy = 0.55
		light.omni_range = 12.0
		light.position = Vector3(0, -1.0, z)
		sea.add_child(light)


static func _add_mirror_chamber(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var chamber := Node3D.new()
	chamber.name = "MirrorChamberProp"
	chamber.position = pos
	parent.add_child(chamber)
	PropLibrary.spawn("castle_pillar", chamber, Vector3(-2.0, 0, 0), 0.0, 1.1)
	PropLibrary.spawn("castle_pillar", chamber, Vector3(2.0, 0, 0), 0.0, 1.1)
	PropLibrary.spawn("castle_arch", chamber, Vector3(0, 0, -1.0), 0.0, 1.05)
	var mirror := MeshInstance3D.new()
	mirror.name = "Mirror"
	var sphere := SphereMesh.new()
	sphere.radius = 1.35
	sphere.height = 2.7
	mirror.mesh = sphere
	mirror.position = Vector3(0, 1.9, 0.5)
	mirror.scale = Vector3(1.0, 1.25, 0.12)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("#A8D0E8")
	mat.metallic = 0.95
	mat.roughness = 0.04
	mat.emission_enabled = true
	mat.emission = palette.get("glow", Color.WHITE) * 0.15
	mirror.material_override = mat
	chamber.add_child(mirror)
	_add_palace_lanterns(chamber, Vector3(0, 0, 0.8), palette, zone_id)


static func _add_palace_section(
	parent: Node3D,
	pos: Vector3,
	palette: Dictionary,
	zone_id: String,
	with_knights: bool,
) -> void:
	var section := Node3D.new()
	section.position = pos
	parent.add_child(section)
	_add_palace_banners(section, Vector3(0, 0, 0), palette, zone_id)
	_add_palace_lanterns(section, Vector3(0, 0, 0), palette, zone_id)
	PropLibrary.spawn("castle_pillar", section, Vector3(-4.0, 0, 0), 0.0, 1.15)
	PropLibrary.spawn("castle_pillar", section, Vector3(4.0, 0, 0), 0.0, 1.15)
	if with_knights:
		PropLibrary.spawn("knight_red", section, Vector3(-1.5, 0, 1.5), 20.0, 1.05)
		PropLibrary.spawn("knight_red", section, Vector3(1.5, 0, 1.5), -20.0, 1.05)
	else:
		PropLibrary.spawn("castle_arch", section, Vector3(0, 0, 1.5), 0.0, 1.25)
		PropLibrary.spawn("castle_tower_top", section, Vector3(0, 0, -1.5), 0.0, 1.1)


static func _add_palace_columns(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var hall := Node3D.new()
	hall.position = pos
	parent.add_child(hall)
	for x in [-5.0, -2.5, 2.5, 5.0]:
		PropLibrary.spawn("castle_pillar", hall, Vector3(x, 0, 0), 0.0, 1.3)
	PropLibrary.spawn("castle_tower_top", hall, Vector3(0, 0, -2), 0.0, 1.1)


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
	PropLibrary.spawn("grass_leafs", parent, pos, randf_range(0, 360), 1.1, false)
	PropLibrary.spawn("grass", parent, pos + Vector3(0.35, 0, 0.25), randf_range(0, 360), 1.0, false)


static func _add_gate_pillars(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var gate := Node3D.new()
	gate.name = "PalaceGate"
	gate.position = pos
	parent.add_child(gate)
	PropLibrary.spawn("castle_gate", gate, Vector3(0, 0, 0), 0.0, 1.25)
	PropLibrary.spawn("castle_metal_gate", gate, Vector3(0, 0, 1.0), 0.0, 1.1)


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


static func _add_beach_set(parent: Node3D, palette: Dictionary, zone_id: String) -> void:
	for offset in [Vector3(-4, 0, 6), Vector3(3, 0, 4), Vector3(-2, 0, 9), Vector3(5, 0, 7)]:
		PropLibrary.spawn("log", parent, offset, randf_range(-25, 25), randf_range(0.85, 1.1), true)
		PropLibrary.spawn("rock_small_a", parent, offset + Vector3(0.8, 0, 0.5), randf_range(0, 360), 0.9, true)
	_add_rock_cluster(parent, Vector3(-6, 0, 2), palette, zone_id)
	_add_rock_cluster(parent, Vector3(7, 0, 5), palette, zone_id)
	for x in range(-12, 13):
		var sx := float(x) * 1.05
		var shore := TerrainShapes.beach_shore_pos(sx)
		PropLibrary.spawn("rock_small_b", parent, Vector3(shore.x, 0, shore.y - 0.55), float(x * 9), randf_range(0.7, 0.95), false)


static func _add_beach_backdrop(parent: Node3D, palette: Dictionary) -> void:
	var surf := MeshInstance3D.new()
	surf.name = "SurfWater"
	surf.mesh = TerrainShapes.beach_surf_water_mesh(13.0, 11.0, 32)
	WaterMaterial.apply_to_mesh(surf, palette, "beach_shore")
	parent.add_child(surf)
	for x in range(-11, 12):
		var sx := float(x) * 1.15
		var shore := TerrainShapes.beach_shore_pos(sx)
		var rock_z := shore.y - 1.1
		PropLibrary.spawn("rock_small_b", parent, Vector3(shore.x, 0, rock_z), float(x * 11), randf_range(0.85, 1.1), false)
		if x % 3 == 0:
			PropLibrary.spawn("rock_large_a", parent, Vector3(shore.x, 0, rock_z - 0.9), float(x * 7), 0.75, false)


static func _add_festival_banner_prop(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var banner := Node3D.new()
	banner.name = "FestivalBannerProp"
	banner.position = pos
	parent.add_child(banner)
	PropLibrary.spawn("stump", banner, Vector3(0, 0, 0), 12.0, 0.7, true)
	PropLibrary.spawn("log", banner, Vector3(0.35, 0.06, 0.15), 72.0, 0.55, true)
	PropLibrary.spawn("branches", banner, Vector3(0.2, 0.55, 0.05), 18.0, 1.05, true)
	PropLibrary.spawn("bush", banner, Vector3(-0.35, 0, 0.35), 35.0, 0.75, true)
	PropLibrary.spawn("rock_small_b", banner, Vector3(0.55, 0, 0.45), 30.0, 0.8, true)


static func _add_sandal_puddle(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var puddle := Node3D.new()
	puddle.name = "SandalPuddle"
	puddle.position = pos
	parent.add_child(puddle)
	var water := MeshInstance3D.new()
	water.name = "PuddleWater"
	water.mesh = _make_water_plane(Vector2(2.0, 1.6))
	water.position = Vector3(0, 0.02, 0)
	WaterMaterial.apply_to_mesh(water, palette, zone_id, true)
	puddle.add_child(water)
	if PropLibrary.has_prop("canoe_paddle"):
		PropLibrary.spawn("canoe_paddle", puddle, Vector3(0.15, 0.05, 0.05), 32.0, 0.38, true)
	else:
		PropLibrary.spawn("log", puddle, Vector3(0.05, 0.04, 0), 25.0, 0.28, true)
	PropLibrary.spawn("rock_small_a", puddle, Vector3(-0.55, 0, 0.35), -20.0, 0.45, true)
	PropLibrary.spawn("rock_small_a", puddle, Vector3(0.45, 0, -0.25), 15.0, 0.4, true)
	PropLibrary.spawn("grass_small", puddle, Vector3(-0.7, 0, -0.35), 40.0, 0.65, false)


static func _add_deep_pool_faces(parent: Node3D, pos: Vector3, palette: Dictionary) -> void:
	var vfx_script := load("res://scripts/world/pool_face_vfx.gd") as Script
	if vfx_script == null:
		return
	var faces := Node3D.new()
	faces.name = "DeepPoolFaces"
	faces.position = pos
	faces.set_script(vfx_script)
	parent.add_child(faces)


static func _add_shrine_alcove(parent: Node3D, pos: Vector3, palette: Dictionary, zone_id: String) -> void:
	var alcove := Node3D.new()
	alcove.name = "YuzuShrineAlcove"
	alcove.position = pos
	parent.add_child(alcove)
	PropLibrary.spawn("rock_large_b", alcove, Vector3(-2.8, 0, 0.2), 88.0, 1.05, true)
	PropLibrary.spawn("rock_large_a", alcove, Vector3(2.8, 0, 0.2), -88.0, 1.05, true)
	PropLibrary.spawn("rock_large_b", alcove, Vector3(0, 1.6, -1.8), 0.0, 0.95, true)
	_spawn_vertical_log(alcove, Vector3(-0.9, 0.9, 0.8), 0.38)
	_spawn_vertical_log(alcove, Vector3(0.9, 0.9, 0.8), 0.38)
	PropLibrary.spawn("log", alcove, Vector3(0, 1.7, 0.8), 90.0, 0.8, true)
	PropLibrary.spawn("log", alcove, Vector3(0, 1.35, 0.8), 90.0, 0.72, true)
	PropLibrary.spawn("bush", alcove, Vector3(0, 0, 1.5), 0.0, 0.85, true)
	PropLibrary.spawn("mushroom_tan", alcove, Vector3(-1.2, 0, 1.0), 25.0, 1.0, false)
	PropLibrary.spawn("mushroom", alcove, Vector3(1.2, 0, 1.0), -25.0, 0.95, false)
	var light := OmniLight3D.new()
	light.name = "ShrineGlow"
	light.light_color = palette.get("accent", Color.CYAN)
	light.light_energy = 1.15
	light.omni_range = 9.0
	light.position = Vector3(0, 2.0, 0.8)
	alcove.add_child(light)


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
		elif zone_id == "tidal_caves" and "algae" in name_lower:
			key = "accent"
	var path: String = zone_tex.get(key, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		return
	mat.albedo_texture = load(path)
	mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	mat.uv1_scale = Vector3(2, 2, 2)
