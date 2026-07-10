extends CharacterBody3D
## Third-person exploration controller (greybox).


@export var move_speed := 5.0
@export var interact_range := 3.0

var _can_move := true


func _ready() -> void:
	add_to_group("player")


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


func get_focused_interactable() -> Node:
	var camera := get_node_or_null("Camera3D") as Camera3D
	var origin := global_position + Vector3.UP
	var direction := -global_transform.basis.z
	if camera:
		origin = camera.global_position
		direction = -camera.global_transform.basis.z
	return _raycast_interactable(origin, direction)


func _try_interact() -> void:
	var target := get_focused_interactable()
	if target:
		target.interact()


func _raycast_interactable(origin: Vector3, direction: Vector3) -> Node:
	var space := get_world_3d().direct_space_state
	if space == null:
		return null
	var query := PhysicsRayQueryParameters3D.create(
		origin,
		origin + direction.normalized() * interact_range
	)
	query.collide_with_areas = true
	query.collide_with_bodies = true
	var result := space.intersect_ray(query)
	if result.is_empty():
		return null
	var collider: Object = result.get("collider")
	if collider is Node and collider.has_method("interact") and collider.has_method("get_prompt"):
		return collider as Node
	return null


func set_movement_enabled(enabled: bool) -> void:
	_can_move = enabled
