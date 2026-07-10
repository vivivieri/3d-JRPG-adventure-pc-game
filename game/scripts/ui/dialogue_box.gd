extends CanvasLayer
## Bottom-screen dialogue box — speaker, typewriter text, advance hint.

const CHARS_PER_SECOND := 38.0

@onready var _panel: PanelContainer = $DialoguePanel
@onready var _speaker_label: Label = $DialoguePanel/Margin/HBox/VBox/Header/SpeakerLabel
@onready var _body_label: Label = $DialoguePanel/Margin/HBox/VBox/BodyLabel
@onready var _hint_label: Label = $DialoguePanel/Margin/HBox/VBox/HintLabel
@onready var _portrait_frame: PanelContainer = $DialoguePanel/Margin/HBox/PortraitFrame
@onready var _portrait_placeholder: ColorRect = $DialoguePanel/Margin/HBox/PortraitFrame/PortraitPlaceholder

var _full_text := ""
var _visible_chars := 0
var _typing := false
var _type_timer := 0.0
var _current_line: Dictionary = {}


func _ready() -> void:
	layer = 10
	_panel.visible = false
	EventBus.dialogue_started.connect(_on_dialogue_started)
	EventBus.dialogue_line.connect(_on_dialogue_line)
	EventBus.dialogue_finished.connect(_on_dialogue_finished)
	EventBus.locale_changed.connect(_on_locale_changed)
	_apply_fonts()
	_refresh_hint()


func _process(delta: float) -> void:
	if not _typing:
		return
	_type_timer += delta
	var target := int(_type_timer * CHARS_PER_SECOND)
	if target >= _full_text.length():
		_finish_typing()
	else:
		_visible_chars = target
		_body_label.text = _full_text.substr(0, _visible_chars)


func _unhandled_input(event: InputEvent) -> void:
	if not _panel.visible:
		return
	if event.is_action_pressed("confirm") or event.is_action_pressed("interact"):
		_on_advance_pressed()
		get_viewport().set_input_as_handled()


func _on_dialogue_started(_scene_id: String) -> void:
	_panel.visible = true
	_current_line = {}
	_clear_line()


func _on_dialogue_line(line: Dictionary) -> void:
	_current_line = line
	_show_line(line)


func _on_dialogue_finished(_scene_id: String) -> void:
	_panel.visible = false
	_typing = false
	_current_line = {}
	_clear_line()


func _on_locale_changed(_locale_code: String) -> void:
	_apply_fonts()
	_refresh_hint()
	if not _current_line.is_empty():
		_show_line(_current_line)


func _on_advance_pressed() -> void:
	if _typing:
		_finish_typing()
		return
	DialogueRunner.advance()


func _show_line(line: Dictionary) -> void:
	var speaker: String = line.get("speaker", "")
	var speaker_display: String = line.get("speaker_name", "")
	if speaker == "narrator":
		_speaker_label.visible = false
	else:
		_speaker_label.visible = true
		_speaker_label.text = speaker_display if not speaker_display.is_empty() else speaker
	var portrait: String = line.get("portrait", "")
	_portrait_frame.visible = not portrait.is_empty()
	_full_text = line.get("text_resolved", LocalizationManager.resolve_text(line.get("text", "")))
	_visible_chars = 0
	_type_timer = 0.0
	_typing = _full_text.length() > 0
	_body_label.text = "" if _typing else _full_text
	if not _typing:
		_refresh_hint()


func _finish_typing() -> void:
	_typing = false
	_visible_chars = _full_text.length()
	_body_label.text = _full_text
	_refresh_hint()


func _clear_line() -> void:
	_speaker_label.text = ""
	_body_label.text = ""
	_typing = false
	_full_text = ""
	_visible_chars = 0
	_portrait_frame.visible = false


func _refresh_hint() -> void:
	_hint_label.text = LocalizationManager.tr_key("UI_DIALOGUE_ADVANCE")


func _apply_fonts() -> void:
	FontThemeManager.apply_dialogue_speaker(_speaker_label)
	FontThemeManager.apply_dialogue_body(_body_label)
	FontThemeManager.apply_dialogue_hint(_hint_label)
