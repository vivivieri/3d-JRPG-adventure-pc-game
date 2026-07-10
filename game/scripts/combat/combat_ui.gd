extends CanvasLayer
## Combat UI — HP bars, action menu, battle log.

@onready var _ally_box: VBoxContainer = %AllyBox
@onready var _enemy_box: HBoxContainer = %EnemyBox
@onready var _log: RichTextLabel = %BattleLog
@onready var _actions: HBoxContainer = %Actions
@onready var _result: PanelContainer = %ResultPanel
@onready var _result_label: Label = %ResultLabel

var _engine: Node = null


func _ready() -> void:
	hide()
	_result.hide()


func show_battle(engine: Node) -> void:
	_engine = engine
	show()
	_result.hide()
	refresh()


func refresh() -> void:
	if not _engine:
		return
	var state: Dictionary = _engine.get_state()
	_render_units(state.allies, _ally_box, false)
	_render_units(state.enemies, _enemy_box, true)
	_log.text = "\n".join(state.log)
	_build_actions(state)


func _render_units(units: Array, container: Node, is_enemy: bool) -> void:
	for child in container.get_children():
		child.queue_free()
	for unit in units:
		var lbl := Label.new()
		var intent := ""
		if is_enemy and unit.intent_skill != "":
			intent = " [%s]" % unit.intent_skill
		lbl.text = "%s %d/%d%s" % [unit.display_name, unit.hp, unit.max_hp, intent]
		if not unit.is_alive():
			lbl.modulate = Color(0.5, 0.5, 0.5)
		container.add_child(lbl)


func _build_actions(state: Dictionary) -> void:
	for child in _actions.get_children():
		child.queue_free()
	if not state.awaiting_player:
		return
	var actor = state.current
	if not actor:
		return
	var attack := Button.new()
	attack.text = "Attack"
	attack.pressed.connect(_engine.player_action.bind("attack", "", 0))
	_actions.add_child(attack)
	for sid in actor.skills:
		var sk: Dictionary = GameManager.skills.get(sid, {})
		if sk.get("is_limit", false):
			continue
		var btn := Button.new()
		btn.text = "%s (%d MP)" % [sk.get("display_name", sid), int(sk.get("mp_cost", 0))]
		btn.pressed.connect(_engine.player_action.bind("skill", sid, 0))
		_actions.add_child(btn)
	if not actor.limit_used and actor.limit_gauge >= 100.0 and actor.limit_skill != "":
		var lim := Button.new()
		lim.text = "LIMIT"
		lim.pressed.connect(_engine.player_action.bind("limit", "", 0))
		_actions.add_child(lim)
	var defend := Button.new()
	defend.text = "Defend"
	defend.pressed.connect(_engine.player_action.bind("defend", "", 0))
	_actions.add_child(defend)
	if int(GameManager.inventory.get("sea_salve", 0)) > 0:
		var item := Button.new()
		item.text = "Sea Salve"
		item.pressed.connect(_engine.player_action.bind("item", "sea_salve", 0))
		_actions.add_child(item)
	var flee := Button.new()
	flee.text = "Escape"
	flee.pressed.connect(_engine.player_action.bind("escape", "", 0))
	_actions.add_child(flee)


func prompt_player_action(_actor) -> void:
	refresh()


func show_result(victory: bool, log_lines: Array) -> void:
	_result.show()
	_result_label.text = "Victory!" if victory else "Defeated..."
	_log.text = "\n".join(log_lines)
	await get_tree().create_timer(2.5).timeout
	hide()
	_result.hide()
