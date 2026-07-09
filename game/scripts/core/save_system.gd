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
		"equipped": GameManager.equipped,
		"party_field_stats": GameManager.party_field_stats,
		"quest_tracker": QuestTracker.get_snapshot(),
		"gold": GameManager.gold,
		"current_area": GameManager.current_area,
		"chosen_ending": GameManager.chosen_ending,
		"lore_collected": LoreJournal.collected_count(),
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
	GameManager.equipped = parsed.get("equipped", {})
	GameManager.party_field_stats = parsed.get("party_field_stats", {})
	var tracker: Dictionary = parsed.get("quest_tracker", {})
	QuestTracker.restore(tracker.get("active_quests", []), tracker.get("completed_quests", []))
	GameManager.gold = parsed.get("gold", 0)
	GameManager.current_area = parsed.get("current_area", "ruined_village")
	GameManager.chosen_ending = parsed.get("chosen_ending", "")
	if GameManager.party_field_stats.is_empty():
		GameManager.reset_party_field_stats()
	return true


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)
