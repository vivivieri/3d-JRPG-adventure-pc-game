extends CharacterBody3D
## Party follower using stylized primitive character visual.

var character_id: String = ""
var _target: Node3D = null
var _slot := 0
var _follow_speed := 8.0


func setup(char_id: String, target: Node3D, slot: int) -> void:
	character_id = char_id
	_target = target
	_slot = slot
	_build_visual()
	add_to_group("party_follower")


func _build_visual() -> void:
	for child in get_children():
		child.queue_free()
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.32
	shape.height = 1.5
	col.shape = shape
	col.position = Vector3(0, 0.75, 0)
	add_child(col)
	var visual_script = load("res://scripts/visuals/character_visual.gd")
	visual_script.build_character(self, character_id)
	collision_layer = 0
	collision_mask = 1


func _physics_process(delta: float) -> void:
	if not _target:
		return
	if not is_on_floor():
		velocity.y -= 20.0 * delta
	else:
		velocity.y = 0.0
	var back := -_target.global_transform.basis.z
	back.y = 0
	if back.length_squared() < 0.01:
		back = Vector3(0, 0, 1)
	back = back.normalized()
	var side := back.cross(Vector3.UP).normalized()
	var offset := back * (1.4 + _slot * 0.6) + side * (0.7 if _slot % 2 == 0 else -0.7)
	var desired := _target.global_position + offset
	desired.y = _target.global_position.y
	var to := desired - global_position
	to.y = 0
	if to.length() > 0.05:
		velocity.x = to.normalized().x * _follow_speed
		velocity.z = to.normalized().z * _follow_speed
	else:
		velocity.x = 0
		velocity.z = 0
	move_and_slide()
