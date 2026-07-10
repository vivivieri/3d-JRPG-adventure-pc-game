extends Node


const TOAST_SCENE := preload("res://scenes/ui/save_toast_hud.tscn")


func _ready() -> void:
	get_tree().root.add_child(TOAST_SCENE.instantiate())
