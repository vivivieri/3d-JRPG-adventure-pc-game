extends Node3D
## Orbit camera rig following the player.

@export var pivot_height: float = 1.4
@export var distance: float = 6.0
@export var min_pitch: float = -35.0
@export var max_pitch: float = 55.0
@export var sensitivity: float = 0.003

var _yaw := 0.0
var _pitch := 15.0
var _target: Node3D = null
var _camera: Camera3D = null


func _ready() -> void:
	_camera = Camera3D.new()
	_camera.name = "Camera3D"
	_camera.current = true
	add_child(_camera)
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func set_target(target: Node3D) -> void:
	_target = target
	if _target and _target.has_method("set_camera"):
		_target.set_camera(_camera)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		_yaw -= event.relative.x * sensitivity
		_pitch = clamp(_pitch - event.relative.y * sensitivity, deg_to_rad(min_pitch), deg_to_rad(max_pitch))
	if event.is_action_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED else Input.MOUSE_MODE_CAPTURED


func _process(_delta: float) -> void:
	if not _target:
		return
	var origin := _target.global_position + Vector3(0, pivot_height, 0)
	var offset := Vector3(
		sin(_yaw) * cos(_pitch),
		sin(_pitch),
		cos(_yaw) * cos(_pitch)
	) * distance
	global_position = origin + offset
	look_at(origin, Vector3.UP)
