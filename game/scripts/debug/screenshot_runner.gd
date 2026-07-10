extends Node
## Loads each world scene, frames the camera, and saves viewport PNG.


const CAPTURES := [
	{"file": "main_menu", "path": "res://scenes/world/main_menu.tscn", "wait": 2.0},
	{
		"file": "gameplay_beach",
		"path": "res://scenes/world/beach_shore.tscn",
		"wait": 8.0,
		"use_player_camera": true,
		"player_pos": Vector3(0, 1, 8),
		"player_look_at": Vector3(0, 0.5, 2),
	},
	{
		"file": "gameplay_village",
		"path": "res://scenes/world/ruined_village.tscn",
		"wait": 8.0,
		"use_player_camera": true,
		"player_pos": Vector3(0, 1, 4),
		"player_look_at": Vector3(-6, 1.5, -5),
	},
	{
		"file": "gameplay_interact",
		"path": "res://scenes/world/ruined_village.tscn",
		"wait": 0.8,
		"reuse_scene": true,
		"use_player_camera": true,
		"player_pos": Vector3(-5.5, 1, -2.5),
		"player_look_at": Vector3(-6, 2.5, -5),
		"show_interact_prompt": true,
	},
	{
		"file": "gameplay_dialogue",
		"path": "res://scenes/world/ruined_village.tscn",
		"wait": 0.5,
		"reuse_scene": true,
		"use_player_camera": true,
		"player_pos": Vector3(-5.5, 1, -2.5),
		"player_look_at": Vector3(-6, 2.5, -5),
		"show_dialogue": true,
		"dialogue_id": "SC-03",
	},
	{
		"file": "gameplay_combat",
		"path": "res://scenes/world/ruined_village.tscn",
		"wait": 0.5,
		"reuse_scene": true,
		"use_player_camera": true,
		"player_pos": Vector3(0, 1, -6),
		"player_look_at": Vector3(0, 1, -10),
		"start_combat": ["salt_crab"],
	},
	{
		"file": "gameplay_caves",
		"path": "res://scenes/world/tidal_caves.tscn",
		"wait": 8.0,
		"use_player_camera": true,
		"player_pos": Vector3(0, 1, 2),
		"player_look_at": Vector3(0, 1.5, -8),
	},
	{
		"file": "gameplay_palace",
		"path": "res://scenes/world/dragon_palace_gate.tscn",
		"wait": 8.0,
		"use_player_camera": true,
		"player_pos": Vector3(0, 1, 6),
		"player_look_at": Vector3(0, 3, 14),
	},
	{
		"file": "beach",
		"path": "res://scenes/world/beach_shore.tscn",
		"cam": Vector3(5, 4.2, 12),
		"focus": Vector3(0, 0.6, 6),
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
		"file": "village_torii",
		"path": "res://scenes/world/ruined_village.tscn",
		"cam": Vector3(-2, 3.5, 2),
		"focus": Vector3(-6, 3.2, -5),
		"fov": 55.0,
		"wait": 0.8,
		"reuse_scene": true,
	},
	{
		"file": "dialogue_torii",
		"path": "res://scenes/world/ruined_village.tscn",
		"cam": Vector3(-3, 3.2, 1),
		"focus": Vector3(-6, 2.8, -5),
		"fov": 58.0,
		"wait": 0.5,
		"reuse_scene": true,
		"show_dialogue": true,
		"dialogue_id": "SC-03",
	},
	{
		"file": "combat_tutorial",
		"path": "res://scenes/world/ruined_village.tscn",
		"cam": Vector3(4, 5, 6),
		"focus": Vector3(0, 1.2, -8),
		"fov": 62.0,
		"wait": 0.5,
		"reuse_scene": true,
		"start_combat": ["salt_crab"],
	},
	{
		"file": "field_menu",
		"path": "res://scenes/world/ruined_village.tscn",
		"cam": Vector3(6, 5, 10),
		"focus": Vector3(0, 1.0, 2),
		"fov": 65.0,
		"wait": 0.5,
		"reuse_scene": true,
		"open_field_menu": true,
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
		"file": "caves_boss",
		"path": "res://scenes/world/tidal_caves.tscn",
		"cam": Vector3(0, 4.5, -22),
		"focus": Vector3(0, 2.0, -28),
		"fov": 64.0,
		"wait": 0.6,
		"reuse_scene": true,
	},
	{
		"file": "palace",
		"path": "res://scenes/world/dragon_palace_gate.tscn",
		"cam": Vector3(0, 14, 28),
		"focus": Vector3(0, 2.5, 6),
		"fov": 74.0,
		"wait": 8.0,
	},
	{
		"file": "palace_gate",
		"path": "res://scenes/world/dragon_palace_gate.tscn",
		"cam": Vector3(0, 6, 18),
		"focus": Vector3(0, 4.5, 12),
		"fov": 60.0,
		"wait": 0.8,
		"reuse_scene": true,
	},
	{
		"file": "combat_boss",
		"path": "res://scenes/world/dragon_palace_gate.tscn",
		"cam": Vector3(2, 5, -24),
		"focus": Vector3(0, 2.5, -30),
		"fov": 62.0,
		"wait": 0.5,
		"reuse_scene": true,
		"start_combat": ["tide_keeper"],
	},
	{
		"file": "ending_rewind",
		"path": "res://scenes/world/ending_rewind.tscn",
		"wait": 3.0,
	},
	{
		"file": "ending_anchor",
		"path": "res://scenes/world/ending_anchor.tscn",
		"wait": 3.0,
	},
	{
		"file": "ending_drift",
		"path": "res://scenes/world/ending_drift.tscn",
		"wait": 3.0,
	},
]

const DEFAULT_OUT := "/opt/cursor/artifacts/screenshots"

var _current_scene_path := ""


func _ready() -> void:
	var out_dir: String = OS.get_environment("SCREENSHOT_DIR") if OS.has_environment("SCREENSHOT_DIR") else DEFAULT_OUT
	DirAccess.make_dir_recursive_absolute(out_dir)
	_preload_story_flags()
	var filter := OS.get_environment("SCREENSHOT_FILTER") if OS.has_environment("SCREENSHOT_FILTER") else ""
	await get_tree().process_frame
	for entry in CAPTURES:
		if not filter.is_empty() and not str(entry.file).begins_with(filter):
			continue
		await _capture_entry(entry, out_dir)
	var count := CAPTURES.size() if filter.is_empty() else CAPTURES.filter(func(e): return str(e.file).begins_with(filter)).size()
	print("[Screenshot] Done — saved %d images to %s" % [count, out_dir])
	get_tree().quit()


func _preload_story_flags() -> void:
	GameManager.set_flag("gate_arrival_dialogue")
	GameManager.set_flag("palace_vision_seen")
	GameManager.set_flag("caves_entrance_dialogue")
	GameManager.set_flag("village_arrival_seen")
	GameManager.set_flag("beach_arrival_seen")


func _capture_entry(entry: Dictionary, out_dir: String) -> void:
	if not entry.get("reuse_scene", false) or entry.path != _current_scene_path:
		get_tree().change_scene_to_file(entry.path)
		_current_scene_path = entry.path
		await get_tree().create_timer(entry.get("wait", 5.0)).timeout
	else:
		await get_tree().create_timer(entry.get("wait", 0.5)).timeout
	_apply_capture_setup(entry)
	_position_player(entry)
	if entry.get("show_dialogue", false):
		_show_dialogue(entry.get("dialogue_id", "SC-03"))
	elif entry.get("start_combat", []).size() > 0:
		_start_combat(entry.start_combat)
	elif entry.get("open_field_menu", false):
		_open_field_menu()
	else:
		_hide_dialogue_ui()
		_hide_combat_ui()
	if entry.get("show_interact_prompt", false):
		_force_interact_prompt()
	if entry.get("hide_player", entry.has("cam") and not entry.get("use_player_camera", false)):
		_hide_player_visual()
	else:
		_ensure_player_visible()
	if entry.get("use_player_camera", false):
		_set_player_camera_yaw(entry)
		await get_tree().process_frame
	elif entry.has("cam") and entry.has("focus"):
		_frame_camera(entry)
	await get_tree().create_timer(0.8).timeout
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


func _ensure_player_visible() -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player:
		var visual := player.get_node_or_null("Visual")
		if visual:
			visual.visible = true
		elif player.has_method("_add_visual"):
			player._add_visual()


func _position_player(entry: Dictionary) -> void:
	if not entry.has("player_pos"):
		return
	var player := get_tree().get_first_node_in_group("player") as Node3D
	if player == null:
		return
	player.global_position = entry.player_pos
	if entry.has("player_look_at"):
		player.look_at(entry.player_look_at, Vector3.UP)


func _force_interact_prompt() -> void:
	var hud := get_tree().root.find_child("InteractionPromptHud", true, false)
	if hud and hud.has_method("show_prompt"):
		hud.show_prompt(LocalizationManager.tr_key("UI_INTERACT_EXAMINE"))


func _hide_dialogue_ui() -> void:
	var panel := get_tree().root.find_child("DialoguePanel", true, false)
	if panel:
		panel.visible = false


func _hide_combat_ui() -> void:
	var combat := get_tree().root.find_child("CombatRoot", true, false)
	if combat:
		combat.get_parent().visible = false


func _show_dialogue(scene_id: String) -> void:
	_hide_combat_ui()
	DialogueRunner.play_scene(scene_id)
	await get_tree().create_timer(0.4).timeout
	var dlg := get_tree().root.find_child("DialogueBox", true, false)
	if dlg and dlg.has_method("_finish_typing"):
		dlg._finish_typing()
	var panel := get_tree().root.find_child("DialoguePanel", true, false)
	if panel:
		panel.visible = true
	await get_tree().create_timer(0.6).timeout


func _set_player_camera_yaw(entry: Dictionary) -> void:
	var player := get_tree().get_first_node_in_group("player")
	if player == null:
		return
	var cam := player.get_node_or_null("Camera3D")
	if cam == null or cam.get("orbit_enabled") == null:
		return
	cam.set("orbit_enabled", true)
	if entry.has("player_look_at"):
		var to: Vector3 = entry.player_look_at - player.global_position
		cam.set("_yaw", atan2(to.x, to.z))
	cam.call("_apply_transform")


func _start_combat(enemy_ids: Array) -> void:
	_hide_dialogue_ui()
	GameManager.start_combat(enemy_ids)
	await get_tree().create_timer(1.2).timeout
	var combat_layer := get_tree().root.find_child("CombatUi", true, false)
	if combat_layer:
		combat_layer.visible = true
	var combat := get_tree().root.find_child("CombatRoot", true, false)
	if combat:
		combat.get_parent().visible = true


func _open_field_menu() -> void:
	_hide_dialogue_ui()
	_hide_combat_ui()
	var field_menu := get_tree().root.find_child("FieldMenu", true, false)
	if field_menu and field_menu.has_method("open_menu"):
		field_menu.open_menu()
	await get_tree().process_frame
