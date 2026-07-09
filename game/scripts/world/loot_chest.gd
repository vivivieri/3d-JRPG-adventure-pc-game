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
		return
	_spawn_visual()


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


func _spawn_visual() -> void:
	if get_node_or_null("ChestVisual"):
		return
	var visual := Node3D.new()
	visual.name = "ChestVisual"
	add_child(visual)
	PropLibrary.spawn("log_stack", visual, Vector3(0, 0, 0), 0.0, 0.9, true)
	PropLibrary.spawn("mushroom_tan", visual, Vector3(0.15, 0.55, 0.1), 20.0, 0.95, true)
	PropLibrary.spawn("rock_small_b", visual, Vector3(-0.35, 0, -0.25), -15.0, 0.8, true)
	PropLibrary.spawn("fern", visual, Vector3(0.3, 0, 0.3), 35.0, 0.85, true)


func _hide_chest() -> void:
	visible = false
	set_collision_layer_value(1, false)
	set_collision_mask_value(1, false)
