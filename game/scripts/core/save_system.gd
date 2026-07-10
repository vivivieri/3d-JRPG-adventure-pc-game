extends Node
## JSON-based save/load for exploration state.

const SAVE_PATH := "user://save_slot_0.json"


func save_game() -> bool:
	var data := {
		"version": 1,
		"story_flags": GameManager.story_flags,
		"party_ids": GameManager.party_ids,
		"party_levels": GameManager.party_levels,
		"inventory": GameManager.inventory,
		"gold": GameManager.gold,
		"current_area": GameManager.current_area,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("Save failed: cannot open %s" % SAVE_PATH)
		return false
	file.store_string(JSON.stringify(data, "\t"))
	file.close()
	return true


func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return false
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	if parsed == null or typeof(parsed) != TYPE_DICTIONARY:
		return false
	GameManager.story_flags = parsed.get("story_flags", {})
	GameManager.party_ids.assign(parsed.get("party_ids", ["urashima"]))
	GameManager.party_levels = parsed.get("party_levels", { "urashima": 1 })
	GameManager.inventory = parsed.get("inventory", {})
	GameManager.gold = parsed.get("gold", 0)
	GameManager.current_area = parsed.get("current_area", "ruined_village")
	return true


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)
