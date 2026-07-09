extends Node3D
## Subsurface face silhouettes that ripple beneath the deep pool.


@export var face_count := 6
@export var pool_size := Vector2(6.5, 4.5)
@export var depth := -0.42
@export var ripple_speed := 0.75

var _faces: Array[MeshInstance3D] = []
var _phase_offsets: Array[float] = []


func _ready() -> void:
	_build_faces()


func _process(delta: float) -> void:
	var t := Time.get_ticks_msec() * 0.001 * ripple_speed
	for i in _faces.size():
		var face := _faces[i]
		var phase := _phase_offsets[i]
		face.position.y = depth + sin(t + phase) * 0.07
		face.position.x += sin(t * 0.35 + phase * 1.7) * delta * 0.04
		var mat := face.material_override as StandardMaterial3D
		if mat:
			var pulse := 0.35 + (sin(t * 1.6 + phase * 2.1) * 0.5 + 0.5) * 0.45
			mat.emission = Color(0.35, 0.82, 0.78) * pulse


func _build_faces() -> void:
	for i in face_count:
		var face := MeshInstance3D.new()
		face.name = "Face_%d" % i
		var plane := PlaneMesh.new()
		plane.size = Vector2(randf_range(0.55, 0.95), randf_range(0.7, 1.1))
		face.mesh = plane
		face.rotation_degrees = Vector3(-88, randf_range(0, 360), randf_range(-12, 12))
		face.position = Vector3(
			randf_range(-pool_size.x * 0.42, pool_size.x * 0.42),
			depth,
			randf_range(-pool_size.y * 0.42, pool_size.y * 0.42),
		)
		var mat := StandardMaterial3D.new()
		mat.albedo_color = Color(0.08, 0.22, 0.28, 0.55)
		mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		mat.cull_mode = BaseMaterial3D.CULL_DISABLED
		mat.emission_enabled = true
		mat.emission = Color(0.35, 0.82, 0.78) * 0.4
		mat.roughness = 0.2
		face.material_override = mat
		add_child(face)
		_faces.append(face)
		_phase_offsets.append(randf() * TAU)
