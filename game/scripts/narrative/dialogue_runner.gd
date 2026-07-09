extends Node
## Plays dialogue scenes from JSON data.

var _active := false
var _current_scene: Dictionary = {}
var _line_index := 0


func play_scene(scene_id: String) -> void:
	var dialogue_data: Dictionary = GameManager.get_data("dialogue")
	if dialogue_data == null:
		push_error("Dialogue data not loaded")
		return
	for scene in dialogue_data.get("scenes", []):
		if scene.get("scene_id") == scene_id:
			_start_scene(scene)
			return
	push_error("Dialogue scene not found: %s" % scene_id)


func _start_scene(scene: Dictionary) -> void:
	_active = true
	_current_scene = scene
	_line_index = 0
	GameManager.change_state(GameManager.GameState.DIALOGUE)
	EventBus.dialogue_started.emit(scene.get("scene_id", ""))
	_emit_current_line()


func _emit_current_line() -> void:
	var lines: Array = _current_scene.get("lines", [])
	if _line_index >= lines.size():
		_finish_scene()
		return
	var line: Dictionary = lines[_line_index]
	EventBus.dialogue_line.emit(line)
	_line_index += 1


func advance() -> void:
	if not _active:
		return
	_emit_current_line()


func skip_to_end() -> void:
	if not _active:
		return
	_finish_scene()


func _finish_scene() -> void:
	var scene_id: String = _current_scene.get("scene_id", "")
	var on_complete: Dictionary = _current_scene.get("on_complete", {})
	for flag in on_complete.get("set_flags", []):
		GameManager.set_flag(flag)
	var quest_val = on_complete.get("start_quest", [])
	if quest_val is String and not quest_val.is_empty():
		EventBus.quest_updated.emit(quest_val)
	elif quest_val is Array:
		for quest_id in quest_val:
			EventBus.quest_updated.emit(quest_id)
	for item_entry in on_complete.get("give_items", []):
		var item_id: String = item_entry.get("item_id", "")
		var qty: int = item_entry.get("quantity", 1)
		GameManager.inventory[item_id] = GameManager.inventory.get(item_id, 0) + qty
	_active = false
	_current_scene = {}
	_line_index = 0
	GameManager.change_state(GameManager.GameState.EXPLORATION)
	EventBus.dialogue_finished.emit(scene_id)
