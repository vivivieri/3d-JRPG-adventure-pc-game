extends StaticBody3D
## Save point interactable — persists exploration state.


@export var interaction_prompt_key: String = "UI_INTERACT_SAVE"


func interact() -> void:
	if SaveSystem.save_game():
		AudioManager.play_sfx("ui_confirm")
		EventBus.save_message.emit(LocalizationManager.tr_key("UI_SAVE_SUCCESS"))
	else:
		EventBus.save_message.emit(LocalizationManager.tr_key("UI_SAVE_FAILED"))


func get_prompt() -> String:
	return LocalizationManager.tr_key(interaction_prompt_key)
