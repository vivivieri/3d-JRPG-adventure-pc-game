extends Node


const HUD_SCENE := preload("res://scenes/ui/quest_tracker_hud.tscn")


func _ready() -> void:
	get_tree().root.call_deferred("add_child", HUD_SCENE.instantiate())
