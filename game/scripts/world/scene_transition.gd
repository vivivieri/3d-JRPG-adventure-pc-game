extends StaticBody3D
## Door / zone exit — loads another world scene when the player interacts.

@export_file("*.tscn") var target_scene: String = ""
@export var target_area: String = ""
@export var target_spawn: String = "default"
@export var interaction_prompt_key: String = "UI_INTERACT_ENTER"


func interact() -> void:
	if target_scene.is_empty():
		push_warning("SceneTransition missing target_scene on %s" % name)
		return
	if not target_area.is_empty():
		GameManager.current_area = target_area
	get_tree().change_scene_to_file(target_scene)


func get_prompt() -> String:
	return LocalizationManager.tr_key(interaction_prompt_key)
