extends Node
## Tracks discovered lore entries and exposes journal data.


var _entries: Array = []
var _by_id: Dictionary = {}


func _ready() -> void:
	_load_entries()


func _load_entries() -> void:
	var data = GameManager.load_json("res://data/lore/lore_entries.json")
	if data == null:
		return
	_entries = data.get("entries", [])
	_by_id.clear()
	for entry in _entries:
		_by_id[entry.get("id", "")] = entry


func get_all_entries() -> Array:
	return _entries


func get_entry(lore_id: String) -> Dictionary:
	return _by_id.get(lore_id, {})


func is_collected(lore_id: String) -> bool:
	return GameManager.has_flag(_flag_for(lore_id))


func collect(lore_id: String) -> bool:
	if lore_id.is_empty() or is_collected(lore_id):
		return false
	if get_entry(lore_id).is_empty():
		return false
	GameManager.set_flag(_flag_for(lore_id))
	EventBus.lore_collected.emit(lore_id)
	return true


func collected_count() -> int:
	var count := 0
	for entry in _entries:
		if is_collected(entry.get("id", "")):
			count += 1
	return count


func total_count() -> int:
	return _entries.size()


func title_for(lore_id: String) -> String:
	var entry: Dictionary = get_entry(lore_id)
	if entry.is_empty():
		return ""
	return LocalizationManager.resolve_text(entry.get("title", {}))


func body_for(lore_id: String) -> String:
	var entry: Dictionary = get_entry(lore_id)
	if entry.is_empty():
		return ""
	return LocalizationManager.resolve_text(entry.get("body", {}))


func locked_label() -> String:
	return LocalizationManager.tr_key("UI_LORE_LOCKED")


func _flag_for(lore_id: String) -> String:
	return "lore_%s" % lore_id
