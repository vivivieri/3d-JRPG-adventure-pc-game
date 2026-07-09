extends Node
## Loads each world scene, waits for render, saves viewport PNG.


const SCENES := [
	{"file": "main_menu", "path": "res://scenes/world/main_menu.tscn"},
	{"file": "village", "path": "res://scenes/world/ruined_village.tscn"},
	{"file": "caves", "path": "res://scenes/world/tidal_caves.tscn"},
	{"file": "palace", "path": "res://scenes/world/dragon_palace_gate.tscn"},
]

const DEFAULT_OUT := "/opt/cursor/artifacts/screenshots"


func _ready() -> void:
	var out_dir: String = OS.get_environment("SCREENSHOT_DIR") if OS.has_environment("SCREENSHOT_DIR") else DEFAULT_OUT
	DirAccess.make_dir_recursive_absolute(out_dir)
	await get_tree().process_frame
	for entry in SCENES:
		await _capture_scene(entry, out_dir)
	print("[Screenshot] Done — saved %d images to %s" % [SCENES.size(), out_dir])
	get_tree().quit()


func _capture_scene(entry: Dictionary, out_dir: String) -> void:
	get_tree().change_scene_to_file(entry.path)
	# Allow zone visuals, materials, and lighting to settle.
	await get_tree().create_timer(2.0).timeout
	await get_tree().process_frame
	await get_tree().process_frame
	var img: Image = get_viewport().get_texture().get_image()
	var path := "%s/%s.png" % [out_dir, entry.file]
	var err := img.save_png(path)
	if err != OK:
		push_error("Failed to save %s (err %s)" % [path, err])
	else:
		print("[Screenshot] Saved ", path)
