extends StaticBody3D
## Door or zone that loads another world scene when interacted with.


@export var target_scene: String = ""
@export var target_area: String = ""
@export var target_spawn: String = "default"
@export var required_flag: String = ""
@export var interaction_prompt_key: String = "UI_INTERACT_ENTER"
@export var blocked_prompt_key: String = "UI_INTERACT_LOCKED"


func interact() -> void:
	if not _is_accessible():
		return
	if target_scene.is_empty():
		return
	GameManager.current_area = target_area
	GameManager.entry_spawn = target_spawn
	get_tree().change_scene_to_file(target_scene)


func get_prompt() -> String:
	if not _is_accessible():
		return LocalizationManager.tr_key(blocked_prompt_key)
	return LocalizationManager.tr_key(interaction_prompt_key)


func _is_accessible() -> bool:
	return required_flag.is_empty() or GameManager.has_flag(required_flag)
