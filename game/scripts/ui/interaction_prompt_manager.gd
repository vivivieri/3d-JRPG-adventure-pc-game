extends Node
## Tracks the player's focused interactable and drives the prompt HUD.


const PROMPT_SCENE := preload("res://scenes/ui/interaction_prompt_hud.tscn")

var _hud: CanvasLayer
var _last_prompt := ""
var _focused: Node


func _ready() -> void:
	_hud = PROMPT_SCENE.instantiate()
	get_tree().root.add_child(_hud)
	EventBus.locale_changed.connect(_on_locale_changed)


func _physics_process(_delta: float) -> void:
	if _hud == null:
		return
	if GameManager.state != GameManager.GameState.EXPLORATION:
		_clear_focus()
		return
	var player: CharacterBody3D = get_tree().get_first_node_in_group("player") as CharacterBody3D
	if player == null or not player.has_method("get_focused_interactable"):
		_clear_focus()
		return
	var target: Node = player.get_focused_interactable()
	if target == null or not target.has_method("get_prompt"):
		_clear_focus()
		return
	var prompt: String = target.get_prompt()
	if prompt.is_empty():
		_clear_focus()
		return
	_focused = target
	if prompt != _last_prompt or not _hud.is_showing():
		_last_prompt = prompt
		_hud.show_prompt(prompt)


func _clear_focus() -> void:
	_focused = null
	if _last_prompt.is_empty():
		return
	_last_prompt = ""
	_hud.hide_prompt()


func _on_locale_changed(_locale_code: String) -> void:
	if _focused == null or not is_instance_valid(_focused):
		return
	if not _focused.has_method("get_prompt"):
		return
	var prompt: String = _focused.get_prompt()
	_last_prompt = prompt
	if _hud.is_showing():
		_hud.show_prompt(prompt)
