extends Node3D
## World scene root helper — spawn placement + zone art pass.

@export var zone_id: String = "ruined_village"
@export var default_spawn := "default"


func _ready() -> void:
	var player := get_tree().get_first_node_in_group("player") as Node3D
	if player:
		var spawn_id := GameManager.entry_spawn if not GameManager.entry_spawn.is_empty() else default_spawn
		GameManager.entry_spawn = ""
		var marker := get_node_or_null("Spawns/%s" % spawn_id) as Node3D
		if marker:
			player.global_position = marker.global_position
			player.global_rotation = marker.global_rotation
	GameManager.current_area = zone_id
	ZoneVisuals.apply_to_scene(self, zone_id)
	AudioManager.play_bgm(zone_id if zone_id != "main_menu" else "main_menu")
