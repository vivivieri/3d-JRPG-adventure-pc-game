extends Node
## Loads each world scene, frames the camera, and saves viewport PNG.


const SCENES := [
	{"file": "main_menu", "path": "res://scenes/world/main_menu.tscn"},
	{"file": "village", "path": "res://scenes/world/ruined_village.tscn"},
	{"file": "caves", "path": "res://scenes/world/tidal_caves.tscn"},
	{"file": "palace", "path": "res://scenes/world/dragon_palace_gate.tscn"},
]

const CAMERA_VIEWS := {
	"village": {"cam": Vector3(12, 8, 14), "focus": Vector3(0, 1.5, 0), "fov": 68.0},
	"caves": {"cam": Vector3(5, 4.5, 10), "focus": Vector3(0, 1.5, -8), "fov": 65.0},
	"palace": {"cam": Vector3(8, 24, 50), "focus": Vector3(0, 2, 0), "fov": 80.0},
}

const DEFAULT_OUT := "/opt/cursor/artifacts/screenshots"


func _ready() -> void:
	var out_dir: String = OS.get_environment("SCREENSHOT_DIR") if OS.has_environment("SCREENSHOT_DIR") else DEFAULT_OUT
	DirAccess.make_dir_recursive_absolute(out_dir)
	_preload_story_flags()
	await get_tree().process_frame
	for entry in SCENES:
		await _capture_scene(entry, out_dir)
	print("[Screenshot] Done — saved %d images to %s" % [SCENES.size(), out_dir])
	get_tree().quit()


func _preload_story_flags() -> void:
	# Prevent auto-dialogue from covering palace / cave shots.
	GameManager.set_flag("gate_arrival_dialogue")
	GameManager.set_flag("palace_vision_seen")
	GameManager.set_flag("caves_entrance_dialogue")


func _capture_scene(entry: Dictionary, out_dir: String) -> void:
	get_tree().change_scene_to_file(entry.path)
	await get_tree().create_timer(5.0).timeout
	_hide_dialogue_ui()
	_hide_player_visual()
	if CAMERA_VIEWS.has(entry.file):
		_frame_camera(CAMERA_VIEWS[entry.file])
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
