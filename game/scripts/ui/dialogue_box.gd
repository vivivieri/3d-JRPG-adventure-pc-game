extends CanvasLayer
## Lower-third dialogue box with typewriter text and choices.

@onready var _panel: PanelContainer = %Panel
@onready var _portrait: TextureRect = %Portrait
@onready var _speaker: Label = %Speaker
@onready var _text: RichTextLabel = %Text
@onready var _choices: VBoxContainer = %Choices
@onready var _continue_hint: Label = %ContinueHint

var _lines: Array = []
var _line_idx := 0
var _typing := false
var _full_text := ""
var _char_idx := 0
var _cps := 40.0
var _scene_data: Dictionary = {}
var _done_callback: Callable = Callable()


func _ready() -> void:
	hide()


func start(scene_data: Dictionary, done_callback: Callable) -> void:
	if SettingsManager:
		_cps = SettingsManager.text_speed_cps
	_scene_data = scene_data
	_done_callback = done_callback
	_lines = scene_data.get("lines", [])
	_line_idx = 0
	show()
	_panel.show()
	_choices.hide()
	_continue_hint.hide()
	_show_line()


func _show_line() -> void:
	if _line_idx >= _lines.size():
		_show_choices_or_finish()
		return
	var line: Dictionary = _lines[_line_idx]
	var speaker_id := str(line.get("speaker", ""))
	_speaker.text = _format_speaker(speaker_id)
	_set_portrait(str(line.get("portrait", "")))
	_full_text = LocalizationManager.tr_text(line.get("text", ""))
	_text.text = ""
	_char_idx = 0
	_typing = true
	_continue_hint.hide()


func _format_speaker(speaker_id: String) -> String:
	match speaker_id:
		"narrator":
			return ""
		"urashima":
			return "Urashima"
		"yuzu":
			return "Yuzu"
		"roku":
			return "Roku"
		"otohime":
			return "Otohime"
		"shore_wraith":
			return "Shore Wraith"
		"tide_keeper":
			return "Tide Keeper"
		_:
			return speaker_id.capitalize()


func _set_portrait(portrait_id: String) -> void:
	if portrait_id == "":
		_portrait.texture = null
		_portrait.hide()
		return
	var path := "res://assets/ui/portraits/%s.png" % portrait_id
	if ResourceLoader.exists(path):
		_portrait.texture = load(path)
		_portrait.show()
	else:
		_portrait.texture = null
		_portrait.hide()


func _process(delta: float) -> void:
	if not _typing:
		return
	_char_idx += int(_cps * delta) + 1
	if _char_idx >= _full_text.length():
		_text.text = _full_text
		_typing = false
		_continue_hint.show()
	else:
		_text.text = _full_text.substr(0, _char_idx)


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		if _choices.visible:
			return
		if _typing:
			_text.text = _full_text
			_typing = false
			_continue_hint.show()
		else:
			_line_idx += 1
			_show_line()
		get_viewport().set_input_as_handled()


func _show_choices_or_finish() -> void:
	var choices: Array = _scene_data.get("choices", [])
	if choices.is_empty():
		_finish({})
		return
	_choices.show()
	_continue_hint.hide()
	_speaker.text = ""
	_text.text = LocalizationManager.tr_text(_scene_data.lines[-1].get("text", "")) if _scene_data.lines.size() > 0 else ""
	for child in _choices.get_children():
		child.queue_free()
	for choice in choices:
		var btn := Button.new()
		btn.text = LocalizationManager.tr_text(choice.get("text", ""))
		btn.pressed.connect(_on_choice_pressed.bind(choice))
		_choices.add_child(btn)


func _on_choice_pressed(choice: Dictionary) -> void:
	var payload := {}
	if choice.has("set_flags"):
		payload["set_flags"] = choice.set_flags
	_finish(payload)


func _finish(choice_data: Dictionary) -> void:
	hide()
	if _done_callback.is_valid():
		_done_callback.call(choice_data)
