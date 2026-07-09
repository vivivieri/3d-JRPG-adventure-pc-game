class_name CombatActorSlot
extends PanelContainer
## Single combatant row — name, HP/MP bars, optional intent icon.

signal slot_pressed(index: int)

@onready var _name_label: Label = $Margin/VBox/NameLabel
@onready var _hp_bar: ProgressBar = $Margin/VBox/HpBar
@onready var _mp_row: HBoxContainer = $Margin/VBox/MpRow
@onready var _mp_bar: ProgressBar = $Margin/VBox/MpRow/MpBar
@onready var _limit_bar: ProgressBar = $Margin/VBox/LimitBar
@onready var _intent_label: Label = $Margin/VBox/IntentLabel
@onready var _select_btn: Button = $SelectButton

var slot_index := 0
var is_enemy_slot := false


func _ready() -> void:
	_select_btn.pressed.connect(func(): slot_pressed.emit(slot_index))
	_apply_fonts()


func configure(index: int, is_enemy: bool) -> void:
	slot_index = index
	is_enemy_slot = is_enemy
	_mp_row.visible = not is_enemy
	_limit_bar.visible = not is_enemy
	_intent_label.visible = is_enemy


func bind_combatant(combatant: Combatant) -> void:
	_name_label.text = combatant.display_name
	update_stats(combatant)


func update_stats(combatant: Combatant) -> void:
	_hp_bar.max_value = combatant.max_hp
	_hp_bar.value = combatant.hp
	if not is_enemy_slot:
		_mp_bar.max_value = maxi(combatant.max_mp, 1)
		_mp_bar.value = combatant.mp
		_limit_bar.max_value = Combatant.LIMIT_MAX
		_limit_bar.value = combatant.limit_gauge
	modulate = Color.WHITE if combatant.is_alive() else Color(0.45, 0.45, 0.45, 0.75)


func set_intent(intent_key: String, skill_id: String = "") -> void:
	if not is_enemy_slot:
		return
	var text := LocalizationManager.tr_key("intent.%s" % intent_key)
	if not skill_id.is_empty():
		var skill_name := LocalizationManager.skill_name(skill_id)
		if skill_name != skill_id:
			text = "%s — %s" % [text, skill_name]
	_intent_label.text = text
	_intent_label.visible = true


func clear_intent() -> void:
	_intent_label.visible = false
	_intent_label.text = ""


func set_targetable(active: bool) -> void:
	_select_btn.visible = active and modulate.a > 0.5
	if active:
		add_theme_stylebox_override(&"panel", _highlight_style())
	else:
		remove_theme_stylebox_override(&"panel")


func _highlight_style() -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = Color(0.14, 0.22, 0.28, 0.95)
	box.border_color = Color(0.831, 0.647, 0.353, 0.9)
	box.set_border_width_all(2)
	box.set_corner_radius_all(4)
	return box


func _apply_fonts() -> void:
	FontThemeManager.apply_combat_name(_name_label)
	FontThemeManager.apply_combat_hint(_intent_label)
