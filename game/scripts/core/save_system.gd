extends Node
## JSON save/load to user://saves/

const SAVE_PATH := "user://saves/slot1.json"


func _ready() -> void:
	DirAccess.make_dir_recursive_absolute("user://saves")


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


func save_game() -> bool:
	var data := GameManager.get_save_dict()
	data["saved_at"] = Time.get_datetime_string_from_system()
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		return false
	file.store_string(JSON.stringify(data, "\t"))
	EventBus.game_saved.emit()
	return true


func load_game() -> bool:
	if not has_save():
		return false
	var text := FileAccess.get_file_as_string(SAVE_PATH)
	var data = JSON.parse_string(text)
	if data == null:
		return false
	GameManager.load_save_dict(data)
	EventBus.game_loaded.emit()
	GameManager.go_to_zone(GameManager.current_zone)
	return true
