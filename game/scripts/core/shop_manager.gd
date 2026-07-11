extends Node
## Shop purchases, stock tracking, and vendor data.

var vendors: Dictionary = {}
var stock: Dictionary = {}


func _ready() -> void:
	_load_vendors()


func _load_vendors() -> void:
	var path := "res://data/shop/roku_shop.json"
	var data: Variant = GameManager.load_json(path)
	if data is Dictionary and data.has("vendor_id"):
		vendors[str(data.vendor_id)] = data


func reset_for_new_game() -> void:
	stock.clear()
	for vendor_id in vendors:
		_init_stock(str(vendor_id))


func _init_stock(vendor_id: String) -> void:
	var vendor: Dictionary = vendors.get(vendor_id, {})
	if vendor.is_empty():
		return
	stock[vendor_id] = {}
	for entry in vendor.get("inventory", []):
		stock[vendor_id][str(entry.item_id)] = int(entry.get("stock", -1))


func ensure_stock(vendor_id: String) -> void:
	if not stock.has(vendor_id):
		_init_stock(vendor_id)
	var vendor: Dictionary = vendors.get(vendor_id, {})
	if vendor.is_empty():
		return
	var restock_flag := str(vendor.get("restock_on_flag", ""))
	if restock_flag != "" and GameManager.has_flag(restock_flag):
		for entry in vendor.get("inventory", []):
			var item_id := str(entry.item_id)
			if int(entry.get("stock", -1)) == 1:
				stock[vendor_id][item_id] = 1


func get_vendor(vendor_id: String) -> Dictionary:
	return vendors.get(vendor_id, {})


func get_listings(vendor_id: String) -> Array:
	ensure_stock(vendor_id)
	var vendor: Dictionary = vendors.get(vendor_id, {})
	var rows: Array = []
	for entry in vendor.get("inventory", []):
		var item_id := str(entry.item_id)
		var left: int = int(stock.get(vendor_id, {}).get(item_id, int(entry.get("stock", -1))))
		if left == 0:
			continue
		rows.append({
			"item_id": item_id,
			"price": int(entry.get("price", 0)),
			"stock": left,
			"kind": "item",
		})
	for entry in vendor.get("scrolls", []):
		var skill_id := str(entry.skill_id)
		var key := "scroll_%s" % skill_id
		var left: int = int(stock.get(vendor_id, {}).get(key, int(entry.get("stock", 1))))
		if left == 0:
			continue
		rows.append({
			"item_id": skill_id,
			"price": int(entry.get("price", 0)),
			"stock": left,
			"kind": "scroll",
			"character_id": str(entry.get("character_id", "")),
		})
	return rows


func buy(vendor_id: String, listing: Dictionary) -> bool:
	ensure_stock(vendor_id)
	var price: int = int(listing.get("price", 0))
	if GameManager.gold < price:
		return false
	var kind := str(listing.get("kind", "item"))
	if kind == "scroll":
		return _buy_scroll(vendor_id, listing, price)
	return _buy_item(vendor_id, listing, price)


func _buy_item(vendor_id: String, listing: Dictionary, price: int) -> bool:
	var item_id := str(listing.item_id)
	var left: int = int(stock.get(vendor_id, {}).get(item_id, -1))
	if left == 0:
		return false
	GameManager.gold -= price
	GameManager.add_item(item_id, 1)
	if left > 0:
		stock[vendor_id][item_id] = left - 1
	EventBus.gold_changed.emit(GameManager.gold)
	AudioManager.play_sfx("ui")
	return true


func _buy_scroll(vendor_id: String, listing: Dictionary, price: int) -> bool:
	var skill_id := str(listing.item_id)
	var char_id := str(listing.get("character_id", ""))
	if char_id == "" or not GameManager.party_state.has(char_id):
		return false
	var key := "scroll_%s" % skill_id
	var left: int = int(stock.get(vendor_id, {}).get(key, 1))
	if left == 0:
		return false
	var skills: Array = GameManager.party_state[char_id].skills
	if skill_id in skills:
		return false
	GameManager.gold -= price
	skills.append(skill_id)
	if left > 0:
		stock[vendor_id][key] = left - 1
	EventBus.gold_changed.emit(GameManager.gold)
	AudioManager.play_sfx("ui")
	return true


func get_save_dict() -> Dictionary:
	return stock.duplicate(true)


func load_save_dict(data: Dictionary) -> void:
	stock = data.duplicate(true)
