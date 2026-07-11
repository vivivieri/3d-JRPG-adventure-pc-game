extends Node
## GUI autopilot: plays each ending cinematic and saves proof frames.

const OUT_DIR := "/workspace/artifacts/videos"
const ENDING_SCENES := {
	"rewind": "SC-17a",
	"anchor": "SC-17b",
	"drift": "SC-17c",
}

var _step := 0
var _endings: Array[String] = ["rewind", "anchor", "drift"]


func start() -> void:
	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	call_deferred("_run_next")


func _run_next() -> void:
	if _step >= _endings.size():
		print("E2E_ENDINGS_DONE count=3 dir=%s" % OUT_DIR)
		get_tree().quit(0)
		return
	var ending := _endings[_step]
	print("E2E_PLAY ending=%s" % ending)
	await _play_ending(ending)
	_step += 1
	call_deferred("_run_next")


func _play_ending(ending: String) -> void:
	GameManager.reset_new_game()
	_setup_act3()
	GameManager.set_flag("ending_chosen", ending)
	var zone := "ending_%s" % ending
	get_tree().change_scene_to_file(GameManager.ZONE_SCENES[zone])
	await _wait(25)
	AudioManager.play_bgm(AudioManager.BGM_FIELD, true)
	var scene_id := str(ENDING_SCENES.get(ending, ""))
	if DialogueRunner.is_active():
		await _skip_dialogue(scene_id)
	elif scene_id != "":
		DialogueRunner.play(scene_id)
		await _skip_dialogue(scene_id)
	await _wait(20)
	await _shot("ending_%s" % ending)


func _skip_dialogue(scene_id: String) -> void:
	for _i in 40:
		if not DialogueRunner.is_active():
			break
		var ev := InputEventKey.new()
		ev.keycode = KEY_SPACE
		ev.pressed = true
		Input.parse_input_event(ev)
		ev.pressed = false
		Input.parse_input_event(ev)
		await _wait(2)
	if DialogueRunner.is_active() and scene_id != "":
		var data: Dictionary = GameManager.dialogue_scenes.get(scene_id, {})
		GameManager.apply_dialogue_complete(data.get("on_complete", {}))
		GameManager.mark_scene_done(scene_id)


func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	await get_tree().process_frame
	var tex := get_viewport().get_texture()
	if tex == null:
		return
	var path := "%s/%s.png" % [OUT_DIR, name]
	var err := tex.get_image().save_png(path)
	if err == OK:
		print("E2E_SAVED %s" % path)


func _setup_act3() -> void:
	for sid in ["SC-00", "SC-01", "SC-02", "SC-03", "SC-04", "SC-05", "SC-06", "SC-07", "SC-08", "SC-09", "SC-10", "SC-11", "SC-12", "SC-13", "SC-14", "SC-15", "SC-16"]:
		GameManager.mark_scene_done(sid)
	GameManager.set_flag("prologue_seen")
	GameManager.set_flag("game_started")
	GameManager.set_flag("met_roku")
	GameManager.set_flag("cave_entrance_unlocked")
	GameManager.set_flag("tutorial_combat_done")
	GameManager.set_flag("water_puzzle_solved")
	GameManager.set_flag("shore_wraith_defeated")
	GameManager.set_flag("yuzu_joined")
	GameManager.set_flag("roku_combat_active")
	GameManager.set_flag("tide_keeper_phase3")
	GameManager.add_item("wraith_pearl", 1)
	GameManager.party_field = ["urashima", "yuzu", "roku"]
	GameManager.party_combat = ["urashima", "yuzu", "roku"]


func _wait(frames: int) -> void:
	for _i in frames:
		await get_tree().process_frame
