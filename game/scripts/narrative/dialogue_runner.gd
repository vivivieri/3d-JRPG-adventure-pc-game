extends Node
## Plays dialogue scenes from chapter_01.json and drives field blocking.

signal finished(scene_id: String)

var _active := false
var _scene_id := ""
var _ui: Node = null


func _ready() -> void:
	call_deferred("_ensure_ui")


func _ensure_ui() -> void:
	if _ui:
		return
	var packed := preload("res://scenes/ui/dialogue_box.tscn")
	_ui = packed.instantiate()
	get_tree().root.add_child(_ui)
	_ui.hide()


func is_active() -> bool:
	return _active


func play(scene_id: String) -> void:
	if _active:
		return
	var data: Dictionary = GameManager.dialogue_scenes.get(scene_id, {})
	if data.is_empty():
		push_warning("Missing dialogue scene: %s" % scene_id)
		finished.emit(scene_id)
		return
	_scene_id = scene_id
	_active = true
	EventBus.dialogue_started.emit(scene_id)
	EventBus.scene_blocked_changed.emit(true)
	_ensure_ui()
	_ui.start(data, _on_dialogue_done)


func _on_dialogue_done(choice_data: Dictionary) -> void:
	var scene_data: Dictionary = GameManager.dialogue_scenes.get(_scene_id, {})
	if not choice_data.is_empty():
		GameManager.apply_dialogue_complete(choice_data)
	var on_complete: Dictionary = scene_data.get("on_complete", {})
	if not on_complete.is_empty():
		GameManager.apply_dialogue_complete(on_complete)
	GameManager.mark_scene_done(_scene_id)
	_active = false
	EventBus.scene_blocked_changed.emit(false)
	EventBus.dialogue_finished.emit(_scene_id)
	finished.emit(_scene_id)
	_scene_id = ""
