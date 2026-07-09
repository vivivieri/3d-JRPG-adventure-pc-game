extends SceneTree
## Bootstrap for automated cloud screenshots (run with -s flag).


func _initialize() -> void:
	var helper := Node.new()
	helper.name = "ScreenshotHelper"
	helper.set_script(load("res://scripts/debug/screenshot_runner.gd"))
	root.add_child(helper)
