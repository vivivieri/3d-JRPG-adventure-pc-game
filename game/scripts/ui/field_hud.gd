extends CanvasLayer
## Field HUD — interact prompt, quest tracker, puzzle/ending overlays.

@onready var _prompt: Label = %InteractPrompt
@onready var _quest: Label = %QuestTracker
@onready var _zone: Label = %ZoneLabel
@onready var _toast: Label = %Toast
@onready var _overlay: Control = %Overlay
@onready var _overlay_title: Label = %OverlayTitle
@onready var _overlay_body: RichTextLabel = %OverlayBody
@onready var _overlay_actions: HBoxContainer = %OverlayActions

var _puzzle_callback: Callable = Callable()
var _water_level := 1


func _ready() -> void:
	_overlay.hide()
	_toast.hide()
	EventBus.quest_updated.connect(func(_q): refresh_quest())
	EventBus.zone_changed.connect(_on_zone)
	call_deferred("refresh_quest")


func _on_zone(zone_id: String) -> void:
	_zone.text = zone_id.replace("_", " ").capitalize()
	refresh_quest()


func set_prompt(text: String) -> void:
	if text == "":
		_prompt.hide()
	else:
		_prompt.show()
		_prompt.text = "[E] %s" % text


func toast(msg: String) -> void:
	_toast.text = msg
	_toast.show()
	var tween := create_tween()
	tween.tween_interval(2.0)
	tween.tween_callback(func(): _toast.hide())


func refresh_quest() -> void:
	var lines: PackedStringArray = []
	for qid in GameManager.active_quests:
		var stage: Dictionary = GameManager.get_active_quest_stage(qid)
		if stage.is_empty():
			continue
		var quest: Dictionary = GameManager.quests.get(qid, {})
		var title := LocalizationManager.tr_text(quest.get("title", ""))
		var desc := LocalizationManager.tr_text(stage.get("description", ""))
		lines.append("%s — %s" % [title, desc])
	_quest.text = "\n".join(lines) if lines.size() > 0 else ""


func show_lore_popup(entry: Dictionary, on_close: Callable) -> void:
	_overlay.show()
	_overlay_title.text = LocalizationManager.tr_text(entry.get("title", ""))
	_overlay_body.text = LocalizationManager.tr_text(entry.get("body", ""))
	for c in _overlay_actions.get_children():
		c.queue_free()
	var btn := Button.new()
	btn.text = "Close"
	btn.pressed.connect(func():
		_overlay.hide()
		if on_close.is_valid():
			on_close.call()
	)
	_overlay_actions.add_child(btn)


func open_water_puzzle(on_solved: Callable) -> void:
	_puzzle_callback = on_solved
	_water_level = 1
	_overlay.show()
	_overlay_title.text = "Tidal Lock"
	_overlay_body.text = "Raise or lower the water to reach the submerged latch.\nCurrent level: %d / 3" % _water_level
	for c in _overlay_actions.get_children():
		c.queue_free()
	var lower := Button.new()
	lower.text = "Lower"
	lower.pressed.connect(_puzzle_lower)
	_overlay_actions.add_child(lower)
	var raise := Button.new()
	raise.text = "Raise"
	raise.pressed.connect(_puzzle_raise)
	_overlay_actions.add_child(raise)
	var attempt := Button.new()
	attempt.text = "Try latch"
	attempt.pressed.connect(_puzzle_try)
	_overlay_actions.add_child(attempt)


func _puzzle_lower() -> void:
	_water_level = max(0, _water_level - 1)
	_overlay_body.text = "Raise or lower the water to reach the submerged latch.\nCurrent level: %d / 3" % _water_level


func _puzzle_raise() -> void:
	_water_level = min(3, _water_level + 1)
	_overlay_body.text = "Raise or lower the water to reach the submerged latch.\nCurrent level: %d / 3" % _water_level


func _puzzle_try() -> void:
	if _water_level == 2:
		_overlay.hide()
		toast("The latch opens. A blade washes free.")
		if _puzzle_callback.is_valid():
			_puzzle_callback.call()
	else:
		toast("The latch is out of reach.")


func open_ending_choice() -> void:
	DialogueRunner.play("SC-16")
	DialogueRunner.finished.connect(_on_ending_chosen, CONNECT_ONE_SHOT)


func _on_ending_chosen(_scene_id: String) -> void:
	var ending := str(GameManager.get_flag("ending_chosen", "rewind"))
	match ending:
		"anchor":
			GameManager.go_to_zone("ending_anchor")
		"drift":
			GameManager.go_to_zone("ending_drift")
		_:
			GameManager.go_to_zone("ending_rewind")
