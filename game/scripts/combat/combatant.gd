class_name Combatant
extends RefCounted
## Runtime combat entity — party member or enemy instance.

var id: String
var display_name: String
var is_player: bool
var element: String
var hp: int
var max_hp: int
var mp: int
var max_mp: int
var atk: int
var def: int
var mag: int
var res: int
var spd: int
var skills: Array[String] = []
var statuses: Array[Dictionary] = []
var limit_gauge: int = 0
var is_defending: bool = false
var ai_data: Dictionary = {}
var tier: String = "normal"

const LIMIT_MAX := 100


func _init(definition: Dictionary, player: bool) -> void:
	id = definition.get("id", "")
	display_name = definition.get("display_name", id)
	is_player = player
	element = definition.get("element", "physical")
	tier = definition.get("tier", "normal")
	var stats: Dictionary = definition.get("stats", definition.get("base_stats", {}))
	max_hp = stats.get("max_hp", 50)
	hp = max_hp
	max_mp = stats.get("max_mp", 10)
	mp = max_mp
	atk = stats.get("atk", 5)
	def = stats.get("def", 5)
	mag = stats.get("mag", 5)
	res = stats.get("res", 5)
	spd = stats.get("spd", 5)
	for s in definition.get("skills", definition.get("starting_skills", [])):
		skills.append(s)
	ai_data = definition.get("ai", {})


func is_alive() -> bool:
	return hp > 0


func heal(amount: int) -> int:
	var before := hp
	hp = mini(hp + amount, max_hp)
	return hp - before


func restore_mp(amount: int) -> void:
	mp = mini(mp + amount, max_mp)


func take_damage(amount: int) -> int:
	if is_defending:
		amount = maxi(1, int(amount * 0.5))
	var dealt := mini(amount, hp)
	hp -= dealt
	if is_player:
		limit_gauge = mini(limit_gauge + 12, LIMIT_MAX)
	return dealt


func add_limit(amount: int) -> void:
	limit_gauge = mini(limit_gauge + amount, LIMIT_MAX)


func can_use_limit() -> bool:
	return is_player and limit_gauge >= LIMIT_MAX


func spend_mp(cost: int) -> bool:
	if mp < cost:
		return false
	mp -= cost
	return true


func reset_defend() -> void:
	is_defending = false


func apply_status(effect: Dictionary) -> void:
	statuses.append({
		"type": effect.get("type", ""),
		"duration": effect.get("duration", 1),
		"potency": effect.get("potency", 0),
	})


func tick_statuses() -> Array[String]:
	var messages: Array[String] = []
	var remaining: Array[Dictionary] = []
	for s in statuses:
		var type: String = s.get("type", "")
		var potency: int = s.get("potency", 0)
		match type:
			"poison":
				var dmg := take_damage(potency)
				messages.append("%s takes %d poison damage." % [display_name, dmg])
			"regen":
				var healed := heal(potency)
				messages.append("%s regenerates %d HP." % [display_name, healed])
		s["duration"] = s.get("duration", 1) - 1
		if s.get("duration", 0) > 0:
			remaining.append(s)
	statuses = remaining
	return messages
