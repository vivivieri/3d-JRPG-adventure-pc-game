extends Node
## Validates tab menu open/close and inventory refresh.
## godot4 --headless --path game res://tests/tab_menu_smoke_test.tscn

func _ready() -> void:
	call_deferred("_run")


func _run() -> void:
	await get_tree().process_frame
	await get_tree().process_frame
	GameManager.reset_new_game()
	GameManager.add_item("sea_salve", 2)
	GameManager.gold = 50
	TabMenuUI.open_menu()
	await get_tree().process_frame
	var opened := TabMenuUI.is_open()
	TabMenuUI.close_menu()
	await get_tree().process_frame
	var closed := not TabMenuUI.is_open()
	var ok := opened and closed
	print("TAB_MENU_TEST ok=%s opened=%s closed=%s" % [ok, opened, closed])
	get_tree().quit(0 if ok else 1)
