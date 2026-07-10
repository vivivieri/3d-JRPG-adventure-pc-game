extends Control
## Credits roll after endings.


func _ready() -> void:
	%Body.text = """Tides of Urashima

Design & Story — vivivieri
Engine — Godot 4.3

Thank you for playing.

Press any key to return to title."""


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		get_tree().change_scene_to_file("res://scenes/ui/main_menu.tscn")
