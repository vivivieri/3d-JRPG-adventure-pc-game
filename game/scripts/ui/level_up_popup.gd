extends CanvasLayer
## Level-up celebration overlay shown after combat XP grants.

const SKILL_NAMES := {}

@onready var _panel: PanelContainer = %Panel
@onready var _title: Label = %Title
@onready var _body: RichTextLabel = %Body
@onready var _hint: Label = %Hint

var _queue: Array = []
var _showing := false


func _ready() -> void:
	hide()


func show_level_ups(level_ups: Array) -> void:
	if level_ups.is_empty():
		return
	_queue.append_array(level_ups)
	if not _showing:
		_show_next()


func _show_next() -> void:
	if _queue.is_empty():
		_showing = false
		hide()
		return
	_showing = true
	var data: Dictionary = _queue.pop_front()
	_title.text = "Level Up!"
	var lines: PackedStringArray = []
	lines.append("[b]%s[/b] reached [b]Level %d[/b]!" % [data.get("display_name", "?"), int(data.get("level", 1))])
	var skills: Array = data.get("new_skills", [])
	if skills.size() > 0:
		lines.append("")
		lines.append("New skills:")
		for sid in skills:
			var sk: Dictionary = GameManager.skills.get(str(sid), {})
			lines.append("  • %s" % sk.get("display_name", sid))
	_body.text = "\n".join(lines)
	_hint.text = "Space / Click to continue"
	show()


func _unhandled_input(event: InputEvent) -> void:
	if not visible:
		return
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.pressed):
		_show_next()
		get_viewport().set_input_as_handled()
