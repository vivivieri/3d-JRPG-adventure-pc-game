extends Node
## Shows level-up popups after combat; autoload singleton.

const POPUP_SCENE = preload("res://scenes/ui/level_up_popup.tscn")

var _popup: CanvasLayer = null


func _ready() -> void:
	_ensure_popup()


func _ensure_popup() -> void:
	if _popup:
		return
	_popup = POPUP_SCENE.instantiate()
	get_tree().root.call_deferred("add_child", _popup)
	_popup.hide()


func show_level_ups(level_ups: Array) -> void:
	if level_ups.is_empty():
		return
	_ensure_popup()
	_popup.show_level_ups(level_ups)
	while _popup.visible:
		await get_tree().process_frame
