extends Node
## Loads each world scene, frames the camera, and saves viewport PNG.


const CAPTURES := [
	{"file": "main_menu", "path": "res://scenes/world/main_menu.tscn"},
	{
		"file": "beach",
		"path": "res://scenes/world/beach_shore.tscn",
		"cam": Vector3(10, 6, 16),
		"focus": Vector3(0, 1.2, 7),
		"fov": 70.0,
		"wait": 8.0,
	},
	{
		"file": "village",
		"path": "res://scenes/world/ruined_village.tscn",
		"cam": Vector3(12, 8, 14),
		"focus": Vector3(0, 1.5, 0),
		"fov": 68.0,
		"wait": 8.0,
	},
	{
		"file": "village_inspects",
		"path": "res://scenes/world/ruined_village.tscn",
		"cam": Vector3(-5, 4.5, 9),
		"focus": Vector3(-0.5, 1.2, 4.5),
		"fov": 58.0,
		"wait": 0.6,
		"reuse_scene": true,
	},
	{
		"file": "caves",
		"path": "res://scenes/world/tidal_caves.tscn",
		"cam": Vector3(5, 4.5, 10),
		"focus": Vector3(0, 1.5, -8),
		"fov": 65.0,
		"wait": 8.0,
	},
	{
		"file": "caves_pool",
		"path": "res://scenes/world/tidal_caves.tscn",
		"cam": Vector3(0.5, 2.8, -12),
		"focus": Vector3(0, -0.2, -16),
		"fov": 62.0,
		"wait": 0.8,
		"reuse_scene": true,
	},
	{
		"file": "caves_water",
		"path": "res://scenes/world/tidal_caves.tscn",
		"cam": Vector3(6, 3.5, -2),
		"focus": Vector3(0, 0.2, -6),
		"fov": 60.0,
		"wait": 0.6,
		"reuse_scene": true,
		"set_flags": ["water_lowered"],
	},
	{
		"file": "caves_shrine",
		"path": "res://scenes/world/tidal_caves.tscn",
		"cam": Vector3(0, 3.5, -24),
		"focus": Vector3(0, 1.8, -28),
		"fov": 64.0,
		"wait": 0.6,
		"reuse_scene": true,
	},
	{
		"file": "palace",
		"path": "res://scenes/world/dragon_palace_gate.tscn",
		"cam": Vector3(5, 18, 36),
		"focus": Vector3(0, 4, 8),
		"fov": 74.0,
		"wait": 5.0,
	},
]

const DEFAULT_OUT := "/opt/cursor/artifacts/screenshots"

var _current_scene_path := ""


func _ready() -> void:
	var out_dir: String = OS.get_environment("SCREENSHOT_DIR") if OS.has_environment("SCREENSHOT_DIR") else DEFAULT_OUT
	DirAccess.make_dir_recursive_absolute(out_dir)
	_preload_story_flags()
	await get_tree().process_frame
	for entry in CAPTURES:
		await _capture_entry(entry, out_dir)
	print("[Screenshot] Done — saved %d images to %s" % [CAPTURES.size(), out_dir])
	get_tree().quit()


func _preload_story_flags() -> void:
	GameManager.set_flag("gate_arrival_dialogue")
	GameManager.set_flag("palace_vision_seen")
	GameManager.set_flag("caves_entrance_dialogue")
	GameManager.set_flag("village_arrival_seen")


func _capture_entry(entry: Dictionary, out_dir: String) -> void:
	if not entry.get("reuse_scene", false) or entry.path != _current_scene_path:
		get_tree().change_scene_to_file(entry.path)
		_current_scene_path = entry.path
		await get_tree().create_timer(entry.get("wait", 5.0)).timeout
	else:
		await get_tree().create_timer(entry.get("wait", 0.5)).timeout
	_apply_capture_setup(entry)
	_hide_dialogue_ui()
	_hide_player_visual()
	if entry.has("cam") and entry.has("focus"):
		_frame_camera(entry)
	await get_tree().create_timer(0.5).timeout
	await get_tree().process_frame
	await get_tree().process_frame
	var img: Image = get_viewport().get_texture().get_image()
	var path := "%s/%s.png" % [out_dir, entry.file]
	var err := img.save_png(path)
	if err != OK:
		push_error("Failed to save %s (err %s)" % [path, err])
	else:
		print("[Screenshot] Saved ", path)


func _apply_capture_setup(entry: Dictionary) -> void:
	for flag in entry.get("set_flags", []):
		GameManager.set_flag(flag)
	for flag in entry.get("clear_flags", []):
		GameManager.story_flags.erase(flag)
	if entry.get("refresh_water", false) or entry.has("set_flags"):
		var controller := get_tree().get_first_node_in_group("water_controller")
		if controller and controller.has_method("sync_from_flags"):
			controller.sync_from_flags()


func _frame_camera(view: Dictionary) -> void:
	var cam := get_viewport().get_camera_3d()
	if cam == null:
		return
	if cam is Camera3D and cam.get("orbit_enabled") != null:
		cam.set("orbit_enabled", false)
	cam.global_position = view.cam
	cam.look_at(view.focus, Vector3.UP)
	if view.has("fov"):
		cam.fov = view.fov


func _hide_player_visual() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		var visual := player.get_node_or_null("Visual")
		if visual:
			visual.visible = false


func _hide_dialogue_ui() -> void:
	var panel := get_tree().root.find_child("DialoguePanel", true, false)
	if panel:
		panel.visible = false
