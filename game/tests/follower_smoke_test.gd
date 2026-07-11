extends Node
## Validates party follower spawn when members join.
## godot4 --headless --path game res://tests/follower_smoke_test.tscn

const VILLAGE := preload("res://scenes/world/ruined_village.tscn")


func _ready() -> void:
	GameManager.reset_new_game()
	for sid in ["SC-00", "SC-01", "SC-02", "SC-03", "SC-04", "SC-05", "SC-06", "SC-07", "SC-08", "SC-09", "SC-10"]:
		GameManager.mark_scene_done(sid)
	GameManager.set_flag("yuzu_joined")
	GameManager.add_party_member("yuzu")
	var zone := VILLAGE.instantiate()
	get_tree().root.call_deferred("add_child", zone)
	call_deferred("_run")


func _run() -> void:
	await get_tree().create_timer(0.6).timeout
	var followers := get_tree().get_nodes_in_group("party_follower")
	# Followers may not be in group - check by name
	var field = get_tree().get_first_node_in_group("field_controller")
	var count := 0
	if field:
		for child in field.get_children():
			if str(child.name).begins_with("Follower_"):
				count += 1
	print("FOLLOWER_TEST count=%d party=%s" % [count, str(GameManager.party_field)])
	get_tree().quit(0 if count >= 1 else 1)
