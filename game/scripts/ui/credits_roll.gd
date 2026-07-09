extends Control
## Scrolling credits roll — used after endings and from main menu.


signal finished

@export var auto_start := true
@export var scroll_speed := 42.0

@onready var _scroll: ScrollContainer = $Scroll
@onready var _content: VBoxContainer = $Scroll/Content
@onready var _skip_btn: Button = $SkipBtn


func _ready() -> void:
	visible = false
	_skip_btn.pressed.connect(_finish)
	_build_lines()
	EventBus.locale_changed.connect(func(_l): _build_lines())
	if auto_start:
		call_deferred("play")


func play() -> void:
	visible = true
	_scroll.scroll_vertical = 0
	set_process(true)


func _process(delta: float) -> void:
	if not visible:
		return
	_scroll.scroll_vertical += int(scroll_speed * delta)
	if _scroll.scroll_vertical >= _scroll.get_v_scroll_bar().max_value:
		_finish()


func _build_lines() -> void:
	for child in _content.get_children():
		child.queue_free()
	_add_line(LocalizationManager.tr_key("credits.title"), 34, Color(0.95, 0.82, 0.55))
	_add_spacer(24)
	for key in [
		"credits.story",
		"credits.game_design",
		"credits.programming",
		"credits.audio",
		"credits.art",
		"credits.models3d",
		"credits.localization",
		"credits.fonts",
		"credits.engine",
		"credits.godotsteam",
	]:
		_add_line(LocalizationManager.tr_key(key), 20, Color(0.88, 0.9, 0.96))
	_add_spacer(32)
	_add_line(LocalizationManager.tr_key("credits.thanks"), 18, Color(0.7, 0.75, 0.82))
	_add_spacer(800)
	_skip_btn.text = LocalizationManager.tr_key("UI_CREDITS_SKIP")


func _add_line(text: String, size: int, color: Color) -> void:
	var lbl := Label.new()
	lbl.text = text
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", color)
	_content.add_child(lbl)


func _add_spacer(height: int) -> void:
	var spacer := Control.new()
	spacer.custom_minimum_size.y = height
	_content.add_child(spacer)


func _finish() -> void:
	visible = false
	set_process(false)
	finished.emit()
