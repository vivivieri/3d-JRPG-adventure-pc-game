extends Node
## Scrolls water texture UVs for a parent MeshInstance3D.


@export var scroll_speed := Vector2(0.035, 0.022)

var _mat: StandardMaterial3D


func _ready() -> void:
	var mesh := get_parent() as MeshInstance3D
	if mesh == null:
		return
	var base_mat := mesh.material_override as StandardMaterial3D
	if base_mat == null:
		return
	_mat = base_mat.duplicate() as StandardMaterial3D
	mesh.material_override = _mat


func _process(delta: float) -> void:
	if _mat:
		_mat.uv1_offset += Vector3(scroll_speed.x, scroll_speed.y, 0.0) * delta
