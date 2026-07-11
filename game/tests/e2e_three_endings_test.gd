extends Node
## Bootstrap: root-attached runner survives ending scene changes.

func _ready() -> void:
	call_deferred("_boot")


func _boot() -> void:
	var runner := Node.new()
	runner.name = "E2EEndingsRunner"
	runner.set_script(load("res://tests/e2e_three_endings_runner.gd"))
	runner.process_mode = Node.PROCESS_MODE_ALWAYS
	get_tree().root.add_child(runner)
	await get_tree().process_frame
	runner.start()
