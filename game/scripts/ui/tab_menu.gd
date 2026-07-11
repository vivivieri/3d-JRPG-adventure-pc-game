extends CanvasLayer
## Tab pause menu — Items, Equipment, Party, Key Items, Shop.

signal closed

@onready var _panel: PanelContainer = %Panel
@onready var _gold: Label = %GoldLabel
@onready var _tabs: TabContainer = %TabContainer
@onready var _items_list: ItemList = %ItemsList
@onready var _item_detail: RichTextLabel = %ItemDetail
@onready var _equip_char: OptionButton = %EquipCharOption
@onready var _equip_slots: ItemList = %EquipSlotsList
@onready var _party_list: ItemList = %PartyList
@onready var _party_detail: RichTextLabel = %PartyDetail
@onready var _key_list: ItemList = %KeyItemsList
@onready var _shop_list: ItemList = %ShopList
@onready var _shop_detail: RichTextLabel = %ShopDetail
@onready var _shop_tab: Control = %ShopTab

var _open := false
var _shop_vendor := ""
var _selected_item := ""


func _ready() -> void:
	hide()
	_items_list.item_selected.connect(_on_item_selected)
	_equip_char.item_selected.connect(func(_i): _refresh_equipment())
	_shop_list.item_selected.connect(_on_shop_item_selected)


func open_menu() -> void:
	_shop_vendor = ""
	_shop_tab.visible = false
	_open = true
	show()
	_refresh_all()
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE


func open_shop(vendor_id: String) -> void:
	if not GameManager.has_flag(str(ShopManager.get_vendor(vendor_id).get("requires_flag", "met_roku"))):
		return
	_shop_vendor = vendor_id
	_shop_tab.visible = true
	_open = true
	show()
	_refresh_all()
	_tabs.current_tab = _tabs.get_tab_count() - 1
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	AudioManager.play_sfx("ui")


func close_menu() -> void:
	if not _open:
		return
	_open = false
	hide()
	closed.emit()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	AudioManager.play_sfx("ui")


func is_open() -> bool:
	return _open


func _refresh_all() -> void:
	_gold.text = "Gold: %d" % GameManager.gold
	_refresh_items()
	_refresh_equipment()
	_refresh_party()
	_refresh_key_items()
	if _shop_vendor != "":
		_refresh_shop()


func _refresh_items() -> void:
	_items_list.clear()
	_selected_item = ""
	for item_id in GameManager.inventory:
		var qty: int = int(GameManager.inventory[item_id])
		if qty <= 0:
			continue
		var def: Dictionary = GameManager.items.get(str(item_id), {})
		var name := LocalizationManager.tr_text(def.get("display_name", item_id))
		_items_list.add_item("%s x%d" % [name, qty])
		_items_list.set_item_metadata(_items_list.item_count - 1, str(item_id))
	_item_detail.text = "Select an item."


func _on_item_selected(index: int) -> void:
	_selected_item = str(_items_list.get_item_metadata(index))
	var def: Dictionary = GameManager.items.get(_selected_item, {})
	var name := LocalizationManager.tr_text(def.get("display_name", _selected_item))
	var desc := LocalizationManager.tr_text(def.get("description", ""))
	_item_detail.text = "[b]%s[/b]\n%s\nType: %s" % [name, desc, def.get("type", "?")]


func _refresh_equipment() -> void:
	_equip_char.clear()
	for i in range(GameManager.party_field.size()):
		var cid := str(GameManager.party_field[i])
		var def: Dictionary = GameManager.characters.get(cid, {})
		_equip_char.add_item(str(def.get("display_name", cid)))
		_equip_char.set_item_metadata(i, cid)
	_equip_slots.clear()
	if _equip_char.item_count == 0:
		return
	var char_id := str(_equip_char.get_item_metadata(_equip_char.selected))
	var eq: Dictionary = GameManager.party_state.get(char_id, {}).get("equipment", {})
	for slot in ["weapon", "armor", "charm"]:
		var item_id = eq.get(slot)
		var label := "%s: (empty)" % slot.capitalize()
		if item_id:
			var def: Dictionary = GameManager.items.get(str(item_id), {})
			label = "%s: %s" % [slot.capitalize(), LocalizationManager.tr_text(def.get("display_name", item_id))]
		_equip_slots.add_item(label)
		_equip_slots.set_item_metadata(_equip_slots.item_count - 1, slot)


func _refresh_party() -> void:
	_party_list.clear()
	for cid in GameManager.party_field:
		var def: Dictionary = GameManager.characters.get(str(cid), {})
		var ps: Dictionary = GameManager.party_state.get(str(cid), {})
		var stats := GameManager.get_character_stats(str(cid))
		_party_list.add_item("%s  Lv.%d" % [def.get("display_name", cid), int(ps.get("level", 1))])
		_party_list.set_item_metadata(_party_list.item_count - 1, str(cid))
	_party_detail.text = "Select a party member."


func _refresh_key_items() -> void:
	_key_list.clear()
	for kid in GameManager.key_items:
		var def: Dictionary = GameManager.items.get(str(kid), {})
		var name := LocalizationManager.tr_text(def.get("display_name", kid))
		_key_list.add_item(name)
		_key_list.set_item_metadata(_key_list.item_count - 1, str(kid))


func _refresh_shop() -> void:
	_shop_list.clear()
	ShopManager.ensure_stock(_shop_vendor)
	var vendor: Dictionary = ShopManager.get_vendor(_shop_vendor)
	_gold.text = "Gold: %d  |  %s" % [
		GameManager.gold,
		LocalizationManager.tr_text(vendor.get("display_name", "Shop")),
	]
	for row in ShopManager.get_listings(_shop_vendor):
		var label := ""
		if row.kind == "scroll":
			var sk: Dictionary = GameManager.skills.get(str(row.item_id), {})
			label = "Scroll: %s — %d G" % [sk.get("display_name", row.item_id), int(row.price)]
		else:
			var def: Dictionary = GameManager.items.get(str(row.item_id), {})
			label = "%s — %d G" % [LocalizationManager.tr_text(def.get("display_name", row.item_id)), int(row.price)]
		if int(row.stock) > 0:
			label += " (x%d)" % int(row.stock)
		_shop_list.add_item(label)
		_shop_list.set_item_metadata(_shop_list.item_count - 1, row)
	_shop_detail.text = "Select an item to buy."


func _on_shop_item_selected(index: int) -> void:
	var row: Dictionary = _shop_list.get_item_metadata(index)
	var detail := ""
	if row.kind == "scroll":
		var sk: Dictionary = GameManager.skills.get(str(row.item_id), {})
		detail = "Teaches %s to %s." % [sk.get("display_name", row.item_id), row.get("character_id", "")]
	else:
		var def: Dictionary = GameManager.items.get(str(row.item_id), {})
		detail = LocalizationManager.tr_text(def.get("description", ""))
	_shop_detail.text = "%s\nPrice: %d G" % [detail, int(row.price)]


func _on_buy_pressed() -> void:
	if _shop_vendor == "" or _shop_list.get_selected_items().is_empty():
		return
	var row: Dictionary = _shop_list.get_item_metadata(_shop_list.get_selected_items()[0])
	if ShopManager.buy(_shop_vendor, row):
		var hud = get_tree().root.get_node_or_null("FieldHUD")
		if hud and hud.has_method("toast"):
			hud.toast("Purchased!")
		_refresh_all()
	else:
		var hud = get_tree().root.get_node_or_null("FieldHUD")
		if hud and hud.has_method("toast"):
			hud.toast("Cannot buy that item.")


func _on_equip_pressed() -> void:
	if _items_list.get_selected_items().is_empty() or _equip_char.item_count == 0:
		return
	var item_id := str(_items_list.get_item_metadata(_items_list.get_selected_items()[0]))
	var char_id := str(_equip_char.get_item_metadata(_equip_char.selected))
	if GameManager.equip_item(char_id, item_id):
		_refresh_all()
		var hud = get_tree().root.get_node_or_null("FieldHUD")
		if hud and hud.has_method("toast"):
			hud.toast("Equipped %s." % item_id)


func _on_use_pressed() -> void:
	if _items_list.get_selected_items().is_empty():
		return
	var item_id := str(_items_list.get_item_metadata(_items_list.get_selected_items()[0]))
	if GameManager.use_item_field(str(GameManager.party_field[0]), item_id):
		_refresh_all()


func _on_party_selected(index: int) -> void:
	var cid := str(_party_list.get_item_metadata(index))
	var def: Dictionary = GameManager.characters.get(cid, {})
	var ps: Dictionary = GameManager.party_state.get(cid, {})
	var stats := GameManager.get_character_stats(cid)
	_party_detail.text = (
		"[b]%s[/b]  Level %d  XP %d\n"
		+ "HP %d/%d  MP %d/%d\n"
		+ "ATK %d  DEF %d  MAG %d  RES %d  SPD %d"
	) % [
		def.get("display_name", cid), int(ps.level), int(ps.xp),
		int(ps.hp), stats.max_hp, int(ps.mp), stats.max_mp,
		stats.atk, stats.def, stats.mag, stats.res, stats.spd,
	]


func _unhandled_input(event: InputEvent) -> void:
	if not _open:
		return
	if event.is_action_pressed("ui_cancel") or event.is_action_pressed("tab_menu"):
		close_menu()
		get_viewport().set_input_as_handled()
