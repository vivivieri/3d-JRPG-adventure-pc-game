class_name JapaneseNatureMeshes
extends RefCounted
## High-polygon procedural Japanese natural-world meshes (torii, tōrō, bamboo, pine, rocks).


static func build_torii(vermillion: Color, wood: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "ToriiHD"
	for side in [-1.0, 1.0]:
		var pillar := _build_tapered_pillar(0.28, 0.22, 4.6, 24, vermillion)
		pillar.position = Vector3(side * 1.55, 0, 0)
		root.add_child(pillar)
	var kasagi := _build_curved_beam(3.8, 0.32, 0.38, 32, vermillion, 0.18)
	kasagi.position = Vector3(0, 4.55, 0)
	root.add_child(kasagi)
	var nuki := _build_curved_beam(3.2, 0.22, 0.28, 24, vermillion, 0.06)
	nuki.position = Vector3(0, 3.65, 0)
	root.add_child(nuki)
	var shimaki := _build_curved_beam(3.35, 0.16, 0.2, 20, wood.darkened(0.15), 0.04)
	shimaki.position = Vector3(0, 4.15, 0)
	root.add_child(shimaki)
	var rope := _build_shimenawa(Vector3(0, 4.35, 0), 1.35, vermillion.lightened(0.15))
	root.add_child(rope)
	return root


static func build_stone_lantern(stone: Color, glow: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "TorouHD"
	var base := _build_cylinder_mesh(0.75, 0.18, 20, stone)
	base.position = Vector3(0, 0.09, 0)
	root.add_child(base)
	var leg := _build_cylinder_mesh(0.42, 0.55, 18, stone.darkened(0.08))
	leg.position = Vector3(0, 0.45, 0)
	root.add_child(leg)
	var platform := _build_cylinder_mesh(0.58, 0.14, 20, stone.lightened(0.05))
	platform.position = Vector3(0, 0.82, 0)
	root.add_child(platform)
	var chamber := _build_lantern_chamber(0.48, 0.62, 16, stone, glow)
	chamber.position = Vector3(0, 1.25, 0)
	root.add_child(chamber)
	var roof := _build_lantern_roof(0.62, 0.38, 20, stone.darkened(0.12))
	roof.position = Vector3(0, 1.82, 0)
	root.add_child(roof)
	var finial := _build_cylinder_mesh(0.08, 0.22, 12, stone)
	finial.position = Vector3(0, 2.12, 0)
	root.add_child(finial)
	return root


static func build_bamboo_cluster(count: int, green: Color, ring: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "BambooCluster"
	for i in count:
		var stalk := _build_bamboo_stalk(green, ring)
		var angle := float(i) / float(count) * TAU + randf_range(-0.2, 0.2)
		var dist := randf_range(0.15, 0.55)
		stalk.position = Vector3(cos(angle) * dist, 0, sin(angle) * dist)
		stalk.rotation_degrees.y = randf_range(0, 360)
		stalk.scale = Vector3.ONE * randf_range(0.85, 1.15)
		root.add_child(stalk)
	return root


static func build_japanese_pine(trunk: Color, needle: Color, height: float = 5.5) -> Node3D:
	var root := Node3D.new()
	root.name = "PineHD"
	var trunk_mesh := _build_tapered_pillar(0.22, 0.14, height * 0.55, 16, trunk)
	trunk_mesh.position = Vector3(0, height * 0.27, 0)
	root.add_child(trunk_mesh)
	var tiers := 6
	for t in tiers:
		var tier_h := height * (0.38 + float(t) * 0.1)
		var spread := 1.45 - float(t) * 0.15
		var layer := _build_pine_needle_layer(spread, 0.58 - float(t) * 0.05, 36, needle.darkened(float(t) * 0.04))
		layer.position = Vector3(0, tier_h, 0)
		layer.rotation_degrees.y = float(t) * 37.0
		root.add_child(layer)
	return root


static func build_moss_rock(radius: float, base: Color, moss: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "MossRockHD"
	var body := _build_deformed_rock(radius, 3, base)
	root.add_child(body)
	for i in 6:
		var patch := _build_moss_patch(radius * randf_range(0.35, 0.75), moss)
		var dir := Vector3(randf_range(-1, 1), randf_range(0.2, 0.9), randf_range(-1, 1)).normalized()
		patch.position = dir * radius * 0.72
		patch.look_at(patch.position + dir, Vector3.UP)
		root.add_child(patch)
	return root


static func build_lacquer_box(color: Color, accent: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "LacquerBoxHD"
	var body := _build_box_mesh(Vector3(0.42, 0.28, 0.32), color, 0.25, 0.35)
	body.position = Vector3(0, 0.14, 0)
	root.add_child(body)
	var lid := _build_box_mesh(Vector3(0.44, 0.1, 0.34), color.lightened(0.08), 0.3, 0.4)
	lid.position = Vector3(0, 0.33, 0)
	root.add_child(lid)
	var clasp := _build_cylinder_mesh(0.04, 0.06, 12, accent)
	clasp.position = Vector3(0, 0.28, 0.18)
	root.add_child(clasp)
	var cord := _build_shimenawa(Vector3(0, 0.3, 0.12), 0.12, accent.darkened(0.2))
	root.add_child(cord)
	return root


static func build_driftwood_log(length: float, wood: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "DriftwoodHD"
	var segments := 14
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var prev_ring: Array[Vector3] = []
	for s in segments + 1:
		var t := float(s) / float(segments)
		var x := lerpf(-length * 0.5, length * 0.5, t)
		var wobble_y := sin(t * 8.0) * 0.06 + cos(t * 3.5) * 0.04
		var wobble_z := cos(t * 6.0) * 0.05
		var r := lerpf(0.18, 0.12, t) + sin(t * 12.0) * 0.02
		var ring: Array[Vector3] = []
		for i in 12:
			var ang := float(i) / 12.0 * TAU
			ring.append(Vector3(x, wobble_y + cos(ang) * r, wobble_z + sin(ang) * r))
		if s > 0:
			for i in 12:
				var i2 := (i + 1) % 12
				_add_quad(st, prev_ring[i], prev_ring[i2], ring[i2], ring[i])
		prev_ring = ring
	st.generate_normals()
	var mesh_inst := MeshInstance3D.new()
	mesh_inst.mesh = st.commit()
	_apply_mat(mesh_inst, wood, 0.88)
	root.add_child(mesh_inst)
	return root


static func build_seaweed_cluster(teal: Color) -> Node3D:
	var root := Node3D.new()
	root.name = "SeaweedHD"
	for i in 8:
		var blade := _build_seaweed_blade(teal.darkened(randf_range(0, 0.15)))
		blade.position = Vector3(randf_range(-0.4, 0.4), 0, randf_range(-0.4, 0.4))
		blade.rotation_degrees.y = randf_range(0, 360)
		root.add_child(blade)
	return root


# --- Internal builders ---

static func _build_tapered_pillar(top_r: float, bot_r: float, height: float, sides: int, color: Color) -> MeshInstance3D:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var rings: Array = []
	for ring_i in 2:
		var y := height * float(ring_i)
		var r := bot_r if ring_i == 0 else top_r
		var ring: Array[Vector3] = []
		for i in sides:
			var ang := float(i) / float(sides) * TAU
			ring.append(Vector3(cos(ang) * r, y, sin(ang) * r))
		rings.append(ring)
	for i in sides:
		var i2 := (i + 1) % sides
		_add_quad(st, rings[0][i], rings[0][i2], rings[1][i2], rings[1][i])
	st.generate_normals()
	return _mesh_instance(st.commit(), color, 0.82)


static func _build_curved_beam(length: float, height: float, depth: float, segs: int, color: Color, curve: float) -> MeshInstance3D:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var half := length * 0.5
	for s in segs:
		var t0 := float(s) / float(segs)
		var t1 := float(s + 1) / float(segs)
		var x0 := lerpf(-half, half, t0)
		var x1 := lerpf(-half, half, t1)
		var y0 := sin(t0 * PI) * curve
		var y1 := sin(t1 * PI) * curve
		var hd := depth * 0.5
		var hh := height * 0.5
		var v0 := Vector3(x0, y0 - hh, -hd)
		var v1 := Vector3(x1, y1 - hh, -hd)
		var v2 := Vector3(x1, y1 + hh, -hd)
		var v3 := Vector3(x0, y0 + hh, -hd)
		var v4 := Vector3(x0, y0 - hh, hd)
		var v5 := Vector3(x1, y1 - hh, hd)
		var v6 := Vector3(x1, y1 + hh, hd)
		var v7 := Vector3(x0, y0 + hh, hd)
		_add_quad(st, v0, v1, v2, v3)
		_add_quad(st, v5, v4, v7, v6)
		_add_quad(st, v4, v0, v3, v7)
		_add_quad(st, v1, v5, v6, v2)
	st.generate_normals()
	return _mesh_instance(st.commit(), color, 0.7, 0.05)


static func _build_shimenawa(center: Vector3, radius: float, color: Color) -> Node3D:
	var root := Node3D.new()
	root.position = center
	var torus := _build_torus_mesh(radius, 0.035, 24, 8, color)
	root.add_child(torus)
	for i in 4:
		var paper := _build_box_mesh(Vector3(0.06, 0.14, 0.01), Color.WHITE, 0.0, 0.0)
		var ang := float(i) / 4.0 * TAU
		paper.position = Vector3(cos(ang) * radius, -0.08, sin(ang) * radius)
		paper.rotation_degrees = Vector3(-12, rad_to_deg(ang) + 90, 0)
		root.add_child(paper)
	return root


static func _build_torus_mesh(major_r: float, minor_r: float, major_seg: int, minor_seg: int, color: Color) -> MeshInstance3D:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in major_seg:
		var a0 := float(i) / float(major_seg) * TAU
		var a1 := float(i + 1) / float(major_seg) * TAU
		for j in minor_seg:
			var b0 := float(j) / float(minor_seg) * TAU
			var b1 := float(j + 1) / float(minor_seg) * TAU
			var p00 := _torus_point(a0, b0, major_r, minor_r)
			var p10 := _torus_point(a1, b0, major_r, minor_r)
			var p11 := _torus_point(a1, b1, major_r, minor_r)
			var p01 := _torus_point(a0, b1, major_r, minor_r)
			_add_quad(st, p00, p10, p11, p01)
	st.generate_normals()
	return _mesh_instance(st.commit(), color, 0.75)


static func _torus_point(a: float, b: float, major_r: float, minor_r: float) -> Vector3:
	var cx := cos(a) * major_r
	var cz := sin(a) * major_r
	var nx := cos(a)
	var nz := sin(a)
	var px := cos(b) * nx
	var py := sin(b)
	var pz := cos(b) * nz
	return Vector3(cx + px * minor_r, py * minor_r, cz + pz * minor_r)


static func _build_cylinder_mesh(radius: float, height: float, sides: int, color: Color) -> MeshInstance3D:
	var mesh := CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius
	mesh.height = height
	mesh.radial_segments = sides
	mesh.rings = 4
	return _mesh_instance(mesh, color, 0.85)


static func _build_lantern_chamber(radius: float, height: float, sides: int, stone: Color, glow: Color) -> Node3D:
	var root := Node3D.new()
	var frame := _build_cylinder_mesh(radius, height, sides, stone)
	frame.position.y = height * 0.5
	root.add_child(frame)
	var window := _build_box_mesh(Vector3(radius * 1.6, height * 0.55, 0.04), glow, 0.6, 0.0)
	window.position = Vector3(0, height * 0.5, radius * 0.92)
	root.add_child(window)
	var light := OmniLight3D.new()
	light.light_color = glow
	light.light_energy = 0.35
	light.omni_range = 2.5
	light.position = Vector3(0, height * 0.5, 0)
	root.add_child(light)
	return root


static func _build_lantern_roof(radius: float, height: float, sides: int, color: Color) -> MeshInstance3D:
	var mesh := CylinderMesh.new()
	mesh.top_radius = 0.05
	mesh.bottom_radius = radius
	mesh.height = height
	mesh.radial_segments = sides
	mesh.rings = 3
	return _mesh_instance(mesh, color, 0.78)


static func _build_bamboo_stalk(green: Color, ring: Color) -> Node3D:
	var root := Node3D.new()
	var height := randf_range(2.8, 4.2)
	var segments := 8
	for s in segments:
		var seg_h := height / float(segments)
		var r := lerpf(0.07, 0.05, float(s) / float(segments))
		var cyl := _build_cylinder_mesh(r, seg_h, 14, green.darkened(float(s) * 0.02))
		cyl.position.y = float(s) * seg_h + seg_h * 0.5
		root.add_child(cyl)
		var node_ring := _build_torus_mesh(r * 1.08, 0.012, 14, 6, ring)
		node_ring.position.y = float(s + 1) * seg_h
		root.add_child(node_ring)
	for l in 3:
		var leaf := _build_bamboo_leaf(green.lightened(0.08))
		leaf.position = Vector3(randf_range(-0.15, 0.15), height * randf_range(0.55, 0.9), randf_range(-0.15, 0.15))
		leaf.rotation_degrees = Vector3(randf_range(-25, 25), randf_range(0, 360), randf_range(-15, 15))
		root.add_child(leaf)
	return root


static func _build_bamboo_leaf(color: Color) -> MeshInstance3D:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var len := 0.55
	var w := 0.08
	var pts := [
		Vector3(0, 0, 0),
		Vector3(len * 0.85, 0.02, w),
		Vector3(len, 0, 0),
		Vector3(len * 0.85, 0.02, -w),
	]
	_add_quad(st, pts[0], pts[1], pts[2], pts[3])
	st.generate_normals()
	return _mesh_instance(st.commit(), color, 0.65)


static func _build_pine_needle_layer(radius: float, thickness: float, segments: int, color: Color) -> MeshInstance3D:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var layers := 3
	for layer in layers:
		var r := radius * (1.0 - float(layer) * 0.12)
		var y_off := float(layer) * thickness * 0.25
		for i in segments:
			var a0 := float(i) / float(segments) * TAU
			var a1 := float(i + 1) / float(segments) * TAU
			var tip := Vector3(0, thickness + y_off, 0)
			var p0 := Vector3(cos(a0) * r, y_off, sin(a0) * r)
			var p1 := Vector3(cos(a1) * r, y_off, sin(a1) * r)
			st.set_normal(Vector3.UP)
			st.add_vertex(tip)
			st.add_vertex(p0)
			st.add_vertex(p1)
	st.generate_normals()
	return _mesh_instance(st.commit(), color, 0.72)


static func _build_deformed_rock(radius: float, subdiv: int, color: Color) -> MeshInstance3D:
	var sphere := SphereMesh.new()
	sphere.radius = radius
	sphere.height = radius * 2.0
	sphere.radial_segments = 24
	sphere.rings = 16
	var arrays := sphere.surface_get_arrays(0)
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	for i in verts.size():
		var v := verts[i]
		var n := v.normalized()
		var noise := sin(v.x * 4.1) * cos(v.y * 3.7) * sin(v.z * 5.2) * 0.12
		verts[i] = n * radius * (1.0 + noise)
	arrays[Mesh.ARRAY_VERTEX] = verts
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return _mesh_instance(mesh, color, 0.92)


static func _build_moss_patch(size: float, color: Color) -> MeshInstance3D:
	var mesh := SphereMesh.new()
	mesh.radius = size
	mesh.height = size * 0.35
	mesh.radial_segments = 14
	mesh.rings = 8
	var inst := _mesh_instance(mesh, color, 0.95)
	inst.scale = Vector3(1.2, 0.35, 1.0)
	return inst


static func _build_box_mesh(size: Vector3, color: Color, metallic: float, emission: float) -> MeshInstance3D:
	var box := BoxMesh.new()
	box.size = size
	var inst := _mesh_instance(box, color, 0.75, metallic)
	if emission > 0.0:
		var mat := inst.material_override as StandardMaterial3D
		mat.emission_enabled = true
		mat.emission = color * emission
	return inst


static func _build_seaweed_blade(color: Color) -> MeshInstance3D:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var h := randf_range(0.6, 1.1)
	var w := 0.07
	for seg in 6:
		var t0 := float(seg) / 6.0
		var t1 := float(seg + 1) / 6.0
		var sway0 := sin(t0 * PI) * 0.12
		var sway1 := sin(t1 * PI) * 0.12
		var y0 := t0 * h
		var y1 := t1 * h
		_add_quad(
			st,
			Vector3(sway0, y0, -w),
			Vector3(sway0, y0, w),
			Vector3(sway1, y1, w),
			Vector3(sway1, y1, -w),
		)
	st.generate_normals()
	var inst := _mesh_instance(st.commit(), color, 0.35)
	var mat := inst.material_override as StandardMaterial3D
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_color.a = 0.85
	return inst


static func _add_quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3) -> void:
	var n := (b - a).cross(c - a).normalized()
	st.set_normal(n)
	st.add_vertex(a)
	st.set_normal(n)
	st.add_vertex(b)
	st.set_normal(n)
	st.add_vertex(c)
	st.set_normal(n)
	st.add_vertex(a)
	st.set_normal(n)
	st.add_vertex(c)
	st.set_normal(n)
	st.add_vertex(d)


static func _mesh_instance(mesh: Mesh, color: Color, roughness: float, metallic: float = 0.0) -> MeshInstance3D:
	var inst := MeshInstance3D.new()
	inst.mesh = mesh
	_apply_mat(inst, color, roughness, metallic)
	return inst


static func _apply_mat(inst: MeshInstance3D, color: Color, roughness: float, metallic: float = 0.0) -> void:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = roughness
	mat.metallic = metallic
	inst.material_override = mat
