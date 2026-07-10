extends CanvasLayer
## Field menu — Items and Equipment tabs (Tab to toggle).


enum Tab { ITEMS, EQUIPMENT }

@onready var _root: Control = $MenuRoot
@onready var _items_panel: VBoxContainer = $MenuRoot/Panel/Margin/MainVBox/ItemsPanel
@onready var _item_list: VBoxContainer = $MenuRoot/Panel/Margin/MainVBox/ItemsPanel/ItemScroll/ItemList
@onready var _item_char_option: OptionButton = $MenuRoot/Panel/Margin/MainVBox/ItemsPanel/ItemCharRow/ItemCharOption
@onready var _equip_panel: VBoxContainer = $MenuRoot/Panel/Margin/MainVBox/EquipPanel
@onready var _char_option: OptionButton = $MenuRoot/Panel/Margin/MainVBox/EquipPanel/CharRow/CharOption
@onready var _slot_list: VBoxContainer = $MenuRoot/Panel/Margin/MainVBox/EquipPanel/SlotList
@onready var _equip_item_list: VBoxContainer = $MenuRoot/Panel/Margin/MainVBox/EquipPanel/EquipScroll/EquipItemList
@onready var _message_label: Label = $MenuRoot/Panel/Margin/MainVBox/MessageLabel
@onready var _items_tab: Button = $MenuRoot/Panel/Margin/MainVBox/TabRow/ItemsTab
@onready var _equip_tab: Button = $MenuRoot/Panel/Margin/MainVBox/TabRow/EquipTab
@onready var _close_btn: Button = $MenuRoot/Panel/Margin/MainVBox/CloseBtn

var _open := false
var _tab := Tab.ITEMS
var _selected_char := ""


func _ready() -> void:
	layer = 6
	_root.visible = false
	_items_tab.pressed.connect(func(): _show_tab(Tab.ITEMS))
	_equip_tab.pressed.connect(func(): _show_tab(Tab.EQUIPMENT))
	_close_btn.pressed.connect(close_menu)
	_char_option.item_selected.connect(_on_char_selected)
	EventBus.locale_changed.connect(_on_locale_changed)
	EventBus.party_changed.connect(_refresh)
	EventBus.equipment_changed.connect(func(_id): _refresh())
	_apply_fonts()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("menu"):
		if _open:
			close_menu()
		elif GameManager.state == GameManager.GameState.EXPLORATION:
			open_menu()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed("cancel") and _open:
		close_menu()
		get_viewport().set_input_as_handled()


func open_menu() -> void:
	_open = true
	_root.visible = true
	GameManager.change_state(GameManager.GameState.MENU)
	_message_label.text = ""
	_show_tab(_tab)
	AudioManager.play_sfx("ui_confirm")


func close_menu() -> void:
	_open = false
	_root.visible = false
	GameManager.change_state(GameManager.GameState.EXPLORATION)
	AudioManager.play_sfx("ui_cancel")


func _show_tab(tab: Tab) -> void:
	_tab = tab
	_items_panel.visible = tab == Tab.ITEMS
	_equip_panel.visible = tab == Tab.EQUIPMENT
	_refresh_tab_labels()
	if tab == Tab.ITEMS:
		_populate_items()
	else:
		_populate_equipment()


func _refresh() -> void:
	if _open:
		_show_tab(_tab)


func _populate_items() -> void:
	for child in _item_list.get_children():
		child.queue_free()
	_item_char_option.clear()
	for i in GameManager.party_ids.size():
		var char_id: String = GameManager.party_ids[i]
		_item_char_option.add_item(LocalizationManager.character_name(char_id), i)
		_item_char_option.set_item_metadata(i, char_id)
	if GameManager.party_ids.is_empty():
		return
	var target_id: String = GameManager.party_ids[0]
	if _item_char_option.item_count > 0:
		target_id = _item_char_option.get_item_metadata(0)
	for item_id in GameManager.get_field_item_ids():
		var btn := Button.new()
		var qty := GameManager.get_item_count(item_id)
		btn.text = "%s x%d" % [LocalizationManager.item_name(item_id), qty]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.pressed.connect(func() -> void:
			var idx := _item_char_option.selected
			var char_id: String = _item_char_option.get_item_metadata(idx)
			_use_item(item_id, char_id)
		)
		_item_list.add_child(btn)
	if _item_list.get_child_count() == 0:
		var lbl := Label.new()
		lbl.text = LocalizationManager.tr_key("UI_FIELD_NO_ITEMS")
		_item_list.add_child(lbl)


func _use_item(item_id: String, character_id: String) -> void:
	var result := GameManager.use_field_item(item_id, character_id)
	_message_label.text = result.get("message", "")
	_populate_items()


func _populate_equipment() -> void:
	_char_option.clear()
	for i in GameManager.party_ids.size():
		var char_id: String = GameManager.party_ids[i]
		_char_option.add_item(LocalizationManager.character_name(char_id), i)
		_char_option.set_item_metadata(i, char_id)
	if GameManager.party_ids.is_empty():
		_selected_char = ""
		return
	_selected_char = GameManager.party_ids[0]
	_char_option.select(0)
	_refresh_equipment_slots()
	_populate_equippable()


func _on_char_selected(index: int) -> void:
	_selected_char = _char_option.get_item_metadata(index)
	_refresh_equipment_slots()
	_populate_equippable()


func _refresh_equipment_slots() -> void:
	for child in _slot_list.get_children():
		child.queue_free()
	if _selected_char.is_empty():
		return
	for slot in ["weapon", "armor", "charm"]:
		var row := HBoxContainer.new()
		var slot_lbl := Label.new()
		slot_lbl.text = LocalizationManager.tr_key("equip.slot.%s" % slot)
		slot_lbl.custom_minimum_size.x = 120
		row.add_child(slot_lbl)
		var equipped_id: String = GameManager.get_equipment(_selected_char).get(slot, "")
		var name_lbl := Label.new()
		name_lbl.text = LocalizationManager.item_name(equipped_id) if not equipped_id.is_empty() else "—"
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		if not equipped_id.is_empty():
			var unequip := Button.new()
			unequip.text = LocalizationManager.tr_key("UI_EQUIP_UNEQUIP")
			unequip.pressed.connect(func() -> void: _unequip(slot))
			row.add_child(unequip)
		_slot_list.add_child(row)


func _populate_equippable() -> void:
	for child in _equip_item_list.get_children():
		child.queue_free()
	if _selected_char.is_empty():
		return
	for item_id in GameManager.get_equippable_items(_selected_char):
		var def := GameManager.get_item_def(item_id)
		var btn := Button.new()
		btn.text = "%s [%s]" % [LocalizationManager.item_name(item_id), LocalizationManager.tr_key("equip.slot.%s" % def.get("slot", ""))]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.pressed.connect(func() -> void: _equip(item_id))
		_equip_item_list.add_child(btn)
	if _equip_item_list.get_child_count() == 0:
		var lbl := Label.new()
		lbl.text = LocalizationManager.tr_key("UI_EQUIP_NONE")
		_equip_item_list.add_child(lbl)


func _equip(item_id: String) -> void:
	if GameManager.equip_item(_selected_char, item_id):
		_message_label.text = LocalizationManager.tr_key("field.equipped", {
			"item": LocalizationManager.item_name(item_id),
			"target": LocalizationManager.character_name(_selected_char),
		})
	_refresh_equipment_slots()
	_populate_equippable()


func _unequip(slot: String) -> void:
	if GameManager.unequip_slot(_selected_char, slot):
		_message_label.text = LocalizationManager.tr_key("field.unequipped", {
			"target": LocalizationManager.character_name(_selected_char),
			"slot": LocalizationManager.tr_key("equip.slot.%s" % slot),
		})
	_refresh_equipment_slots()
	_populate_equippable()


func _refresh_tab_labels() -> void:
	$MenuRoot/Panel/Margin/MainVBox/Title.text = LocalizationManager.tr_key("UI_MENU_TITLE")
	_items_tab.text = LocalizationManager.tr_key("UI_MENU_ITEMS")
	_equip_tab.text = LocalizationManager.tr_key("UI_MENU_EQUIPMENT")
	_close_btn.text = LocalizationManager.tr_key("UI_COMBAT_BACK")


func _on_locale_changed(_locale: String) -> void:
	_apply_fonts()
	_refresh_tab_labels()
	if _open:
		_show_tab(_tab)


func _apply_fonts() -> void:
	FontThemeManager.apply_to_control($MenuRoot)
