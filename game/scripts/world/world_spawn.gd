extends Node3D
## Positions the player at a named spawn marker when a world scene loads.

@export var default_spawn := "default"


func _ready() -> void:
	var player := get_tree().get_first_node_in_group("player") as Node3D
	if player == null:
		return
	var spawn_id := GameManager.entry_spawn if not GameManager.entry_spawn.is_empty() else default_spawn
	GameManager.entry_spawn = ""
	var marker := get_node_or_null("Spawns/%s" % spawn_id) as Node3D
	if marker:
		player.global_position = marker.global_position
		player.global_rotation = marker.global_rotation
