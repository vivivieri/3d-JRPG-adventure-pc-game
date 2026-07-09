extends StaticBody3D
## World interactable — attach to NPCs, inspect points, doors.


@export var dialogue_scene_id: String = ""
@export var interaction_prompt_key: String = "UI_INTERACT_EXAMINE"
@export var sets_flag_on_interact: String = ""
@export var combat_encounter_ids: PackedStringArray = []


func interact() -> void:
	if not dialogue_scene_id.is_empty():
		DialogueRunner.play_scene(dialogue_scene_id)
	elif combat_encounter_ids.size() > 0:
		var ids: Array = []
		for id in combat_encounter_ids:
			ids.append(id)
		GameManager.start_combat(ids)
	if not sets_flag_on_interact.is_empty():
		GameManager.set_flag(sets_flag_on_interact)


func get_prompt() -> String:
	return LocalizationManager.tr_key(interaction_prompt_key)
