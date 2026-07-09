extends StaticBody3D
## Puzzle switch that toggles a linked water controller.


@export var water_controller_path: NodePath
@export var interaction_prompt_key: String = "UI_INTERACT_USE"


func interact() -> void:
	var controller := get_node_or_null(water_controller_path)
	if controller and controller.has_method("toggle"):
		controller.toggle()


func get_prompt() -> String:
	return LocalizationManager.tr_key(interaction_prompt_key)
