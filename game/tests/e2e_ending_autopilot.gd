extends Node
## Bootstrap for GUI ending autopilot on scene root.

func _ready() -> void:
	call_deferred("_boot")


func _boot() -> void:
	var runner := Node.new()
	runner.name = "E2EEndingAutopilotRunner"
	runner.set_script(load("res://tests/e2e_ending_autopilot_runner.gd"))
	runner.process_mode = Node.PROCESS_MODE_ALWAYS
	get_tree().root.add_child(runner)
	await get_tree().process_frame
	runner.start()
