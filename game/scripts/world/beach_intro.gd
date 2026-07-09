extends Node3D
## Beach opening — plays SC-01, then sends the player into the village.


@export var zone_id: String = "beach_shore"
@export var default_spawn := "default"
@export var village_scene := "res://scenes/world/ruined_village.tscn"
@export var village_spawn := "from_shore"


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
	AudioManager.play_bgm("ruined_village")
	if OS.has_environment("SCREENSHOT_MODE"):
		return
	await get_tree().process_frame
	if not GameManager.has_flag("game_started"):
		EventBus.dialogue_finished.connect(_on_intro_finished, CONNECT_ONE_SHOT)
		DialogueRunner.play_scene("SC-01")
	else:
		_go_to_village()


func _on_intro_finished(scene_id: String) -> void:
	if scene_id == "SC-01":
		_go_to_village()


func _go_to_village() -> void:
	GameManager.entry_spawn = village_spawn
	get_tree().change_scene_to_file(village_scene)
