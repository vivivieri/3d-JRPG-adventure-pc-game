extends Node
## Headless movement validation — run:
## godot4 --headless --path game res://tests/movement_smoke_test.tscn

const BEACH := preload("res://scenes/world/beach_shore.tscn")


func _ready() -> void:
	GameManager.mark_scene_done("SC-00")
	GameManager.mark_scene_done("SC-01")
	GameManager.pending_dialogue = ""
	var zone := BEACH.instantiate()
	get_tree().root.call_deferred("add_child", zone)
	call_deferred("_run_test")


func _run_test() -> void:
	await get_tree().create_timer(0.5).timeout
	var player: CharacterBody3D = get_tree().get_first_node_in_group("player")
	if player == null:
		push_error("No player found")
		get_tree().quit(1)
		return
	var field = get_tree().get_first_node_in_group("field_controller")
	if field and field.has_method("_set_field_blocked"):
		field._set_field_blocked(false)
	player.set_enabled(true)
	var start := player.global_position
	Input.action_press("move_forward")
	for i in 20:
		await get_tree().physics_frame
	Input.action_release("move_forward")
	var end := player.global_position
	var moved := start.distance_to(end)
	print("MOVEMENT_TEST delta=%.2f start=%s end=%s enabled=%s" % [moved, start, end, player._enabled])
	get_tree().quit(0 if moved > 0.3 else 1)
