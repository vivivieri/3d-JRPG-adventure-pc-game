extends StaticBody3D
## One-shot loot chest; can require the water puzzle to be solved first.


@export var item_id: String = ""
@export var quantity: int = 1
@export var opened_flag: String = ""
@export var requires_water_lowered: bool = false
@export var interaction_prompt_key: String = "UI_INTERACT_OPEN"


func _ready() -> void:
	if not opened_flag.is_empty() and GameManager.has_flag(opened_flag):
		_hide_chest()


func interact() -> void:
	if requires_water_lowered and not GameManager.has_flag("water_lowered"):
		return
	if not opened_flag.is_empty() and GameManager.has_flag(opened_flag):
		return
	if not item_id.is_empty():
		GameManager.add_item(item_id, quantity)
	if not opened_flag.is_empty():
		GameManager.set_flag(opened_flag)
	_hide_chest()


func get_prompt() -> String:
	if not opened_flag.is_empty() and GameManager.has_flag(opened_flag):
		return ""
	return LocalizationManager.tr_key(interaction_prompt_key)


func _hide_chest() -> void:
	visible = false
	set_collision_layer_value(1, false)
	set_collision_mask_value(1, false)
