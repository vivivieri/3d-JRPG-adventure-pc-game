extends Node
## Instantiates the field menu overlay on the root viewport.


const FIELD_MENU_SCENE := preload("res://scenes/ui/field_menu.tscn")


func _ready() -> void:
	get_tree().root.call_deferred("add_child", FIELD_MENU_SCENE.instantiate())
