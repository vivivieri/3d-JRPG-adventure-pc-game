extends Area3D
## Triggers a one-shot dialogue scene when the player enters the zone.


@export var dialogue_scene_id: String = ""
@export var once_flag: String = ""


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	call_deferred("_check_overlapping_player")


func _check_overlapping_player() -> void:
	for body in get_overlapping_bodies():
		_on_body_entered(body)


func _on_body_entered(body: Node3D) -> void:
	if not body.is_in_group("player"):
		return
	if dialogue_scene_id.is_empty():
		return
	if not once_flag.is_empty() and GameManager.has_flag(once_flag):
		return
	DialogueRunner.play_scene(dialogue_scene_id)
	if not once_flag.is_empty():
		GameManager.set_flag(once_flag)
