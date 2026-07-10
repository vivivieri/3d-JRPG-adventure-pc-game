extends Control
## Dev launcher — pick a greybox zone (Phase 1).


func _go(scene_path: String) -> void:
	get_tree().change_scene_to_file(scene_path)


func _on_beach() -> void:
	_go("res://scenes/world/beach_shore.tscn")


func _on_village() -> void:
	_go("res://scenes/world/ruined_village.tscn")


func _on_caves() -> void:
	_go("res://scenes/world/tidal_caves.tscn")


func _on_palace() -> void:
	_go("res://scenes/world/dragon_palace_gate.tscn")
