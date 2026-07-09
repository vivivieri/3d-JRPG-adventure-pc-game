extends Node
## Turn-based combat orchestrator.

enum Phase { INTRO, PLAYER_TURN, ENEMY_TURN, RESOLVE, CHOICE, VICTORY, DEFEAT }

const ACTION_BEAT := 0.42
const ENEMY_INTENT_BEAT := 1.1

var phase: Phase = Phase.INTRO
var turn_order: Array[Combatant] = []
var current_turn_index := 0
var allies: Array[Combatant] = []
var enemies: Array[Combatant] = []
var battle_log: Array[String] = []
var current_actor: Combatant = null

var _pending_enemy: Dictionary = {}
var _advance_pending := false
var _triggered_phases: Dictionary = {}


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
	GameManager.change_state(GameManager.GameState.COMBAT)
	EventBus.combat_started.emit()
	_log(LocalizationManager.tr_key("combat.battle_start"))
	_emit_stats()
	_start_current_turn()


func resolve_pending_enemy_turn() -> void:
	if _pending_enemy.is_empty():
		return
	var actor: Combatant = _pending_enemy.get("actor")
	var skill_id: String = _pending_enemy.get("skill_id", "")
	_pending_enemy = {}
	if actor == null or not actor.is_alive():
		_schedule_advance(0.1)
		return
	var skill := GameManager.get_skill_def(skill_id)
	var target_idx := _pick_target_index(skill)
	_execute_skill(actor, skill, target_idx, false)


func is_boss_battle() -> bool:
	return enemies.any(func(e): return e.tier == "boss")


func can_escape() -> bool:
	return not is_boss_battle()


func _reset() -> void:
	allies.clear()
	enemies.clear()
	turn_order.clear()
	current_turn_index = 0
	current_actor = null
	battle_log.clear()
	_pending_enemy = {}
	_advance_pending = false
	_triggered_phases = {}
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
	if phase == Phase.CHOICE:
		return
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
	current_actor = actor
	actor.reset_defend()
	for msg in actor.tick_statuses():
		_log(msg)
	_emit_stats()
	if not actor.is_alive():
		_schedule_advance(0.1)
		return
	EventBus.turn_started.emit(_actor_payload(actor))
	if actor.is_player:
		phase = Phase.PLAYER_TURN
	else:
		phase = Phase.ENEMY_TURN
		_queue_enemy_turn(actor)


func _queue_enemy_turn(actor: Combatant) -> void:
	var skill_id := SkillResolver.pick_enemy_skill(actor)
	var enemy_def := GameManager.get_enemy_def(actor.id)
	var intent_key: String = enemy_def.get("intent_display", "attack")
	_pending_enemy = { "actor": actor, "skill_id": skill_id }
	EventBus.enemy_intent_shown.emit(actor.id, skill_id, intent_key)


func _end_round() -> void:
	current_turn_index = 0
	_build_turn_order()
	_start_current_turn()


func _schedule_advance(delay: float = ACTION_BEAT) -> void:
	if _advance_pending or phase in [Phase.VICTORY, Phase.DEFEAT, Phase.CHOICE]:
		return
	_advance_pending = true
	get_tree().create_timer(delay).timeout.connect(func() -> void:
		_advance_pending = false
		if phase in [Phase.VICTORY, Phase.DEFEAT]:
			return
		_advance_turn()
	, CONNECT_ONE_SHOT)


func _advance_turn() -> void:
	if current_actor:
		EventBus.turn_ended.emit(_actor_payload(current_actor))
	current_turn_index += 1
	_start_current_turn()


func resolve_ending_choice(ending_id: String) -> void:
	if phase != Phase.CHOICE:
		return
	GameManager.chosen_ending = ending_id
	GameManager.set_flag("tide_keeper_defeated")
	EventBus.ending_chosen.emit(ending_id)
	phase = Phase.VICTORY
	_on_victory()


func player_action(action: String, skill_id: String = "", target_index: int = 0) -> void:
	if phase == Phase.CHOICE:
		return
	if phase != Phase.PLAYER_TURN or current_actor == null or not current_actor.is_player:
		return
	if _advance_pending:
		return
	var actor := current_actor
	match action:
		"attack":
			_execute_skill(actor, GameManager.get_skill_def("strike"), target_index, false)
		"skill":
			_execute_skill(actor, GameManager.get_skill_def(skill_id), target_index, false)
		"defend":
			actor.is_defending = true
			_log(LocalizationManager.tr_key("combat.defend", { "actor": actor.display_name }))
			_schedule_advance()
		"item":
			player_use_item(skill_id, target_index)
		"escape":
			try_escape()
		"limit":
			var limit_skill := _get_limit_skill(actor)
			if limit_skill.is_empty():
				return
			_execute_skill(actor, limit_skill, target_index, true)
	if _check_battle_end():
		return


func player_use_item(item_id: String, target_index: int) -> void:
	if phase != Phase.PLAYER_TURN or current_actor == null:
		return
	if GameManager.get_item_count(item_id) <= 0:
		return
	var item_def := GameManager.get_item_def(item_id)
	if item_def.is_empty() or not item_def.get("battle_use", false):
		return
	if target_index < 0 or target_index >= allies.size():
		return
	var target := allies[target_index]
	if not target.is_alive():
		return
	var effect: Dictionary = item_def.get("effect", {})
	var item_name := LocalizationManager.item_name(item_id)
	match effect.get("type", ""):
		"heal_hp":
			var healed := target.heal(effect.get("value", 0))
			_log(LocalizationManager.tr_key("combat.item_heal_hp", {
				"user": current_actor.display_name,
				"item": item_name,
				"target": target.display_name,
				"amount": healed,
			}))
		"heal_mp":
			var before := target.mp
			target.restore_mp(effect.get("value", 0))
			var restored := target.mp - before
			_log(LocalizationManager.tr_key("combat.item_heal_mp", {
				"user": current_actor.display_name,
				"item": item_name,
				"target": target.display_name,
				"amount": restored,
			}))
		"cure_status":
			var status_type: String = effect.get("status", "poison")
			if target.has_status(status_type):
				target.cure_status(status_type)
				_log(LocalizationManager.tr_key("combat.item_cure", {
					"user": current_actor.display_name,
					"item": item_name,
					"target": target.display_name,
					"status": LocalizationManager.tr_key("status.%s" % status_type),
				}))
			else:
				_log(LocalizationManager.tr_key("combat.item_no_effect", {
					"user": current_actor.display_name,
					"item": item_name,
					"target": target.display_name,
				}))
				_schedule_advance()
				return
		_:
			_schedule_advance()
			return
	GameManager.consume_item(item_id)
	_emit_stats()
	_schedule_advance()


func try_escape() -> void:
	if not can_escape():
		_log(LocalizationManager.tr_key("combat.escape_blocked"))
		_schedule_advance()
		return
	if randf() > 0.8:
		_log(LocalizationManager.tr_key("combat.escape_fail"))
		_schedule_advance()
		return
	_log(LocalizationManager.tr_key("combat.escape_success"))
	phase = Phase.RESOLVE
	GameManager.change_state(GameManager.GameState.EXPLORATION)
	EventBus.combat_escaped.emit()


func _get_limit_skill(actor: Combatant) -> Dictionary:
	if not actor.can_use_limit():
		return {}
	var char_def := GameManager.get_character_def(actor.id)
	return GameManager.get_skill_def(char_def.get("limit_skill", ""))


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
		_schedule_advance(0.1)
		return
	var mp_cost: int = skill.get("mp_cost", 0)
	if mp_cost > 0 and not actor.spend_mp(mp_cost):
		_log(LocalizationManager.tr_key("combat.no_mp", { "actor": actor.display_name }))
		_schedule_advance()
		return
	var targets := _resolve_targets(actor, skill, target_index)
	if skill.get("power", 0.0) > 0.0:
		for t in targets:
			var dmg := SkillResolver.resolve_damage(actor, t, skill)
			var dealt := t.take_damage(dmg)
			EventBus.damage_dealt.emit(t.id, dealt, skill.get("element", ""))
			var skill_name := LocalizationManager.skill_name(skill.get("id", ""))
			if skill_name == skill.get("id", ""):
				skill_name = skill.get("display_name", "?")
			_log(LocalizationManager.tr_key("combat.damage", {
				"actor": actor.display_name,
				"skill": skill_name,
				"target": t.display_name,
				"amount": dealt
			}))
			_check_boss_phases(t)
			if phase == Phase.CHOICE:
				_emit_stats()
				return
			if not t.is_alive():
				EventBus.actor_defeated.emit(t.id)
				_log(LocalizationManager.tr_key("combat.defeated", { "target": t.display_name }))
		if actor.is_player:
			actor.add_limit(8)
	for msg in SkillResolver.apply_skill_effects(actor, targets, skill):
		_log(msg)
		for t in targets:
			if t is Combatant:
				_check_boss_phases(t)
			if phase == Phase.CHOICE:
				_emit_stats()
				return
	if is_limit:
		actor.limit_gauge = 0
	_emit_stats()
	if _check_battle_end():
		return
	_schedule_advance()


func _check_boss_phases(target: Combatant) -> void:
	var enemy_index := enemies.find(target)
	if enemy_index < 0:
		return
	var enemy_def := GameManager.get_enemy_def(target.id)
	for phase_data in enemy_def.get("phases", []):
		var threshold: float = phase_data.get("hp_threshold", 1.0)
		var phase_key := "%s:%s" % [target.id, threshold]
		if _triggered_phases.has(phase_key):
			continue
		var hp_ratio := float(target.hp) / float(maxi(target.max_hp, 1))
		if hp_ratio > threshold:
			continue
		_triggered_phases[phase_key] = true
		var percent := int(threshold * 100.0)
		var message := LocalizationManager.tr_key("boss.%s.%d" % [target.id, percent])
		if message == "boss.%s.%d" % [target.id, percent]:
			message = phase_data.get("announcement", "")
		EventBus.boss_phase_announced.emit(target.id, message)
		if phase_data.get("triggers_choice", false):
			phase = Phase.CHOICE
			EventBus.boss_choice_required.emit(target.id)


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


func _actor_payload(actor: Combatant) -> Dictionary:
	return {
		"id": actor.id,
		"name": actor.display_name,
		"is_player": actor.is_player,
		"party_index": allies.find(actor),
	}


func _emit_stats() -> void:
	EventBus.combat_stats_changed.emit()


func _log(message: String) -> void:
	battle_log.append(message)
	EventBus.combat_log_appended.emit(message)
	print("[Combat] %s" % message)
