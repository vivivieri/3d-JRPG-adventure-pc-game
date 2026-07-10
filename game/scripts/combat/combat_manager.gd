extends Node
## Turn-based combat engine — loads combat scene and resolves encounters.

const BattleUnitScript = preload("res://scripts/combat/battle_unit.gd")
const DamageCalc = preload("res://scripts/combat/damage_calculator.gd")

signal battle_ended(victory: bool)

var _encounter: Dictionary = {}
var _allies: Array = []
var _enemies: Array = []
var _turn_order: Array = []
var _turn_idx := 0
var _active := false
var _tutorial := false
var _escape_allowed := true
var _log: Array[String] = []
var _ui: Node = null
var _awaiting_player := false
var _current_actor = null


func start_encounter(encounter_id: String) -> void:
	_encounter = GameManager.encounters.get(encounter_id, {})
	if _encounter.is_empty():
		push_error("Unknown encounter: %s" % encounter_id)
		battle_ended.emit(false)
		return
	_tutorial = bool(_encounter.get("tutorial", false))
	_escape_allowed = bool(_encounter.get("escape_allowed", true))
	_build_units()
	_turn_order = _allies + _enemies
	_turn_order.sort_custom(func(a, b): return a.spd > b.spd)
	_turn_idx = 0
	_log.clear()
	_active = true
	EventBus.combat_started.emit(encounter_id)
	EventBus.scene_blocked_changed.emit(true)
	_ensure_ui()
	_ui.show_battle(self)
	_plan_enemy_intents()
	_next_turn()


func _build_units() -> void:
	_allies.clear()
	_enemies.clear()
	for cid in _encounter.get("party", GameManager.party_combat):
		if cid in GameManager.party_state:
			_allies.append(BattleUnitScript.from_party(str(cid)))
	for eid in _encounter.get("enemies", []):
		_enemies.append(BattleUnitScript.from_enemy(str(eid)))


func _ensure_ui() -> void:
	if _ui:
		return
	var packed := preload("res://scenes/combat/combat_scene.tscn")
	_ui = packed.instantiate()
	get_tree().root.add_child(_ui)


func _plan_enemy_intents() -> void:
	for e in _enemies:
		if not e.is_alive():
			continue
		var skill_id := _pick_enemy_skill(e)
		e.intent_skill = skill_id
		var sk: Dictionary = GameManager.skills.get(skill_id, {})
		e.intent_display = sk.get("target", "attack")


func _pick_enemy_skill(unit) -> String:
	var ai: Dictionary = unit.ai_data
	if ai.get("type", "") == "phase":
		for phase in ai.get("phases", []):
			if unit.hp_ratio() > float(phase.get("hp_above", 0.0)):
				return _weighted_pick(phase.get("weights", []), unit)
	elif ai.get("type", "") == "weighted":
		return _weighted_pick(ai.get("weights", []), unit)
	if unit.skills.size() > 0:
		return unit.skills[0]
	return "strike"


func _weighted_pick(weights: Array, unit) -> String:
	var pool: Array = []
	for entry in weights:
		if entry.has("hp_below") and unit.hp_ratio() > float(entry.hp_below):
			continue
		for i in int(entry.get("weight", 1)):
			pool.append(str(entry.skill_id))
	if pool.is_empty() and unit.skills.size() > 0:
		return unit.skills[0]
	return pool[randi() % pool.size()] if pool.size() > 0 else "strike"


func _next_turn() -> void:
	if not _active:
		return
	if _check_end():
		return
	_turn_idx = _turn_idx % _turn_order.size()
	var tries := 0
	while tries < _turn_order.size():
		_current_actor = _turn_order[_turn_idx]
		_turn_idx += 1
		if _current_actor.is_alive():
			break
		tries += 1
	if not _current_actor or not _current_actor.is_alive():
		_check_end()
		return
	_current_actor.defending = false
	if _current_actor.is_enemy:
		_do_enemy_turn(_current_actor)
	else:
		_awaiting_player = true
		_ui.prompt_player_action(_current_actor)


func player_action(action: String, skill_id: String = "", target_idx: int = 0) -> void:
	if not _awaiting_player or not _current_actor:
		return
	_awaiting_player = false
	match action:
		"attack":
			_execute_skill(_current_actor, "strike", _enemies[target_idx] if _enemies.size() > target_idx else null)
		"skill":
			_execute_skill(_current_actor, skill_id, _pick_target(_current_actor, skill_id, target_idx))
		"defend":
			_current_actor.defending = true
			_log.append("%s braces." % _current_actor.display_name)
		"item":
			_use_item(_current_actor, skill_id)
		"escape":
			if _try_escape():
				return
		"limit":
			_execute_skill(_current_actor, _current_actor.limit_skill, _enemies[0] if _enemies.size() > 0 else null)
	_ui.refresh()
	await get_tree().create_timer(0.35).timeout
	_next_turn()


func _pick_target(actor, skill_id: String, idx: int):
	var sk: Dictionary = GameManager.skills.get(skill_id, {})
	match sk.get("target", ""):
		"single_enemy":
			return _enemies[clampi(idx, 0, _enemies.size() - 1)] if _enemies.size() > 0 else null
		"single_ally", "self":
			if sk.target == "self":
				return actor
			return _allies[clampi(idx, 0, _allies.size() - 1)] if _allies.size() > 0 else null
		_:
			return null


func _do_enemy_turn(enemy) -> void:
	var target = _allies[0]
	for a in _allies:
		if a.is_alive():
			target = a
			break
	_execute_skill(enemy, enemy.intent_skill, target)
	_plan_enemy_intents()
	_ui.refresh()
	await get_tree().create_timer(0.45).timeout
	_next_turn()


func _execute_skill(actor, skill_id: String, target) -> void:
	var sk: Dictionary = GameManager.skills.get(skill_id, {})
	if sk.is_empty():
		return
	if int(sk.get("mp_cost", 0)) > actor.mp and not actor.is_enemy:
		_log.append("Not enough MP!")
		return
	if not actor.is_enemy:
		actor.mp -= int(sk.get("mp_cost", 0))
	var targets: Array = []
	match sk.get("target", ""):
		"single_enemy", "single_ally", "self":
			if target:
				targets = [target]
		"all_enemies":
			targets = _enemies if not actor.is_enemy else _allies
		"all_allies":
			targets = _allies if not actor.is_enemy else _enemies
		_:
			if target:
				targets = [target]
	for eff_target in targets:
		if not eff_target or not eff_target.is_alive():
			continue
		_apply_skill_damage(actor, eff_target, sk)
		_apply_skill_effects(actor, eff_target, sk)
	_log.append("%s uses %s." % [actor.display_name, sk.get("display_name", skill_id)])
	if sk.get("is_limit", false) and not actor.is_enemy:
		actor.limit_used = true
		actor.limit_gauge = 0.0
	_ui.refresh()


func _apply_skill_damage(actor, target, sk: Dictionary) -> void:
	var power := float(sk.get("power", 0.0))
	if power <= 0.0:
		return
	var stat_name := str(sk.get("power_stat", "atk"))
	var atk_val: int = actor.atk if stat_name == "atk" else actor.mag
	var def_val: int = target.def if stat_name == "atk" else target.res
	var pierce := float(sk.get("pierce_def", 0.0))
	var dmg := 0
	if stat_name == "atk":
		dmg = DamageCalc.physical_damage(atk_val, def_val, power, pierce)
	else:
		dmg = DamageCalc.magic_damage(atk_val, def_val, power)
	if sk.get("element", "") == "spirit" and target.is_enemy:
		dmg = int(dmg * target.spirit_weakness)
	if target.defending:
		dmg = int(dmg * 0.5)
	target.hp = max(0, target.hp - dmg)
	if not actor.is_enemy and target.is_enemy:
		actor.limit_gauge = min(100.0, actor.limit_gauge + dmg * 0.8)
	if actor.is_enemy and not target.is_enemy:
		target.limit_gauge = min(100.0, target.limit_gauge + dmg * 0.5)
	_log.append("  → %d damage to %s" % [dmg, target.display_name])
	if _tutorial and not actor.is_enemy and target.is_enemy and target.hp <= 0:
		pass
	if _tutorial and actor.is_enemy and not target.is_enemy and target.hp <= 0:
		target.hp = 1
		_log.append("  (Tutorial: Urashima holds on.)")


func _apply_skill_effects(_actor, target, sk: Dictionary) -> void:
	for eff in sk.get("effects", []):
		if randf() > float(eff.get("chance", 1.0)):
			continue
		match eff.get("type", ""):
			"heal":
				var amt := int(eff.get("potency", 0))
				target.hp = min(target.max_hp, target.hp + amt)
				_log.append("  → healed %s for %d" % [target.display_name, amt])
			"def_up", "def_down", "regen", "poison", "stun":
				target.statuses[str(eff.type)] = {
					"duration": int(eff.get("duration", 1)),
					"potency": int(eff.get("potency", 0)),
				}


func _use_item(actor, item_id: String) -> void:
	if int(GameManager.inventory.get(item_id, 0)) <= 0:
		return
	var def: Dictionary = GameManager.items.get(item_id, {})
	var effect: Dictionary = def.get("effect", {})
	match effect.get("type", ""):
		"heal_hp":
			actor.hp = min(actor.max_hp, actor.hp + int(effect.value))
		"heal_mp":
			actor.mp = min(actor.max_mp, actor.mp + int(effect.value))
	GameManager.inventory[item_id] = int(GameManager.inventory[item_id]) - 1
	_log.append("%s uses %s." % [actor.display_name, LocalizationManager.tr_text(def.get("display_name", ""))])


func _try_escape() -> bool:
	var party_spd := 0
	for a in _allies:
		party_spd += a.spd
	var enemy_spd := 0
	for e in _enemies:
		enemy_spd += e.spd
	if not _escape_allowed:
		_log.append("Cannot flee this battle!")
		return false
	if randf() < DamageCalc.flee_chance(party_spd, enemy_spd):
		_end_battle(false, true)
		return true
	_log.append("Escape failed!")
	return false


func _check_end() -> bool:
	var allies_alive := false
	for a in _allies:
		if a.is_alive():
			allies_alive = true
	var enemies_alive := false
	for e in _enemies:
		if e.is_alive():
			enemies_alive = true
	if not allies_alive:
		_end_battle(false)
		return true
	if not enemies_alive:
		_end_battle(true)
		return true
	return false


func _end_battle(victory: bool, escaped: bool = false) -> void:
	_active = false
	_awaiting_player = false
	for a in _allies:
		a.sync_to_party()
	if victory:
		var xp := 0
		var gold_reward := 0
		for e in _enemies:
			xp += int(e.rewards.get("xp", 0))
			gold_reward += int(e.rewards.get("gold", 0))
		GameManager.add_gold(gold_reward)
		_log.append("Victory! +%d XP, +%d gold" % [xp, gold_reward])
		var on_win: Dictionary = _encounter.get("on_win", {})
		GameManager.apply_dialogue_complete(on_win)
		if _encounter.has("scene_id"):
			GameManager.mark_scene_done(str(_encounter.scene_id))
	if _ui:
		_ui.show_result(victory or escaped, _log)
	EventBus.scene_blocked_changed.emit(false)
	EventBus.combat_finished.emit(victory)
	battle_ended.emit(victory or escaped)


func get_state() -> Dictionary:
	return {
		"allies": _allies,
		"enemies": _enemies,
		"log": _log,
		"current": _current_actor,
		"awaiting_player": _awaiting_player,
		"tutorial": _tutorial,
	}
