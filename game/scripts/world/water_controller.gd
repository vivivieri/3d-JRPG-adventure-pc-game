extends Node3D
## Raises/lowers a water plane and optional path barrier for the tidal puzzle.


@export var water_mesh_path: NodePath
@export var barrier_path: NodePath
@export var lowered_y := -1.8
@export var raised_y := 0.4

var _lowered := false


func _ready() -> void:
	_lowered = GameManager.has_flag("water_lowered")
	_apply_level()


func toggle() -> void:
	_lowered = not _lowered
	if _lowered:
		GameManager.set_flag("water_lowered")
	else:
		GameManager.story_flags.erase("water_lowered")
	_apply_level()


func is_lowered() -> bool:
	return _lowered


func _apply_level() -> void:
	var water := get_node_or_null(water_mesh_path) as Node3D
	if water:
		water.position.y = lowered_y if _lowered else raised_y
	var barrier := get_node_or_null(barrier_path) as Node3D
	if barrier:
		barrier.visible = not _lowered
