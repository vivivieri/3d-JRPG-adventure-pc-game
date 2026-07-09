extends Control
## Main menu — New Game / Continue / Quit.


func _ready() -> void:
	$VBox/Continue.disabled = not SaveSystem.has_save()


func _on_new_game_pressed() -> void:
	GameManager.story_flags.clear()
	GameManager.party_ids = ["urashima"]
	GameManager.party_levels = { "urashima": 1 }
	GameManager.inventory.clear()
	GameManager.gold = 0
	GameManager.current_area = "ruined_village"
	get_tree().change_scene_to_file("res://scenes/world/ruined_village.tscn")


func _on_continue_pressed() -> void:
	if SaveSystem.load_game():
		get_tree().change_scene_to_file("res://scenes/world/ruined_village.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
