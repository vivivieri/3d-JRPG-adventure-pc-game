extends StaticBody3D
## One-shot combat encounter with optional dialogue chains and victory rewards.


@export var combat_encounter_ids: PackedStringArray = []
@export var pre_dialogue_id: String = ""
@export var pre_dialogue_flag: String = ""
@export var once_flag: String = ""
@export var victory_flag: String = ""
@export var post_victory_dialogue: String = ""
@export var load_ending_on_victory: bool = false
@export var interaction_prompt_key: String = "UI_INTERACT_FIGHT"

var _defeated := false
var _awaiting_victory := false
var _pending_combat := false


func _ready() -> void:
	if not once_flag.is_empty() and GameManager.has_flag(once_flag):
		_hide_trigger()
		return
	EventBus.dialogue_finished.connect(_on_dialogue_finished)
	EventBus.combat_ended.connect(_on_combat_ended)


func interact() -> void:
	if _defeated:
		return
	if not pre_dialogue_id.is_empty() and not GameManager.has_flag(pre_dialogue_flag):
		_pending_combat = true
		DialogueRunner.play_scene(pre_dialogue_id)
		return
	_start_fight()


func get_prompt() -> String:
	if _defeated:
		return ""
	return LocalizationManager.tr_key(interaction_prompt_key)


func _on_dialogue_finished(_scene_id: String) -> void:
	if not _pending_combat or _defeated:
		return
	_pending_combat = false
	_start_fight()


func _start_fight() -> void:
	if combat_encounter_ids.is_empty():
		return
	var ids: Array = []
	for enemy_id in combat_encounter_ids:
		ids.append(enemy_id)
	_awaiting_victory = true
	GameManager.start_combat(ids)


func _on_combat_ended(victory: bool) -> void:
	if not _awaiting_victory:
		return
	_awaiting_victory = false
	if not victory:
		return
	_defeated = true
	if not victory_flag.is_empty():
		GameManager.set_flag(victory_flag)
	if not once_flag.is_empty():
		GameManager.set_flag(once_flag)
	_hide_trigger()
	if load_ending_on_victory and not GameManager.chosen_ending.is_empty():
		await get_tree().create_timer(1.6).timeout
		GameManager.play_ending(GameManager.chosen_ending)
		return
	if not post_victory_dialogue.is_empty():
		await get_tree().process_frame
		DialogueRunner.play_scene(post_victory_dialogue)


func _hide_trigger() -> void:
	visible = false
	set_collision_layer_value(1, false)
	set_collision_mask_value(1, false)
