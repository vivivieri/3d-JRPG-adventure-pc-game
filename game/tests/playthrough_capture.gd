extends Node
## Bootstrap: attaches capture runner to scene root so it survives scene changes.

func _ready() -> void:
	call_deferred("_boot")


func _boot() -> void:
	var runner := Node.new()
	runner.name = "CaptureRunner"
	runner.set_script(load("res://tests/capture_runner.gd"))
	runner.process_mode = Node.PROCESS_MODE_ALWAYS
	get_tree().root.add_child(runner)
	await get_tree().process_frame
	runner.start()
