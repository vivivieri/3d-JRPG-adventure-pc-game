extends Node
## Validates shop stock and purchase flow.
## godot4 --headless --path game res://tests/shop_smoke_test.tscn

func _ready() -> void:
	GameManager.reset_new_game()
	GameManager.set_flag("met_roku")
	GameManager.gold = 100
	ShopManager.ensure_stock("roku_shack")
	var listings: Array = ShopManager.get_listings("roku_shack")
	var salve_row: Dictionary = {}
	for row in listings:
		if str(row.get("item_id", "")) == "sea_salve":
			salve_row = row
			break
	var bought := false
	if not salve_row.is_empty():
		bought = ShopManager.buy("roku_shack", salve_row)
	var have_salve: int = int(GameManager.inventory.get("sea_salve", 0))
	var ok := listings.size() > 0 and bought and have_salve > 0
	print("SHOP_TEST ok=%s listings=%d bought=%s salve=%d gold=%d" % [ok, listings.size(), bought, have_salve, GameManager.gold])
	get_tree().quit(0 if ok else 1)
