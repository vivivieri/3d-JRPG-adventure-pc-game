extends RefCounted

const Self = preload("res://scripts/combat/battle_unit.gd")

var id: String
var display_name: String
var is_enemy: bool
var element: String = "physical"
var max_hp: int
var hp: int
var max_mp: int
var mp: int
var atk: int
var def: int
var mag: int
var res: int
var spd: int
var skills: Array[String] = []
var statuses: Dictionary = {}
var defending := false
var intent_skill: String = ""
var intent_display: String = "attack"
var ai_data: Dictionary = {}
var rewards: Dictionary = {}
var limit_gauge := 0.0
var limit_used := false
var limit_skill := ""
var spirit_weakness := 1.0
var boss_phases: Array = []
var announced_phases: Array = []


static func from_party(char_id: String):
	var u = Self.new()
	var def: Dictionary = GameManager.characters[char_id]
	var ps: Dictionary = GameManager.party_state[char_id]
	var stats := GameManager.get_character_stats(char_id)
	u.id = char_id
	u.display_name = def.display_name
	u.is_enemy = false
	u.element = def.element
	u.max_hp = stats.max_hp
	u.hp = int(ps.hp)
	u.max_mp = stats.max_mp
	u.mp = int(ps.mp)
	u.atk = stats.atk
	u.def = stats.def
	u.mag = stats.mag
	u.res = stats.res
	u.spd = stats.spd
	u.skills = []
	for sid in ps.skills:
		u.skills.append(str(sid))
	u.limit_gauge = float(ps.get("limit_gauge", 0.0))
	u.limit_used = bool(ps.get("limit_used", false))
	u.limit_skill = str(def.get("limit_skill", ""))
	return u


static func from_enemy(enemy_id: String):
	var u = Self.new()
	var def: Dictionary = GameManager.enemies[enemy_id]
	var stats: Dictionary = def.stats
	u.id = enemy_id
	u.display_name = def.display_name
	u.is_enemy = true
	u.element = def.element
	u.max_hp = stats.max_hp
	u.hp = stats.max_hp
	u.atk = stats.atk
	u.def = stats.def
	u.mag = stats.mag
	u.res = stats.res
	u.spd = stats.spd
	for sid in def.skills:
		u.skills.append(str(sid))
	u.ai_data = def.get("ai", {})
	u.intent_display = str(def.get("intent_display", "attack"))
	u.rewards = def.get("rewards", {})
	u.spirit_weakness = float(def.get("spirit_weakness", 1.0))
	u.boss_phases = def.get("phases", [])
	return u


func sync_to_party() -> void:
	if is_enemy:
		return
	GameManager.party_state[id].hp = hp
	GameManager.party_state[id].mp = mp
	GameManager.party_state[id].limit_gauge = limit_gauge
	GameManager.party_state[id].limit_used = limit_used


func is_alive() -> bool:
	return hp > 0


func hp_ratio() -> float:
	return float(hp) / float(max_hp) if max_hp > 0 else 0.0
