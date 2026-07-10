extends CharacterBody3D
## Third-person field movement with simple capsule proxy (greybox phase).

@export var move_speed: float = 6.0
@export var sprint_speed: float = 9.0

var _camera: Camera3D = null
var _enabled := true


func _ready() -> void:
	add_to_group("player")


func set_camera(cam: Camera3D) -> void:
	_camera = cam


func set_enabled(on: bool) -> void:
	_enabled = on
	velocity = Vector3.ZERO


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= 20.0 * delta
	else:
		velocity.y = 0.0
	if not _enabled:
		velocity = Vector3.ZERO
		move_and_slide()
		return
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	if input_dir.length_squared() < 0.01:
		input_dir = Vector2(
			float(Input.is_key_pressed(KEY_D)) - float(Input.is_key_pressed(KEY_A)),
			float(Input.is_key_pressed(KEY_S)) - float(Input.is_key_pressed(KEY_W))
		)
	var speed := sprint_speed if Input.is_action_pressed("sprint") else move_speed
	var direction := Vector3.ZERO
	if _camera:
		var basis := _camera.global_transform.basis
		var forward := -basis.z
		forward.y = 0
		forward = forward.normalized()
		var right := basis.x
		right.y = 0
		right = right.normalized()
		direction = (forward * -input_dir.y + right * input_dir.x).normalized()
	elif input_dir.length_squared() > 0:
		direction = Vector3(input_dir.x, 0, input_dir.y).normalized()
	velocity.x = direction.x * speed
	velocity.z = direction.z * speed
	if direction.length_squared() > 0.01:
		look_at(global_position + direction, Vector3.UP)
	move_and_slide()
