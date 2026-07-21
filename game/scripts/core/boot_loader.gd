extends Node
## Boot scene entry — validate data then proceed (main_menu wired in Phase 2).


func _ready() -> void:
	run_boot()


func run_boot() -> void:
	if not GameBootstrap.validate_data_paths():
		for line: String in get_boot_errors():
			push_error(line)
		get_tree().quit(1)
		return
	if DisplayServer.get_name() == "headless":
		get_tree().quit(0)


func get_boot_errors() -> PackedStringArray:
	return GameBootstrap.get_boot_errors()
