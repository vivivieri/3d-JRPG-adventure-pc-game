extends Node
## Headless validation: all three ending zones complete with game_completed flag.

const ENDING_SCENES := {
	"rewind": "SC-17a",
	"anchor": "SC-17b",
	"drift": "SC-17c",
}

var _step := 0
var _endings: Array[String] = ["rewind", "anchor", "drift"]
var _results: Dictionary = {}


func start() -> void:
	call_deferred("_run_next")


func _run_next() -> void:
	if _step >= _endings.size():
		var all_ok := true
		for ending in _endings:
			if not bool(_results.get(ending, false)):
				all_ok = false
		print("E2E_ENDINGS_TEST ok=%s results=%s" % [all_ok, _results])
		get_tree().quit(0 if all_ok else 1)
		return
	var ending := _endings[_step]
	var ok := await _test_ending(ending)
	_results[ending] = ok
	_step += 1
	call_deferred("_run_next")


func _test_ending(ending: String) -> bool:
	GameManager.reset_new_game()
	_setup_act3()
	GameManager.set_flag("ending_chosen", ending)
	var zone := "ending_%s" % ending
	if not GameManager.ZONE_SCENES.has(zone):
		print("ENDING_TEST %s missing_zone" % ending)
		return false
	get_tree().change_scene_to_file(GameManager.ZONE_SCENES[zone])
	await _wait(8)
	var zone_ok := GameManager.current_zone == zone
	var scene_id := str(ENDING_SCENES.get(ending, ""))
	var data: Dictionary = GameManager.dialogue_scenes.get(scene_id, {})
	GameManager.apply_dialogue_complete(data.get("on_complete", {}))
	GameManager.mark_scene_done(scene_id)
	var completed := GameManager.has_flag("game_completed")
	print("ENDING_TEST %s zone_ok=%s completed=%s" % [ending, zone_ok, completed])
	return zone_ok and completed


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
