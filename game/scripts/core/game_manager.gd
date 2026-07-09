extends Node
## Global game state, data loading, and scene transitions.

enum GameState { EXPLORATION, DIALOGUE, COMBAT, MENU, CUTSCENE }

var state: GameState = GameState.EXPLORATION
var story_flags: Dictionary = {}
var party_ids: Array[String] = ["urashima"]
var party_levels: Dictionary = { "urashima": 1 }
var inventory: Dictionary = {}
var equipped: Dictionary = {}
var party_field_stats: Dictionary = {}
var gold: int = 0
var current_area: String = "ruined_village"
var entry_spawn: String = ""
var chosen_ending: String = ""

const ENDING_SCENES := {
	"rewind": "res://scenes/world/ending_rewind.tscn",
	"anchor": "res://scenes/world/ending_anchor.tscn",
	"drift": "res://scenes/world/ending_drift.tscn",
}

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
		_init_field_stats_for(character_id)
		EventBus.party_changed.emit()


func reset_party_field_stats() -> void:
	party_field_stats.clear()
	equipped.clear()
	for char_id in party_ids:
		_init_field_stats_for(char_id)


func _init_field_stats_for(character_id: String) -> void:
	var stats := get_combat_base_stats(character_id)
	party_field_stats[character_id] = {
		"hp": stats.get("max_hp", 100),
		"mp": stats.get("max_mp", 20),
		"max_hp": stats.get("max_hp", 100),
		"max_mp": stats.get("max_mp", 20),
		"statuses": [],
	}


func get_combat_base_stats(character_id: String) -> Dictionary:
	var def := get_character_def(character_id)
	var stats: Dictionary = def.get("base_stats", {}).duplicate()
	for slot in get_equipment(character_id).values():
		var item_def := get_item_def(slot)
		var bonus: Dictionary = item_def.get("stat_bonus", {})
		for key in bonus.keys():
			stats[key] = stats.get(key, 0) + bonus[key]
	return stats


func get_equipment(character_id: String) -> Dictionary:
	return equipped.get(character_id, {})


func get_field_item_ids() -> Array[String]:
	var result: Array[String] = []
	for item_id in inventory.keys():
		var def := get_item_def(item_id)
		if def.get("field_use", false) and get_item_count(item_id) > 0:
			result.append(item_id)
	result.sort()
	return result


func get_equippable_items(character_id: String) -> Array[String]:
	var result: Array[String] = []
	for item_id in inventory.keys():
		var def := get_item_def(item_id)
		if def.get("type", "") != "equipment":
			continue
		var allowed: Array = def.get("equip_by", [])
		if allowed.size() > 0 and character_id not in allowed:
			continue
		result.append(item_id)
	result.sort()
	return result


func equip_item(character_id: String, item_id: String) -> bool:
	var def := get_item_def(item_id)
	if def.is_empty() or def.get("type", "") != "equipment":
		return false
	if get_item_count(item_id) <= 0:
		return false
	var allowed: Array = def.get("equip_by", [])
	if allowed.size() > 0 and character_id not in allowed:
		return false
	if not equipped.has(character_id):
		equipped[character_id] = {}
	var slot: String = def.get("slot", "")
	var current: Dictionary = equipped[character_id]
	if current.get(slot, "") == item_id:
		return false
	current[slot] = item_id
	equipped[character_id] = current
	_recalc_field_caps(character_id)
	EventBus.equipment_changed.emit(character_id)
	AudioManager.play_sfx("equip")
	return true


func unequip_slot(character_id: String, slot: String) -> bool:
	if not equipped.has(character_id):
		return false
	var current: Dictionary = equipped[character_id]
	if not current.has(slot):
		return false
	current.erase(slot)
	equipped[character_id] = current
	_recalc_field_caps(character_id)
	EventBus.equipment_changed.emit(character_id)
	AudioManager.play_sfx("equip")
	return true


func _recalc_field_caps(character_id: String) -> void:
	if not party_field_stats.has(character_id):
		_init_field_stats_for(character_id)
		return
	var stats := get_combat_base_stats(character_id)
	var field: Dictionary = party_field_stats[character_id]
	field["max_hp"] = stats.get("max_hp", field.get("max_hp", 100))
	field["max_mp"] = stats.get("max_mp", field.get("max_mp", 20))
	field["hp"] = mini(field.get("hp", field.max_hp), field.max_hp)
	field["mp"] = mini(field.get("mp", field.max_mp), field.max_mp)


func use_field_item(item_id: String, character_id: String) -> Dictionary:
	var def := get_item_def(item_id)
	if def.is_empty() or not def.get("field_use", false):
		return { "success": false, "message": "" }
	if get_item_count(item_id) <= 0:
		return { "success": false, "message": "" }
	if not party_field_stats.has(character_id):
		_init_field_stats_for(character_id)
	var field: Dictionary = party_field_stats[character_id]
	var outcome := ItemEffectResolver.apply_to_stats(field, def)
	if not outcome.success and outcome.message_key == "field.item_no_effect":
		return {
			"success": false,
			"message": LocalizationManager.tr_key(outcome.message_key, {
				"target": LocalizationManager.character_name(character_id),
			}),
		}
	if not outcome.success:
		return { "success": false, "message": LocalizationManager.tr_key("field.item_no_effect", {
			"target": LocalizationManager.character_name(character_id),
		}) }
	consume_item(item_id)
	AudioManager.play_sfx("item")
	var item_name := LocalizationManager.item_name(item_id)
	var target_name := LocalizationManager.character_name(character_id)
	var message := LocalizationManager.tr_key(outcome.message_key, {
		"item": item_name,
		"target": target_name,
		"amount": outcome.healed_hp if outcome.healed_hp > 0 else outcome.restored_mp,
		"status": LocalizationManager.tr_key("status.%s" % outcome.cured_status) if outcome.cured_status else "",
	})
	EventBus.field_item_used.emit(character_id, item_id)
	return { "success": true, "message": message }


func build_combat_definition(character_id: String) -> Dictionary:
	var def := get_character_def(character_id).duplicate(true)
	var stats := get_combat_base_stats(character_id)
	if party_field_stats.has(character_id):
		var field: Dictionary = party_field_stats[character_id]
		stats["max_hp"] = field.get("max_hp", stats.get("max_hp", 100))
		stats["max_mp"] = field.get("max_mp", stats.get("max_mp", 20))
		stats["hp"] = field.get("hp", stats.get("max_hp", 100))
		stats["mp"] = field.get("mp", stats.get("max_mp", 20))
	def["stats"] = stats
	return def


func sync_field_stats_from_combat(allies: Array) -> void:
	for ally in allies:
		if not ally is Combatant:
			continue
		if not party_field_stats.has(ally.id):
			_init_field_stats_for(ally.id)
		party_field_stats[ally.id]["hp"] = ally.hp
		party_field_stats[ally.id]["mp"] = ally.mp
		party_field_stats[ally.id]["max_hp"] = ally.max_hp
		party_field_stats[ally.id]["max_mp"] = ally.max_mp


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


func play_ending(ending_id: String) -> void:
	var scene_path: String = ENDING_SCENES.get(ending_id, "")
	if scene_path.is_empty():
		push_error("Unknown ending: %s" % ending_id)
		return
	chosen_ending = ending_id
	set_flag("ending_%s" % ending_id)
	get_tree().change_scene_to_file(scene_path)


func get_battle_item_ids() -> Array[String]:
	var result: Array[String] = []
	for item_id in inventory.keys():
		var def := get_item_def(item_id)
		if def.get("battle_use", false) and get_item_count(item_id) > 0:
			result.append(item_id)
	result.sort()
	return result
