extends Node3D
## Raises/lowers a water plane and optional path barrier for the tidal puzzle.


@export var water_mesh_path: NodePath
@export var barrier_path: NodePath
@export var lowered_y := -1.8
@export var raised_y := 0.4
@export var anim_duration := 1.35

var _lowered := false
var _tween: Tween
var _bob_time := 0.0


func _ready() -> void:
	_lowered = GameManager.has_flag("water_lowered")
	_apply_level(true)
	set_process(true)


func _process(delta: float) -> void:
	var water := get_node_or_null(water_mesh_path) as Node3D
	if water == null or (_tween and _tween.is_running()):
		return
	_bob_time += delta
	var base_y := lowered_y if _lowered else raised_y
	water.position.y = base_y + sin(_bob_time * 1.4) * 0.035


func toggle() -> void:
	_lowered = not _lowered
	if _lowered:
		GameManager.set_flag("water_lowered")
	else:
		GameManager.story_flags.erase("water_lowered")
	_animate_level()


func is_lowered() -> bool:
	return _lowered


func _apply_level(instant: bool = false) -> void:
	var water := get_node_or_null(water_mesh_path) as Node3D
	var target_y := lowered_y if _lowered else raised_y
	if water:
		if instant:
			water.position.y = target_y
		else:
			water.position.y = target_y
	var barrier := get_node_or_null(barrier_path) as Node3D
	if barrier:
		barrier.visible = not _lowered


func _animate_level() -> void:
	if _tween and _tween.is_running():
		_tween.kill()
	var water := get_node_or_null(water_mesh_path) as Node3D
	var barrier := get_node_or_null(barrier_path) as Node3D
	var target_y := lowered_y if _lowered else raised_y
	_tween = create_tween().set_parallel(true).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	if water:
		_tween.tween_property(water, "position:y", target_y, anim_duration)
	if barrier:
		if _lowered:
			_tween.tween_property(barrier, "position:y", barrier.position.y - 2.5, anim_duration * 0.85)
			_tween.tween_callback(func(): barrier.visible = false).set_delay(anim_duration * 0.7)
		else:
			barrier.visible = true
			var raised_barrier_y := 1.25
			barrier.position.y = raised_barrier_y - 2.5
			_tween.tween_property(barrier, "position:y", raised_barrier_y, anim_duration)
