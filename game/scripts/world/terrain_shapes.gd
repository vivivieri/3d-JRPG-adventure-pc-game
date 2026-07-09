class_name TerrainShapes
extends RefCounted
## Procedural ground meshes with irregular, natural edges.


static func beach_sand_mesh(half_width: float, z_inland: float, z_sea: float) -> ArrayMesh:
	var nx := 16
	var nz := 14
	var verts: PackedVector3Array = []
	verts.resize((nx + 1) * (nz + 1))
	for iz in nz + 1:
		for ix in nx + 1:
			var tx := float(ix) / float(nx)
			var tz := float(iz) / float(nz)
			var x := lerpf(-half_width, half_width, tx)
			var z := lerpf(z_inland, z_sea, tz)
			# Cove taper — beach pinches toward the tree line like a real inlet.
			var cove: float = 1.0 - pow(abs(x) / half_width, 2.2) * 0.28 * tz
			x *= cove
			# Wavy shoreline where sand meets surf.
			if tz > 0.58:
				var shore_t: float = (tz - 0.58) / 0.42
				z += (sin(x * 0.55 + 0.4) * 1.5 + cos(x * 0.21) * 0.9) * shore_t
				x += sin(z * 0.8) * 0.35 * shore_t
			# Gentle dunes inland.
			if tz < 0.35:
				var dune_t: float = 1.0 - tz / 0.35
				z += sin(x * 0.3) * 0.25 * dune_t
			verts[iz * (nx + 1) + ix] = Vector3(x, 0.0, z)
	return _grid_to_mesh(verts, nx, nz, 0.22)


static func beach_shore_pos(x: float) -> Vector2:
	## Returns (x, z) on the sand–surf boundary — same curve as beach_sand_mesh sea edge.
	var half_width := 11.0
	var z_sea := -4.5
	var cove: float = 1.0 - pow(abs(x) / half_width, 2.2) * 0.28
	var cx := x * cove
	var shore_wave := sin(cx * 0.55 + 0.4) * 1.5 + cos(cx * 0.21) * 0.9
	var z := z_sea + shore_wave
	cx += sin(z * 0.8) * 0.35
	return Vector2(cx, z)


static func beach_shoreline_z(x: float) -> float:
	return beach_shore_pos(x).y


static func beach_surf_water_mesh(half_width: float, sea_reach: float, x_segments: int) -> ArrayMesh:
	## Curved surf band that hugs the sand shoreline instead of a flat rectangle.
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in x_segments:
		var t0 := float(i) / float(x_segments)
		var t1 := float(i + 1) / float(x_segments)
		var x0 := lerpf(-half_width, half_width, t0)
		var x1 := lerpf(-half_width, half_width, t1)
		var p0 := beach_shore_pos(x0)
		var p1 := beach_shore_pos(x1)
		var near0 := Vector3(p0.x, -0.3, p0.y - 0.12)
		var near1 := Vector3(p1.x, -0.3, p1.y - 0.12)
		var far0 := Vector3(p0.x, -0.34, p0.y - sea_reach)
		var far1 := Vector3(p1.x, -0.34, p1.y - sea_reach)
		var n := Vector3.UP
		st.set_normal(n)
		st.add_vertex(near0)
		st.set_normal(n)
		st.add_vertex(near1)
		st.set_normal(n)
		st.add_vertex(far1)
		st.set_normal(n)
		st.add_vertex(near0)
		st.set_normal(n)
		st.add_vertex(far1)
		st.set_normal(n)
		st.add_vertex(far0)
	st.generate_normals()
	return st.commit()


static func cave_path_mesh(z_min: float, z_max: float) -> ArrayMesh:
	var nx := 12
	var nz := 28
	var verts: PackedVector3Array = []
	verts.resize((nx + 1) * (nz + 1))
	for iz in nz + 1:
		var tz := float(iz) / float(nz)
		var z := lerpf(z_min, z_max, tz)
		var half_w: float = _cave_half_width(z)
		for ix in nx + 1:
			var tx := float(ix) / float(nx)
			var x := lerpf(-half_w, half_w, tx)
			var edge_dist: float = minf(tx, 1.0 - tx)
			if edge_dist < 0.14:
				var edge_t: float = 1.0 - edge_dist / 0.14
				x += sin(z * 0.55 + ix * 1.7) * 0.42 * edge_t
				x += cos(z * 0.23 + ix * 0.6) * 0.22 * edge_t
			# Slight floor undulation.
			var y := sin(x * 0.7 + z * 0.18) * 0.04
			verts[iz * (nx + 1) + ix] = Vector3(x, y, z)
	return _grid_to_mesh(verts, nx, nz, 0.3)


static func _cave_half_width(z: float) -> float:
	if z < -24.0:
		return 4.2
	if z < -12.0:
		return 3.4 + sin(z * 0.12) * 0.35
	if z < 4.0:
		return 3.8 + cos(z * 0.08) * 0.25
	return 4.0


static func hub_ground_mesh(half_width: float, half_depth: float) -> ArrayMesh:
	var nx := 18
	var nz := 18
	var verts: PackedVector3Array = []
	verts.resize((nx + 1) * (nz + 1))
	for iz in nz + 1:
		for ix in nx + 1:
			var tx := float(ix) / float(nx)
			var tz := float(iz) / float(nz)
			var x := lerpf(-half_width, half_width, tx)
			var z := lerpf(-half_depth, half_depth, tz)
			var nxn := x / half_width
			var nzn := z / half_depth
			var radial: float = sqrt(nxn * nxn + nzn * nzn)
			if radial > 0.78:
				var edge_t: float = clampf((radial - 0.78) / 0.22, 0.0, 1.0)
				x -= sign(x) * edge_t * 1.6
				z -= sign(z) * edge_t * 1.4
				x += sin(z * 0.35 + ix) * 0.45 * edge_t
				z += cos(x * 0.28 + iz) * 0.4 * edge_t
			verts[iz * (nx + 1) + ix] = Vector3(x, sin(x * 0.2 + z * 0.15) * 0.05, z)
	return _grid_to_mesh(verts, nx, nz, 0.25)


static func palace_court_mesh(half_width: float, half_depth: float) -> ArrayMesh:
	var nx := 16
	var nz := 26
	var verts: PackedVector3Array = []
	verts.resize((nx + 1) * (nz + 1))
	for iz in nz + 1:
		for ix in nx + 1:
			var tx := float(ix) / float(nx)
			var tz := float(iz) / float(nz)
			var x := lerpf(-half_width, half_width, tx)
			var z := lerpf(-half_depth, half_depth, tz)
			var taper: float = 1.0 - pow(abs(z) / half_depth, 3.0) * 0.12
			x *= taper
			if abs(x) > half_width * 0.82:
				var edge_t: float = (abs(x) - half_width * 0.82) / (half_width * 0.18)
				x = sign(x) * (half_width * 0.82 + sin(z * 0.22 + ix) * 0.5 * edge_t)
			verts[iz * (nx + 1) + ix] = Vector3(x, 0.0, z)
	return _grid_to_mesh(verts, nx, nz, 0.28)


static func flood_pool_mesh(half_width: float, half_depth: float, segments: int = 14) -> ArrayMesh:
	## Rounded flood-pool basin — not a sharp rectangle on the cave path.
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var center := Vector3.ZERO
	for i in segments:
		var t0 := float(i) / float(segments) * TAU
		var t1 := float(i + 1) / float(segments) * TAU
		var p0 := Vector3(cos(t0) * half_width, 0.0, sin(t0) * half_depth)
		var p1 := Vector3(cos(t1) * half_width, 0.0, sin(t1) * half_depth)
		st.set_normal(Vector3.UP)
		st.set_uv(Vector2(p0.x, p0.z) * 0.22 + Vector2(0.5, 0.5))
		st.add_vertex(center)
		st.set_normal(Vector3.UP)
		st.set_uv(Vector2(p0.x, p0.z) * 0.22 + Vector2(0.5, 0.5))
		st.add_vertex(p0)
		st.set_normal(Vector3.UP)
		st.set_uv(Vector2(p1.x, p1.z) * 0.22 + Vector2(0.5, 0.5))
		st.add_vertex(p1)
	st.generate_normals()
	return st.commit()


static func _grid_to_mesh(verts: PackedVector3Array, nx: int, nz: int, uv_scale: float = 0.35) -> ArrayMesh:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for iz in nz:
		for ix in nx:
			var i00 := iz * (nx + 1) + ix
			var i10 := i00 + 1
			var i01 := i00 + (nx + 1)
			var i11 := i01 + 1
			var v00 := verts[i00]
			var v10 := verts[i10]
			var v01 := verts[i01]
			var v11 := verts[i11]
			var tri := [
				[v00, v10, v11],
				[v00, v11, v01],
			]
			for face in tri:
				var n := (face[1] - face[0]).cross(face[2] - face[0]).normalized()
				for v in face:
					st.set_normal(n)
					st.set_uv(Vector2(v.x, v.z) * uv_scale)
					st.add_vertex(v)
	st.generate_normals()
	return st.commit()
