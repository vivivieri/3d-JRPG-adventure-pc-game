extends Node
## Central game state, data loading, flags, party, inventory, quests.

const ZONE_SCENES := {
	"beach_shore": "res://scenes/world/beach_shore.tscn",
	"ruined_village": "res://scenes/world/ruined_village.tscn",
	"tidal_caves": "res://scenes/world/tidal_caves.tscn",
	"dragon_palace_gate": "res://scenes/world/dragon_palace_gate.tscn",
	"ending_rewind": "res://scenes/world/ending_rewind.tscn",
	"ending_anchor": "res://scenes/world/ending_anchor.tscn",
	"ending_drift": "res://scenes/world/ending_drift.tscn",
}

const FLAG_ALIASES := {
	"caves_unlocked": "cave_entrance_unlocked",
}

var flags: Dictionary = {}
var party_field: Array[String] = []
var party_combat: Array[String] = []
var party_state: Dictionary = {}
var inventory: Dictionary = {}
var key_items: Array[String] = []
var gold: int = 0
var active_quests: Array[String] = []
var completed_scenes: Array[String] = []
var lore_collected: Array[String] = []
var current_zone: String = ""
var pending_spawn: String = "WorldSpawn"
var pending_dialogue: String = ""
var playtime_sec: float = 0.0

var characters: Dictionary = {}
var enemies: Dictionary = {}
var skills: Dictionary = {}
var items: Dictionary = {}
var encounters: Dictionary = {}
var encounters_by_trigger: Dictionary = {}
var quests: Dictionary = {}
var dialogue_scenes: Dictionary = {}
var lore_entries: Dictionary = {}
var lore_placements: Array = []
var story_scenes: Dictionary = {}


func _ready() -> void:
	_load_all_data()
	var required := [
		"res://data/story/scenes.json",
		"res://data/story/flags.json",
		"res://data/dialogue/chapter_01.json",
	]
	for path in required:
		if not FileAccess.file_exists(path):
			push_error("Missing required data: %s" % path)


func _process(delta: float) -> void:
	if current_zone != "":
		playtime_sec += delta


func load_json(path: String) -> Variant:
	if not FileAccess.file_exists(path):
		push_error("Missing JSON: %s" % path)
		return null
	var text := FileAccess.get_file_as_string(path)
	return JSON.parse_string(text)


func _load_all_data() -> void:
	var party_data: Dictionary = load_json("res://data/characters/party.json")
	for ch in party_data.get("characters", []):
		characters[ch.id] = ch

	var enemy_data: Dictionary = load_json("res://data/enemies/enemies.json")
	for e in enemy_data.get("enemies", []):
		enemies[e.id] = e

	var skill_data: Dictionary = load_json("res://data/skills/skills.json")
	for s in skill_data.get("skills", []):
		skills[s.id] = s

	var item_data: Dictionary = load_json("res://data/items/items.json")
	for it in item_data.get("items", []):
		items[it.id] = it

	var enc_data: Dictionary = load_json("res://data/encounters/story_encounters.json")
	for enc in enc_data.get("encounters", []):
		encounters[enc.id] = enc
		var zone: String = enc.get("zone", "")
		if not encounters_by_trigger.has(zone):
			encounters_by_trigger[zone] = {}
		encounters_by_trigger[zone][enc.trigger] = enc

	var quest_data: Dictionary = load_json("res://data/quests/main_quests.json")
	for q in quest_data.get("quests", []):
		quests[q.id] = q

	var dlg: Dictionary = load_json("res://data/dialogue/chapter_01.json")
	for sc in dlg.get("scenes", []):
		dialogue_scenes[sc.scene_id] = sc

	var lore_data: Dictionary = load_json("res://data/lore/lore_entries.json")
	for entry in lore_data.get("entries", []):
		lore_entries[entry.id] = entry

	var placement_data: Dictionary = load_json("res://data/lore/lore_placements.json")
	lore_placements = placement_data.get("placements", [])

	var spine: Dictionary = load_json("res://data/story/scenes.json")
	for sc in spine.get("scenes", []):
		story_scenes[sc.scene_id] = sc


func reset_new_game() -> void:
	var ng: Dictionary = load_json("res://data/starting/new_game.json")
	flags = ng.get("flags", {}).duplicate(true)
	party_field = _to_string_array(ng.get("party_field", ["urashima"]))
	party_combat = _to_string_array(ng.get("party_combat", ["urashima"]))
	inventory = ng.get("inventory", {}).duplicate(true)
	key_items = _to_string_array(ng.get("key_items", []))
	gold = int(ng.get("gold", 0))
	active_quests = _to_string_array(ng.get("quests_active", []))
	completed_scenes.clear()
	lore_collected.clear()
	playtime_sec = 0.0
	_init_party_state(int(ng.get("level", 1)), ng.get("equipment", {}))
	current_zone = str(ng.get("start_scene", "beach_shore"))


func _init_party_state(level: int, equipment: Dictionary) -> void:
	party_state.clear()
	for cid in ["urashima", "yuzu", "roku"]:
		if not characters.has(cid):
			continue
		var def: Dictionary = characters[cid]
		var stats := _stats_at_level(def, level)
		party_state[cid] = {
			"level": level,
			"xp": 0,
			"hp": stats.max_hp,
			"mp": stats.max_mp,
			"skills": def.starting_skills.duplicate(),
			"equipment": equipment.get(cid, {"weapon": null, "armor": null, "charm": null}).duplicate(true),
			"limit_gauge": 0.0,
			"limit_used": false,
		}


func _stats_at_level(def: Dictionary, level: int) -> Dictionary:
	var base: Dictionary = def.base_stats
	var growth: Dictionary = def.growth_per_level
	var lvl_bonus: int = maxi(level - 1, 0)
	return {
		"max_hp": int(base.max_hp + growth.max_hp * lvl_bonus),
		"max_mp": int(base.max_mp + growth.max_mp * lvl_bonus),
		"atk": int(base.atk + growth.atk * lvl_bonus),
		"def": int(base.def + growth.def * lvl_bonus),
		"mag": int(base.mag + growth.mag * lvl_bonus),
		"res": int(base.res + growth.res * lvl_bonus),
		"spd": int(base.spd + growth.spd * lvl_bonus),
	}


func get_character_stats(char_id: String) -> Dictionary:
	var def: Dictionary = characters.get(char_id, {})
	var ps: Dictionary = party_state.get(char_id, {})
	var stats := _stats_at_level(def, int(ps.get("level", 1)))
	var eq: Dictionary = ps.get("equipment", {})
	for slot in eq:
		var item_id = eq[slot]
		if item_id and items.has(item_id):
			var bonus: Dictionary = items[item_id].get("stat_bonus", {})
			for stat in bonus:
				if stats.has(stat):
					stats[stat] += int(bonus[stat])
	return stats


func set_flag(flag_id: String, value: Variant = true) -> void:
	var resolved: String = str(FLAG_ALIASES.get(flag_id, flag_id))
	flags[resolved] = value
	EventBus.flag_changed.emit(resolved, value)
	_check_quest_progress()
	SteamManager.on_flag_set(resolved, value)


func get_flag(flag_id: String, default: Variant = false) -> Variant:
	var resolved: String = str(FLAG_ALIASES.get(flag_id, flag_id))
	return flags.get(resolved, default)


func has_flag(flag_id: String) -> bool:
	var v = get_flag(flag_id, false)
	if v is bool:
		return v
	return v != null and str(v) != ""


func scene_done(scene_id: String) -> bool:
	return scene_id in completed_scenes


func mark_scene_done(scene_id: String) -> void:
	if scene_id not in completed_scenes:
		completed_scenes.append(scene_id)


func apply_dialogue_complete(data: Dictionary) -> void:
	var sf = data.get("set_flags", [])
	if sf is Dictionary:
		for key in sf:
			set_flag(str(key), sf[key])
	elif sf is Array:
		for flag in sf:
			set_flag(str(flag), true)
	for item_grant in data.get("give_items", []):
		add_item(str(item_grant.item_id), int(item_grant.get("quantity", 1)))
	for item_id in data.get("grant_items", []):
		add_item(str(item_id), 1)
	for key_id in data.get("grant_key_items", []):
		if str(key_id) not in key_items:
			key_items.append(str(key_id))
	var quest_id = data.get("start_quest", "")
	if quest_id != "" and quest_id not in active_quests:
		active_quests.append(str(quest_id))
		EventBus.quest_updated.emit(quest_id)
	for member in data.get("add_party", []):
		add_party_member(str(member))


func add_party_member(char_id: String) -> void:
	if char_id not in party_field:
		party_field.append(char_id)
	if char_id not in party_combat:
		party_combat.append(char_id)
	if not party_state.has(char_id) and characters.has(char_id):
		var def: Dictionary = characters[char_id]
		var stats := _stats_at_level(def, 1)
		party_state[char_id] = {
			"level": 1,
			"xp": 0,
			"hp": stats.max_hp,
			"mp": stats.max_mp,
			"skills": def.starting_skills.duplicate(),
			"equipment": {"weapon": null, "armor": null, "charm": null},
			"limit_gauge": 0.0,
			"limit_used": false,
		}
	EventBus.party_changed.emit()


func add_item(item_id: String, qty: int = 1) -> void:
	var def: Dictionary = items.get(item_id, {})
	if def.get("type", "") == "key_item":
		if item_id not in key_items:
			key_items.append(item_id)
		return
	inventory[item_id] = int(inventory.get(item_id, 0)) + qty
	EventBus.inventory_changed.emit()


func has_key_item(item_id: String) -> bool:
	return item_id in key_items


func add_gold(amount: int) -> void:
	gold += amount
	EventBus.gold_changed.emit(gold)


func collect_lore(lore_id: String) -> void:
	if lore_id in lore_collected:
		return
	lore_collected.append(lore_id)
	EventBus.lore_collected.emit(lore_id)


func get_encounter_for_trigger(zone_id: String, trigger: String) -> Dictionary:
	return encounters_by_trigger.get(zone_id, {}).get(trigger, {})


func get_active_quest_stage(quest_id: String) -> Dictionary:
	var quest: Dictionary = quests.get(quest_id, {})
	for stage in quest.get("stages", []):
		if not _stage_complete(stage):
			return stage
	return {}


func _stage_complete(stage: Dictionary) -> bool:
	var comp: Dictionary = stage.get("completion", {})
	if comp.has("flag"):
		return has_flag(str(comp.flag))
	if comp.has("all_flags"):
		for f in comp.all_flags:
			if not has_flag(str(f)):
				return false
		return true
	return false


func _check_quest_progress() -> void:
	for qid in active_quests:
		EventBus.quest_updated.emit(qid)


func get_save_dict() -> Dictionary:
	return {
		"flags": flags,
		"party_field": party_field,
		"party_combat": party_combat,
		"party_state": party_state,
		"inventory": inventory,
		"key_items": key_items,
		"gold": gold,
		"active_quests": active_quests,
		"completed_scenes": completed_scenes,
		"lore_collected": lore_collected,
		"current_zone": current_zone,
		"playtime_sec": playtime_sec,
	}


func load_save_dict(data: Dictionary) -> void:
	flags = data.get("flags", {})
	party_field = _to_string_array(data.get("party_field", []))
	party_combat = _to_string_array(data.get("party_combat", []))
	party_state = data.get("party_state", {})
	inventory = data.get("inventory", {})
	key_items = _to_string_array(data.get("key_items", []))
	gold = int(data.get("gold", 0))
	active_quests = _to_string_array(data.get("active_quests", []))
	completed_scenes = _to_string_array(data.get("completed_scenes", []))
	lore_collected = _to_string_array(data.get("lore_collected", []))
	current_zone = str(data.get("current_zone", "ruined_village"))
	playtime_sec = float(data.get("playtime_sec", 0.0))


func _to_string_array(arr: Array) -> Array[String]:
	var out: Array[String] = []
	for v in arr:
		out.append(str(v))
	return out


func go_to_zone(zone_id: String, spawn_marker: String = "WorldSpawn") -> void:
	if not ZONE_SCENES.has(zone_id):
		push_error("Unknown zone: %s" % zone_id)
		return
	pending_spawn = spawn_marker
	current_zone = zone_id
	EventBus.zone_changed.emit(zone_id)
	get_tree().change_scene_to_file(ZONE_SCENES[zone_id])
