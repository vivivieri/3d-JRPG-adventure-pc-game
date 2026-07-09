extends Node
## Global game state, data loading, and scene transitions.

enum GameState { EXPLORATION, DIALOGUE, COMBAT, MENU, CUTSCENE }

var state: GameState = GameState.EXPLORATION
var story_flags: Dictionary = {}
var party_ids: Array[String] = ["urashima"]
var party_levels: Dictionary = { "urashima": 1 }
var inventory: Dictionary = {}
var gold: int = 0
var current_area: String = "ruined_village"
var entry_spawn: String = ""

var _data_cache: Dictionary = {}


func _ready() -> void:
	_load_core_data()


func _load_core_data() -> void:
	_data_cache["party"] = load_json("res://data/characters/party.json")
	_data_cache["skills"] = load_json("res://data/skills/skills.json")
	_data_cache["enemies"] = load_json("res://data/enemies/enemies.json")
	_data_cache["items"] = load_json("res://data/items/items.json")
	_data_cache["dialogue"] = load_json("res://data/dialogue/chapter_01.json")
	_data_cache["quests"] = load_json("res://data/quests/main_quests.json")


func load_json(path: String) -> Variant:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Failed to open JSON: %s" % path)
		return null
	var text := file.get_as_text()
	file.close()
	var parsed = JSON.parse_string(text)
	if parsed == null:
		push_error("Failed to parse JSON: %s" % path)
	return parsed


func get_data(category: String) -> Variant:
	return _data_cache.get(category)


func set_flag(flag: String, value: bool = true) -> void:
	story_flags[flag] = value
	EventBus.story_flag_changed.emit(flag, value)


func has_flag(flag: String) -> bool:
	return story_flags.get(flag, false)


func add_party_member(character_id: String) -> void:
	if character_id not in party_ids:
		party_ids.append(character_id)
		party_levels[character_id] = party_levels.get(character_id, 1)
		EventBus.party_changed.emit()


func change_state(new_state: GameState) -> void:
	state = new_state
	EventBus.game_state_changed.emit(new_state)


func start_combat(enemy_ids: Array) -> void:
	change_state(GameState.COMBAT)
	CombatManager.start_battle(enemy_ids)


func get_character_def(character_id: String) -> Dictionary:
	var party_data: Dictionary = _data_cache.get("party", {})
	for c in party_data.get("characters", []):
		if c.get("id") == character_id:
			return c
	return {}


func get_skill_def(skill_id: String) -> Dictionary:
	var skills_data: Dictionary = _data_cache.get("skills", {})
	for s in skills_data.get("skills", []):
		if s.get("id") == skill_id:
			return s
	return {}


func get_enemy_def(enemy_id: String) -> Dictionary:
	var enemy_data: Dictionary = _data_cache.get("enemies", {})
	for e in enemy_data.get("enemies", []):
		if e.get("id") == enemy_id:
			return e
	return {}


func get_item_def(item_id: String) -> Dictionary:
	var item_data: Dictionary = _data_cache.get("items", {})
	for item in item_data.get("items", []):
		if item.get("id") == item_id:
			return item
	return {}


func get_item_count(item_id: String) -> int:
	return inventory.get(item_id, 0)


func add_item(item_id: String, quantity: int = 1) -> void:
	inventory[item_id] = get_item_count(item_id) + quantity


func consume_item(item_id: String, quantity: int = 1) -> bool:
	var current := get_item_count(item_id)
	if current < quantity:
		return false
	var remaining := current - quantity
	if remaining <= 0:
		inventory.erase(item_id)
	else:
		inventory[item_id] = remaining
	return true


func get_battle_item_ids() -> Array[String]:
	var result: Array[String] = []
	for item_id in inventory.keys():
		var def := get_item_def(item_id)
		if def.get("battle_use", false) and get_item_count(item_id) > 0:
			result.append(item_id)
	result.sort()
	return result
