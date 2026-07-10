extends Node3D
## Zone entry hooks — attach to world scene roots (editor-friendly, no procedural overlay).


@export var zone_id: String = ""
@export var arrival_dialogue_id: String = ""
@export var arrival_once_flag: String = ""


func _ready() -> void:
	if arrival_dialogue_id.is_empty():
		return
	if not arrival_once_flag.is_empty() and GameManager.has_flag(arrival_once_flag):
		return
	DialogueRunner.play_scene(arrival_dialogue_id)
	if not arrival_once_flag.is_empty():
		GameManager.set_flag(arrival_once_flag)
