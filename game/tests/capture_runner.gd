extends Node
## Survives scene changes on root; saves viewport PNGs for playthrough proof.

const OUT_DIR := "/workspace/artifacts/screenshots"

var _step := 0
var _steps: Array[Dictionary] = []


func start() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	_build_steps()
	call_deferred("_run_next")


func _build_steps() -> void:
	_steps = [
		{"id": "01_main_menu", "fn": _cap_main_menu},
		{"id": "02_prologue_dialogue", "fn": _cap_prologue},
		{"id": "03_beach_field", "fn": _cap_beach},
		{"id": "04_village_field", "fn": _cap_village},
		{"id": "05_combat_tutorial", "fn": _cap_combat},
		{"id": "06_tidal_caves", "fn": _cap_caves},
		{"id": "07_palace_gate", "fn": _cap_palace},
		{"id": "08_ending_rewind", "fn": _cap_ending},
		{"id": "09_credits", "fn": _cap_credits},
	]


func _run_next() -> void:
	if _step >= _steps.size():
		print("CAPTURE_DONE count=%d dir=%s" % [_steps.size(), OUT_DIR])
		get_tree().quit(0)
		return
	_cleanup_ui()
	var entry: Dictionary = _steps[_step]
	print("CAPTURE_STEP %s" % entry.id)
	await entry.fn.call(entry.id)
	_step += 1
	call_deferred("_run_next")


func _wait(frames: int = 8) -> void:
	for i in frames:
		await get_tree().process_frame


func _cleanup_ui() -> void:
	var dlg: Node = get_tree().root.get_node_or_null("DialogueBox")
	if dlg:
		dlg.hide()
	var hud: Node = get_tree().root.get_node_or_null("FieldHUD")
	if hud:
		hud.hide()
	var combat: Node = get_tree().root.get_node_or_null("CombatScene")
	if combat:
		combat.queue_free()
	await get_tree().process_frame


func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	await get_tree().process_frame
	var tex := get_viewport().get_texture()
	if tex == null:
		push_warning("No viewport texture for %s" % name)
		return
	var img := tex.get_image()
	var path := "%s/%s.png" % [OUT_DIR, name]
	var err := img.save_png(path)
	if err == OK:
		print("CAPTURE_SAVED %s" % path)
	else:
		push_error("Failed to save %s err=%s" % [path, err])


func _cap_main_menu(_id: String) -> void:
	get_tree().change_scene_to_file("res://scenes/ui/main_menu.tscn")
	await _wait(12)
	await _shot(_id)


func _cap_prologue(id: String) -> void:
	GameManager.reset_new_game()
	GameManager.pending_dialogue = "SC-00"
	GameManager.pending_spawn = "WorldSpawn"
	get_tree().change_scene_to_file("res://scenes/world/beach_shore.tscn")
	await _wait(14)
	await _shot(id)


func _cap_beach(id: String) -> void:
	GameManager.reset_new_game()
	for sid in ["SC-00", "SC-01"]:
		GameManager.mark_scene_done(sid)
	GameManager.set_flag("prologue_seen")
	GameManager.set_flag("game_started")
	GameManager.pending_spawn = "WorldSpawn"
	get_tree().change_scene_to_file("res://scenes/world/beach_shore.tscn")
	await _wait(10)
	var field = get_tree().get_first_node_in_group("field_controller")
	if field and field.has_method("_set_field_blocked"):
		field._set_field_blocked(false)
	var player = get_tree().get_first_node_in_group("player")
	if player and player.has_method("set_enabled"):
		player.set_enabled(true)
	await _wait(8)
	await _shot(id)


func _cap_village(id: String) -> void:
	_setup_act1_progress()
	GameManager.pending_spawn = "WorldSpawn"
	get_tree().change_scene_to_file("res://scenes/world/ruined_village.tscn")
	await _wait(10)
	await _shot(id)


func _cap_combat(id: String) -> void:
	_setup_act1_progress()
	GameManager.pending_spawn = "TutorialEncounter"
	get_tree().change_scene_to_file("res://scenes/world/ruined_village.tscn")
	await _wait(12)
	GameManager.set_flag("tutorial_combat_done", false)
	CombatManager.start_encounter("enc_sc05_tutorial_crab")
	await _wait(18)
	await _shot(id)


func _cap_caves(id: String) -> void:
	_setup_act2_progress()
	GameManager.pending_spawn = "WorldSpawn"
	get_tree().change_scene_to_file("res://scenes/world/tidal_caves.tscn")
	await _wait(10)
	await _shot(id)


func _cap_palace(id: String) -> void:
	_setup_act3_progress()
	GameManager.add_item("wraith_pearl", 1)
	GameManager.set_flag("roku_combat_active")
	GameManager.set_flag("yuzu_joined")
	GameManager.set_flag("shore_wraith_defeated")
	for sid in ["SC-10", "SC-11"]:
		GameManager.mark_scene_done(sid)
	GameManager.pending_spawn = "WorldSpawn"
	get_tree().change_scene_to_file("res://scenes/world/dragon_palace_gate.tscn")
	await _wait(10)
	await _shot(id)


func _cap_ending(id: String) -> void:
	_setup_act3_progress()
	GameManager.set_flag("ending_choice", "rewind")
	get_tree().change_scene_to_file("res://scenes/world/ending_rewind.tscn")
	await _wait(10)
	await _shot(id)


func _cap_credits(id: String) -> void:
	GameManager.set_flag("game_completed")
	get_tree().change_scene_to_file("res://scenes/ui/credits.tscn")
	await _wait(12)
	await _shot(id)


func _setup_act1_progress() -> void:
	GameManager.reset_new_game()
	for sid in ["SC-00", "SC-01", "SC-02", "SC-03", "SC-04"]:
		GameManager.mark_scene_done(sid)
	GameManager.set_flag("prologue_seen")
	GameManager.set_flag("game_started")
	GameManager.set_flag("met_yuzu_spirit")
	GameManager.set_flag("cave_entrance_unlocked")
	GameManager.add_item("cave_map", 1)
	GameManager.gold = 120


func _setup_act2_progress() -> void:
	_setup_act1_progress()
	for sid in ["SC-05", "SC-06", "SC-07", "SC-08", "SC-09"]:
		GameManager.mark_scene_done(sid)
	GameManager.set_flag("tutorial_combat_done")
	GameManager.set_flag("water_puzzle_solved")
	GameManager.set_flag("shore_wraith_defeated")
	GameManager.add_item("wraith_pearl", 1)
	GameManager.add_item("tide_cut_saber", 1)
	GameManager.party_combat = ["urashima", "yuzu"]
	GameManager.party_field = ["urashima", "yuzu"]
	GameManager.set_flag("yuzu_joined")


func _setup_act3_progress() -> void:
	_setup_act2_progress()
	for sid in ["SC-10", "SC-11", "SC-12", "SC-13", "SC-14", "SC-15", "SC-16"]:
		GameManager.mark_scene_done(sid)
	GameManager.set_flag("roku_combat_active")
	GameManager.party_combat = ["urashima", "yuzu", "roku"]
	GameManager.party_field = ["urashima", "yuzu", "roku"]
