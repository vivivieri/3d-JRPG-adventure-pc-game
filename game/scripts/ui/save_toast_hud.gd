extends CanvasLayer


@onready var _label: Label = $Panel/Label


func _ready() -> void:
	layer = 9
	visible = false
	EventBus.save_message.connect(_show_message)


func _show_message(text: String) -> void:
	_label.text = text
	visible = true
	$Panel.modulate.a = 1.0
	var tween := create_tween()
	tween.tween_interval(1.8)
	tween.tween_property($Panel, "modulate:a", 0.0, 0.4)
	tween.tween_callback(func(): visible = false)
