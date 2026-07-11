extends CanvasLayer
## Combat UI — unit cards with HP/MP bars, placeholders, action menu, battle log.

const ENEMY_COLORS := {
	"salt_crab": Color(0.95, 0.55, 0.2),
	"tide_wraith": Color(0.35, 0.75, 0.95),
	"shore_wraith": Color(0.65, 0.35, 0.9),
	"palace_sentinel": Color(0.9, 0.78, 0.25),
	"tide_keeper": Color(0.2, 0.45, 0.85),
}

const ALLY_COLORS := {
	"urashima": Color(0.55, 0.78, 0.95),
	"yuzu": Color(0.85, 0.55, 0.75),
	"roku": Color(0.55, 0.7, 0.55),
}

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
		container.add_child(_make_unit_card(unit, is_enemy))


func _make_unit_card(unit, is_enemy: bool) -> PanelContainer:
	var card := PanelContainer.new()
	card.custom_minimum_size = Vector2(168 if is_enemy else 220, 0)
	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 10)
	margin.add_theme_constant_override("margin_right", 10)
	margin.add_theme_constant_override("margin_top", 8)
	margin.add_theme_constant_override("margin_bottom", 8)
	card.add_child(margin)
	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 6)
	margin.add_child(vbox)

	var placeholder := ColorRect.new()
	placeholder.custom_minimum_size = Vector2(72, 72)
	placeholder.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	var color: Color = ENEMY_COLORS.get(unit.id, Color(0.7, 0.7, 0.75))
	if not is_enemy:
		color = ALLY_COLORS.get(unit.id, Color(0.6, 0.75, 0.9))
	placeholder.color = color if unit.is_alive() else color.darkened(0.45)
	vbox.add_child(placeholder)

	var name_lbl := Label.new()
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.add_theme_font_size_override("font_size", 15)
	name_lbl.text = str(unit.display_name)
	vbox.add_child(name_lbl)

	vbox.add_child(_make_bar_row("HP", unit.hp, unit.max_hp, Color(0.35, 0.82, 0.45) if not is_enemy else Color(0.9, 0.35, 0.35)))

	if not is_enemy:
		vbox.add_child(_make_bar_row("MP", unit.mp, unit.max_mp, Color(0.35, 0.55, 0.95)))

	if is_enemy and unit.intent_skill != "":
		var sk: Dictionary = GameManager.skills.get(unit.intent_skill, {})
		var intent_lbl := Label.new()
		intent_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		intent_lbl.add_theme_font_size_override("font_size", 12)
		intent_lbl.add_theme_color_override("font_color", Color(0.95, 0.82, 0.45))
		intent_lbl.text = "Intent: %s" % sk.get("display_name", unit.intent_skill)
		vbox.add_child(intent_lbl)

	if not unit.is_alive():
		card.modulate = Color(0.55, 0.55, 0.55, 0.85)
	return card


func _make_bar_row(label_text: String, current: int, maximum: int, fill_color: Color) -> HBoxContainer:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 6)
	var tag := Label.new()
	tag.custom_minimum_size = Vector2(24, 0)
	tag.add_theme_font_size_override("font_size", 12)
	tag.text = label_text
	row.add_child(tag)
	var bar := ProgressBar.new()
	bar.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.custom_minimum_size = Vector2(80, 18)
	bar.max_value = maxi(maximum, 1)
	bar.value = current
	bar.show_percentage = false
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color(0.12, 0.14, 0.18)
	bg.corner_radius_top_left = 4
	bg.corner_radius_top_right = 4
	bg.corner_radius_bottom_left = 4
	bg.corner_radius_bottom_right = 4
	var fill := StyleBoxFlat.new()
	fill.bg_color = fill_color
	fill.corner_radius_top_left = 4
	fill.corner_radius_top_right = 4
	fill.corner_radius_bottom_left = 4
	fill.corner_radius_bottom_right = 4
	bar.add_theme_stylebox_override("background", bg)
	bar.add_theme_stylebox_override("fill", fill)
	row.add_child(bar)
	var val := Label.new()
	val.add_theme_font_size_override("font_size", 11)
	val.text = "%d/%d" % [current, maximum]
	row.add_child(val)
	return row


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
