extends CharacterBody3D
## Third-person exploration controller (greybox).

@export var move_speed := 5.0
@export var interact_range := 2.5

var _can_move := true


func _physics_process(delta: float) -> void:
	if not _can_move or GameManager.state != GameManager.GameState.EXPLORATION:
		velocity = Vector3.ZERO
		move_and_slide()
		return
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	if direction:
		velocity.x = direction.x * move_speed
		velocity.z = direction.z * move_speed
	else:
		velocity.x = move_toward(velocity.x, 0, move_speed)
		velocity.z = move_toward(velocity.z, 0, move_speed)
	move_and_slide()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("interact"):
		_try_interact()


func _try_interact() -> void:
	var space := get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(
		global_position + Vector3.UP,
		global_position + Vector3.UP + -global_transform.basis.z * interact_range
	)
	var result := space.intersect_ray(query)
	if result.is_empty():
		return
	var collider: Object = result.get("collider")
	if collider and collider.has_method("interact"):
		collider.interact()


func set_movement_enabled(enabled: bool) -> void:
	_can_move = enabled
