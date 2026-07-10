extends Camera3D
## Right-mouse orbit camera for exploration.


@export var orbit_enabled := true
@export var mouse_sensitivity := 0.004
@export var min_pitch := -0.15
@export var max_pitch := 0.75
@export var default_distance := 7.0
@export var min_distance := 4.0
@export var max_distance := 12.0

var _yaw := 0.0
var _pitch := 0.38
var _distance := 7.0


func _ready() -> void:
	_distance = default_distance
	_apply_transform()


func _unhandled_input(event: InputEvent) -> void:
	if not orbit_enabled or GameManager.state != GameManager.GameState.EXPLORATION:
		return
	if event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
		var motion := event as InputEventMouseMotion
		_yaw -= motion.relative.x * mouse_sensitivity
		_pitch = clampf(_pitch - motion.relative.y * mouse_sensitivity, min_pitch, max_pitch)
		_apply_transform()
	elif event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_distance = clampf(_distance - 0.8, min_distance, max_distance)
			_apply_transform()
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_distance = clampf(_distance + 0.8, min_distance, max_distance)
			_apply_transform()


func _apply_transform() -> void:
	var horiz := Vector2(sin(_yaw), cos(_yaw)) * cos(_pitch) * _distance
	position = Vector3(horiz.x, sin(_pitch) * _distance + 1.6, horiz.y)
	look_at(Vector3(0, 1.4, 0), Vector3.UP)
