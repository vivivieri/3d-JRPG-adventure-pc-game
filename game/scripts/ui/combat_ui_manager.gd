extends Node
## Instantiates the combat UI overlay on the root viewport.


const COMBAT_UI_SCENE := preload("res://scenes/ui/combat_ui.tscn")


func _ready() -> void:
	var ui := COMBAT_UI_SCENE.instantiate()
	get_tree().root.add_child(ui)
