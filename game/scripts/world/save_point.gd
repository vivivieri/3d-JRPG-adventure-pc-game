extends StaticBody3D
## Save point interactable — optional first-time examine dialogue, then persists state.


@export var interaction_prompt_key: String = "UI_INTERACT_SAVE"
@export var examine_dialogue_id: String = ""
@export var examine_once_flag: String = ""
@export var examine_prompt_key: String = "UI_INTERACT_EXAMINE"


func interact() -> void:
	if _should_examine():
		AudioManager.play_sfx("interact")
		DialogueRunner.play_scene(examine_dialogue_id)
		if not examine_once_flag.is_empty():
			GameManager.set_flag(examine_once_flag)
		return
	if SaveSystem.save_game():
		AudioManager.play_sfx("ui_confirm")
		EventBus.save_message.emit(LocalizationManager.tr_key("UI_SAVE_SUCCESS"))
	else:
		EventBus.save_message.emit(LocalizationManager.tr_key("UI_SAVE_FAILED"))


func get_prompt() -> String:
	if _should_examine():
		return LocalizationManager.tr_key(examine_prompt_key)
	return LocalizationManager.tr_key(interaction_prompt_key)


func _should_examine() -> bool:
	return (
		not examine_dialogue_id.is_empty()
		and (examine_once_flag.is_empty() or not GameManager.has_flag(examine_once_flag))
	)
