extends Node3D
## Soft spirit silhouettes beneath the deep pool — billboards, not flat boxes.


const FACE_TEX := "res://assets/textures/vfx/face_glow.png"

@export var face_count := 7
@export var pool_size := Vector2(6.5, 4.5)
@export var depth := -0.42
@export var ripple_speed := 0.75

var _faces: Array[Sprite3D] = []
var _phase_offsets: Array[float] = []


func _ready() -> void:
	_build_faces()


func _process(delta: float) -> void:
	var t := Time.get_ticks_msec() * 0.001 * ripple_speed
	for i in _faces.size():
		var face := _faces[i]
		var phase := _phase_offsets[i]
		face.position.y = depth + sin(t + phase) * 0.07
		face.position.x += sin(t * 0.35 + phase * 1.7) * delta * 0.03
		var pulse := 0.45 + (sin(t * 1.6 + phase * 2.1) * 0.5 + 0.5) * 0.4
		face.modulate = Color(0.45, 0.92, 0.86, 0.42 * pulse)


func _build_faces() -> void:
	var tex: Texture2D = load(FACE_TEX) if ResourceLoader.exists(FACE_TEX) else null
	for i in face_count:
		var face := Sprite3D.new()
		face.name = "Face_%d" % i
		if tex:
			face.texture = tex
		face.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		face.pixel_size = randf_range(0.007, 0.011)
		face.axis = Vector3.AXIS_Y
		face.rotation_degrees.x = -12.0
		face.position = Vector3(
			randf_range(-pool_size.x * 0.4, pool_size.x * 0.4),
			depth,
			randf_range(-pool_size.y * 0.4, pool_size.y * 0.4),
		)
		face.modulate = Color(0.45, 0.92, 0.86, 0.38)
		add_child(face)
		_faces.append(face)
		_phase_offsets.append(randf() * TAU)
