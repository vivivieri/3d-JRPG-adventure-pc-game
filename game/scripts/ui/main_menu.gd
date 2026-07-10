extends Control
## Title screen — New Game, Continue, Settings, Dev Zone Hub.


func _ready() -> void:
	%ContinueButton.disabled = not SaveSystem.has_save()
	%SettingsPanel.hide()
	_sync_graphics_option()


func _sync_graphics_option() -> void:
	var presets := ["low", "medium", "high"]
	if SettingsManager.graphics_quality in presets:
		%GraphicsOption.select(presets.find(SettingsManager.graphics_quality))


func _on_new_game_pressed() -> void:
	GameManager.reset_new_game()
	var ng: Dictionary = GameManager.load_json("res://data/starting/new_game.json")
	if bool(ng.get("play_prologue", true)):
		GameManager.pending_dialogue = "SC-00"
	GameManager.pending_spawn = "WorldSpawn"
	GameManager.go_to_zone("beach_shore")


func _on_continue_pressed() -> void:
	SaveSystem.load_game()


func _on_settings_pressed() -> void:
	%SettingsPanel.show()


func _on_settings_close_pressed() -> void:
	%SettingsPanel.hide()


func _on_graphics_changed(index: int) -> void:
	var presets := ["low", "medium", "high"]
	SettingsManager.set_graphics_quality(presets[index])


func _on_dev_hub_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/world/zone_hub.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
