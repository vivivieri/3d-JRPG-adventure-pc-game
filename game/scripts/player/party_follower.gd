extends CharacterBody3D
## Simple party follower capsule that trails the lead player.

const COLORS := {
	"yuzu": Color(0.85, 0.5, 0.65),
	"roku": Color(0.45, 0.62, 0.48),
	"urashima": Color(0.55, 0.78, 0.95),
}

var character_id: String = ""
var _target: Node3D = null
var _slot := 0
var _follow_speed := 8.0


func setup(char_id: String, target: Node3D, slot: int) -> void:
	character_id = char_id
	_target = target
	_slot = slot
	_build_mesh()


func _build_mesh() -> void:
	for child in get_children():
		child.queue_free()
	var col := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.32
	shape.height = 1.5
	col.shape = shape
	col.position = Vector3(0, 0.75, 0)
	add_child(col)
	var mesh_node := MeshInstance3D.new()
	var mesh := CapsuleMesh.new()
	mesh.radius = 0.32
	mesh.height = 1.5
	mesh_node.mesh = mesh
	mesh_node.position = Vector3(0, 0.75, 0)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = COLORS.get(character_id, Color(0.7, 0.7, 0.75))
	mesh_node.material_override = mat
	add_child(mesh_node)
	collision_layer = 0
	collision_mask = 1
	add_to_group("party_follower")


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
