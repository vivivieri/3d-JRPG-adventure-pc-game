extends Node
## Minimal autoload — validates data paths exist at startup.
## Full systems (GameManager, DialogueRunner, etc.) added in later implementation phases.


func _ready() -> void:
	var required := [
		"res://data/story/scenes.json",
		"res://data/story/flags.json",
		"res://data/dialogue/chapter_01.json",
	]
	for path in required:
		if not FileAccess.file_exists(path):
			push_error("Missing required data: %s", path)
