extends Node
## Turn-based combat orchestrator.

enum Phase { INTRO, PLAYER_TURN, ENEMY_TURN, RESOLVE, VICTORY, DEFEAT }

var phase: Phase = Phase.INTRO
var turn_order: Array[Combatant] = []
var current_turn_index := 0
var allies: Array[Combatant] = []
var enemies: Array[Combatant] = []
var battle_log: Array[String] = []


func start_battle(enemy_ids: Array) -> void:
	_reset()
	for char_id in GameManager.party_ids:
		var def := GameManager.get_character_def(char_id)
		if not def.is_empty():
			allies.append(Combatant.new(def, true))
	for enemy_id in enemy_ids:
		var def := GameManager.get_enemy_def(enemy_id)
		if not def.is_empty():
			enemies.append(Combatant.new(def, false))
	_build_turn_order()
	phase = Phase.PLAYER_TURN
	EventBus.combat_started.emit()
	_log(LocalizationManager.tr_key("combat.battle_start"))
	_start_current_turn()


func _reset() -> void:
	allies.clear()
	enemies.clear()
	turn_order.clear()
	current_turn_index = 0
	battle_log.clear()
	phase = Phase.INTRO


func _build_turn_order() -> void:
	turn_order.clear()
	for a in allies:
		if a.is_alive():
			turn_order.append(a)
	for e in enemies:
		if e.is_alive():
			turn_order.append(e)
	turn_order.sort_custom(func(a, b): return a.spd > b.spd)
	current_turn_index = 0


func _start_current_turn() -> void:
	if _check_battle_end():
		return
	if turn_order.is_empty():
		_build_turn_order()
	if turn_order.is_empty():
		return
	while current_turn_index < turn_order.size() and not turn_order[current_turn_index].is_alive():
		current_turn_index += 1
	if current_turn_index >= turn_order.size():
		_end_round()
		return
	var actor: Combatant = turn_order[current_turn_index]
	actor.reset_defend()
	for msg in actor.tick_statuses():
		_log(msg)
	if not actor.is_alive():
		_advance_turn()
		return
	EventBus.turn_started.emit(null)
	if actor.is_player:
		phase = Phase.PLAYER_TURN
	else:
		phase = Phase.ENEMY_TURN
		_execute_enemy_turn(actor)


func _end_round() -> void:
	current_turn_index = 0
	_build_turn_order()
	_start_current_turn()


func _advance_turn() -> void:
	current_turn_index += 1
	_start_current_turn()


func player_action(action: String, actor_index: int, skill_id: String, target_index: int) -> void:
	if phase != Phase.PLAYER_TURN:
		return
	var actor := _get_current_player(actor_index)
	if actor == null:
		return
	match action:
		"attack":
			_execute_skill(actor, GameManager.get_skill_def("strike"), target_index, false)
		"skill":
			_execute_skill(actor, GameManager.get_skill_def(skill_id), target_index, false)
		"defend":
			actor.is_defending = true
			_log(LocalizationManager.tr_key("combat.defend", { "actor": actor.display_name }))
			_advance_turn()
		"item":
			_log("Item use not yet implemented.")
			_advance_turn()
		"limit":
			var limit_skill := _get_limit_skill(actor)
			if limit_skill.is_empty():
				return
			_execute_skill(actor, limit_skill, target_index, true)
	if _check_battle_end():
		return


func _get_current_player(index: int) -> Combatant:
	if index < 0 or index >= allies.size():
		return null
	return allies[index]


func _get_limit_skill(actor: Combatant) -> Dictionary:
	if not actor.can_use_limit():
		return {}
	var char_def := GameManager.get_character_def(actor.id)
	return GameManager.get_skill_def(char_def.get("limit_skill", ""))


func _execute_enemy_turn(actor: Combatant) -> void:
	var skill_id := SkillResolver.pick_enemy_skill(actor)
	var skill := GameManager.get_skill_def(skill_id)
	var target_idx := _pick_target_index(skill)
	_execute_skill(actor, skill, target_idx, false)


func _pick_target_index(skill: Dictionary) -> int:
	var target_type: String = skill.get("target", "single_enemy")
	match target_type:
		"single_enemy", "all_enemies":
			var living: Array[int] = []
			for i in allies.size():
				if allies[i].is_alive():
					living.append(i)
			return living[randi() % living.size()] if living.size() > 0 else 0
		_:
			return 0


func _execute_skill(actor: Combatant, skill: Dictionary, target_index: int, is_limit: bool) -> void:
	if skill.is_empty():
		_advance_turn()
		return
	var mp_cost: int = skill.get("mp_cost", 0)
	if mp_cost > 0 and not actor.spend_mp(mp_cost):
		_log(LocalizationManager.tr_key("combat.no_mp", { "actor": actor.display_name }))
		_advance_turn()
		return
	var targets := _resolve_targets(actor, skill, target_index)
	if skill.get("power", 0.0) > 0.0:
		for t in targets:
			var dmg := SkillResolver.resolve_damage(actor, t, skill)
			var dealt := t.take_damage(dmg)
			EventBus.damage_dealt.emit(null, dealt, skill.get("element", ""))
			var skill_name := LocalizationManager.skill_name(skill.get("id", ""))
			if skill_name == skill.get("id", ""):
				skill_name = skill.get("display_name", "?")
			_log(LocalizationManager.tr_key("combat.damage", {
				"actor": actor.display_name,
				"skill": skill_name,
				"target": t.display_name,
				"amount": dealt
			}))
			if not t.is_alive():
				EventBus.actor_defeated.emit(null)
				_log(LocalizationManager.tr_key("combat.defeated", { "target": t.display_name }))
		if actor.is_player:
			actor.add_limit(8)
	for msg in SkillResolver.apply_skill_effects(actor, targets, skill):
		_log(msg)
	if is_limit:
		actor.limit_gauge = 0
	_advance_turn()


func _resolve_targets(actor: Combatant, skill: Dictionary, target_index: int) -> Array:
	var result: Array = []
	var target_type: String = skill.get("target", "single_enemy")
	match target_type:
		"self":
			result.append(actor)
		"single_ally":
			var pool := allies if actor.is_player else enemies
			if target_index >= 0 and target_index < pool.size():
				result.append(pool[target_index])
		"all_allies":
			result.assign(allies if actor.is_player else enemies)
			result = result.filter(func(c): return c.is_alive())
		"single_enemy":
			var pool := enemies if actor.is_player else allies
			if target_index >= 0 and target_index < pool.size():
				result.append(pool[target_index])
		"all_enemies":
			result.assign(enemies if actor.is_player else allies)
			result = result.filter(func(c): return c.is_alive())
	return result


func _check_battle_end() -> bool:
	var allies_alive := allies.any(func(c): return c.is_alive())
	var enemies_alive := enemies.any(func(c): return c.is_alive())
	if not enemies_alive:
		phase = Phase.VICTORY
		_on_victory()
		return true
	if not allies_alive:
		phase = Phase.DEFEAT
		_on_defeat()
		return true
	return false


func _on_victory() -> void:
	var total_xp := 0
	var total_gold := 0
	for e in enemies:
		var def := GameManager.get_enemy_def(e.id)
		var rewards: Dictionary = def.get("rewards", {})
		total_xp += rewards.get("xp", 0)
		total_gold += rewards.get("gold", 0)
	GameManager.gold += total_gold
	_log(LocalizationManager.tr_key("combat.victory", { "xp": total_xp, "gold": total_gold }))
	GameManager.change_state(GameManager.GameState.EXPLORATION)
	EventBus.combat_ended.emit(true)


func _on_defeat() -> void:
	_log(LocalizationManager.tr_key("combat.defeat"))
	GameManager.change_state(GameManager.GameState.EXPLORATION)
	EventBus.combat_ended.emit(false)


func _log(message: String) -> void:
	battle_log.append(message)
	print("[Combat] %s" % message)
