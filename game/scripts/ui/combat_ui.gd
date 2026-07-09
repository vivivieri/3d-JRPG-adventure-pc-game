extends CanvasLayer
## Turn-based combat overlay — party/enemy bars, action menu, battle log.

enum MenuState { MAIN, SKILL, TARGET }

const ACTOR_SLOT_SCENE := preload("res://scenes/ui/combat_actor_slot.tscn")
const ENEMY_TURN_DELAY := 1.1

@onready var _root: Control = $CombatRoot
@onready var _party_row: HBoxContainer = $CombatRoot/Layout/PartyRow
@onready var _enemy_row: HBoxContainer = $CombatRoot/Layout/TopRow/EnemyRow
@onready var _turn_label: Label = $CombatRoot/Layout/TopRow/TurnLabel
@onready var _log_label: RichTextLabel = $CombatRoot/Layout/LogPanel/LogLabel
@onready var _action_panel: PanelContainer = $CombatRoot/Layout/BottomRow/ActionPanel
@onready var _main_actions: GridContainer = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/MainActions
@onready var _attack_btn: Button = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/MainActions/AttackBtn
@onready var _skill_btn: Button = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/MainActions/SkillBtn
@onready var _defend_btn: Button = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/MainActions/DefendBtn
@onready var _limit_btn: Button = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/MainActions/LimitBtn
@onready var _skill_panel: VBoxContainer = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/SkillPanel
@onready var _skill_list: VBoxContainer = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/SkillPanel/SkillList
@onready var _skill_back_btn: Button = $CombatRoot/Layout/BottomRow/ActionPanel/Margin/ActionVBox/SkillPanel/SkillBackBtn
@onready var _target_panel: PanelContainer = $CombatRoot/Layout/BottomRow/TargetPanel
@onready var _target_list: HBoxContainer = $CombatRoot/Layout/BottomRow/TargetPanel/Margin/TargetVBox/TargetList
@onready var _target_cancel_btn: Button = $CombatRoot/Layout/BottomRow/TargetPanel/Margin/TargetVBox/TargetCancelBtn
@onready var _result_overlay: ColorRect = $CombatRoot/ResultOverlay
@onready var _result_label: Label = $CombatRoot/ResultOverlay/ResultLabel

var _party_slots: Array[CombatActorSlot] = []
var _enemy_slots: Array[CombatActorSlot] = []
var _menu_state := MenuState.MAIN
var _pending_action := ""
var _pending_skill_id := ""
var _enemy_timer: SceneTreeTimer


func _ready() -> void:
	layer = 8
	_root.visible = false
	_connect_buttons()
	EventBus.combat_started.connect(_on_combat_started)
	EventBus.combat_ended.connect(_on_combat_ended)
	EventBus.turn_started.connect(_on_turn_started)
	EventBus.enemy_intent_shown.connect(_on_enemy_intent_shown)
	EventBus.combat_log_appended.connect(_on_combat_log_appended)
	EventBus.combat_stats_changed.connect(_on_combat_stats_changed)
	EventBus.locale_changed.connect(_on_locale_changed)
	_apply_fonts()


func _connect_buttons() -> void:
	_attack_btn.pressed.connect(func(): _begin_action("attack"))
	_skill_btn.pressed.connect(_open_skill_menu)
	_defend_btn.pressed.connect(func(): _submit_action("defend", "", 0))
	_limit_btn.pressed.connect(func(): _begin_action("limit"))
	_skill_back_btn.pressed.connect(_show_main_menu)
	_target_cancel_btn.pressed.connect(_show_main_menu)


func _on_combat_started() -> void:
	_root.visible = true
	_result_overlay.visible = false
	_clear_log()
	_build_slots()
	_refresh_all_stats()
	_show_main_menu()
	_set_action_panel_enabled(false)


func _on_combat_ended(victory: bool) -> void:
	_set_action_panel_enabled(false)
	_target_panel.visible = false
	_result_overlay.visible = true
	_result_label.text = _get_victory_text() if victory else LocalizationManager.tr_key("combat.defeat")
	await get_tree().create_timer(1.8).timeout
	_root.visible = false
	_result_overlay.visible = false


func _get_victory_text() -> String:
	var xp := 0
	var gold := 0
	for e in CombatManager.enemies:
		var def := GameManager.get_enemy_def(e.id)
		var rewards: Dictionary = def.get("rewards", {})
		xp += rewards.get("xp", 0)
		gold += rewards.get("gold", 0)
	return LocalizationManager.tr_key("combat.victory", { "xp": xp, "gold": gold })


func _on_turn_started(_actor_data: Dictionary) -> void:
	_refresh_all_stats()
	_show_main_menu()
	var actor := CombatManager.current_actor
	if actor == null:
		return
	if actor.is_player:
		_turn_label.text = LocalizationManager.tr_key("UI_COMBAT_YOUR_TURN", {
			"name": actor.display_name
		})
		_set_action_panel_enabled(true)
		_limit_btn.visible = actor.can_use_limit()
	else:
		_turn_label.text = LocalizationManager.tr_key("UI_COMBAT_ENEMY_TURN")
		_set_action_panel_enabled(false)


func _on_enemy_intent_shown(enemy_id: String, skill_id: String, intent_key: String) -> void:
	for i in _enemy_slots.size():
		if i < CombatManager.enemies.size() and CombatManager.enemies[i].id == enemy_id:
			_enemy_slots[i].set_intent(intent_key, skill_id)
	if _enemy_timer:
		_enemy_timer = null
	_enemy_timer = get_tree().create_timer(ENEMY_TURN_DELAY)
	_enemy_timer.timeout.connect(func(): CombatManager.resolve_pending_enemy_turn())


func _on_combat_log_appended(message: String) -> void:
	_log_label.append_text(message + "\n")
	while _log_label.get_line_count() > 8:
		var text := _log_label.text
		var idx := text.find("\n")
		if idx == -1:
			break
		_log_label.text = text.substr(idx + 1)


func _on_combat_stats_changed() -> void:
	_refresh_all_stats()


func _on_locale_changed(_locale_code: String) -> void:
	_apply_fonts()
	_refresh_action_labels()
	_refresh_all_stats()


func _build_slots() -> void:
	_clear_slots()
	for i in CombatManager.allies.size():
		var slot: CombatActorSlot = ACTOR_SLOT_SCENE.instantiate()
		slot.configure(i, false)
		slot.bind_combatant(CombatManager.allies[i])
		slot.slot_pressed.connect(_on_target_selected)
		_party_row.add_child(slot)
		_party_slots.append(slot)
	for i in CombatManager.enemies.size():
		var slot: CombatActorSlot = ACTOR_SLOT_SCENE.instantiate()
		slot.configure(i, true)
		slot.bind_combatant(CombatManager.enemies[i])
		slot.slot_pressed.connect(_on_target_selected)
		_enemy_row.add_child(slot)
		_enemy_slots.append(slot)


func _clear_slots() -> void:
	for slot in _party_slots:
		slot.queue_free()
	for slot in _enemy_slots:
		slot.queue_free()
	_party_slots.clear()
	_enemy_slots.clear()


func _refresh_all_stats() -> void:
	for i in _party_slots.size():
		if i < CombatManager.allies.size():
			_party_slots[i].update_stats(CombatManager.allies[i])
	for i in _enemy_slots.size():
		if i < CombatManager.enemies.size():
			_enemy_slots[i].update_stats(CombatManager.enemies[i])
			if not CombatManager.enemies[i].is_alive():
				_enemy_slots[i].clear_intent()


func _show_main_menu() -> void:
	_menu_state = MenuState.MAIN
	_pending_action = ""
	_pending_skill_id = ""
	_action_panel.visible = true
	_skill_panel.visible = false
	_target_panel.visible = false
	_clear_target_highlights()


func _open_skill_menu() -> void:
	var actor := CombatManager.current_actor
	if actor == null or not actor.is_player:
		return
	_menu_state = MenuState.SKILL
	_skill_panel.visible = true
	_populate_skill_list(actor)


func _populate_skill_list(actor: Combatant) -> void:
	for child in _skill_list.get_children():
		child.queue_free()
	for skill_id in actor.skills:
		var skill := GameManager.get_skill_def(skill_id)
		if skill.is_empty() or skill.get("is_limit", false):
			continue
		var btn := Button.new()
		var mp_cost: int = skill.get("mp_cost", 0)
		var name := LocalizationManager.skill_name(skill_id)
		btn.text = "%s (%d MP)" % [name, mp_cost] if mp_cost > 0 else name
		btn.disabled = mp_cost > actor.mp
		FontThemeManager.apply_combat_action(btn)
		btn.pressed.connect(func(): _on_skill_chosen(skill_id))
		_skill_list.add_child(btn)


func _on_skill_chosen(skill_id: String) -> void:
	_pending_action = "skill"
	_pending_skill_id = skill_id
	var skill := GameManager.get_skill_def(skill_id)
	_open_target_selection(skill)


func _begin_action(action: String) -> void:
	_pending_action = action
	_pending_skill_id = ""
	if action == "attack":
		_open_target_selection(GameManager.get_skill_def("strike"))
	elif action == "limit":
		var actor := CombatManager.current_actor
		if actor == null:
			return
		var char_def := GameManager.get_character_def(actor.id)
		_open_target_selection(GameManager.get_skill_def(char_def.get("limit_skill", "")))


func _open_target_selection(skill: Dictionary) -> void:
	var target_type: String = skill.get("target", "single_enemy")
	if target_type in ["self", "all_allies", "all_enemies"]:
		_submit_action(_pending_action, _pending_skill_id, 0)
		return
	_menu_state = MenuState.TARGET
	_action_panel.visible = false
	_target_panel.visible = true
	_clear_target_highlights()
	var enemy_targets := target_type in ["single_enemy"]
	for i in _enemy_slots.size():
		var active := enemy_targets and i < CombatManager.enemies.size() and CombatManager.enemies[i].is_alive()
		_enemy_slots[i].set_targetable(active)
	for i in _party_slots.size():
		var active := not enemy_targets and i < CombatManager.allies.size() and CombatManager.allies[i].is_alive()
		_party_slots[i].set_targetable(active)


func _on_target_selected(index: int) -> void:
	if _menu_state != MenuState.TARGET:
		return
	_submit_action(_pending_action, _pending_skill_id, index)


func _submit_action(action: String, skill_id: String, target_index: int) -> void:
	_set_action_panel_enabled(false)
	_show_main_menu()
	CombatManager.player_action(action, skill_id, target_index)


func _clear_target_highlights() -> void:
	for slot in _party_slots:
		slot.set_targetable(false)
	for slot in _enemy_slots:
		slot.set_targetable(false)


func _set_action_panel_enabled(enabled: bool) -> void:
	_attack_btn.disabled = not enabled
	_skill_btn.disabled = not enabled
	_defend_btn.disabled = not enabled
	_limit_btn.disabled = not enabled


func _clear_log() -> void:
	_log_label.clear()


func _refresh_action_labels() -> void:
	_attack_btn.text = LocalizationManager.tr_key("UI_ACTION_ATTACK")
	_skill_btn.text = LocalizationManager.tr_key("UI_ACTION_SKILL")
	_defend_btn.text = LocalizationManager.tr_key("UI_ACTION_DEFEND")
	_limit_btn.text = LocalizationManager.tr_key("UI_ACTION_LIMIT")
	_skill_back_btn.text = LocalizationManager.tr_key("UI_COMBAT_BACK")
	_target_cancel_btn.text = LocalizationManager.tr_key("UI_COMBAT_CANCEL")


func _apply_fonts() -> void:
	FontThemeManager.apply_combat_title(_turn_label)
	FontThemeManager.apply_combat_log(_log_label)
	_refresh_action_labels()
	for btn in [_attack_btn, _skill_btn, _defend_btn, _limit_btn, _skill_back_btn, _target_cancel_btn]:
		FontThemeManager.apply_combat_action(btn)
