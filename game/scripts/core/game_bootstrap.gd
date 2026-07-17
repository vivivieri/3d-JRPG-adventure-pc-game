extends Node
## Startup validation — required game/data JSON paths (autoload_registry GameBootstrap).

const REQUIRED_DATA_PATHS: Array[String] = [
	"res://data/story/scenes.json",
	"res://data/story/flags.json",
	"res://data/dialogue/chapter_01.json",
	"res://data/encounters/story_encounters.json",
	"res://data/story/cinematic_hooks.json",
	"res://data/code/scene_registry.json",
	"res://data/code/autoload_registry.json",
	"res://data/world/zone_palettes.json",
]


func validate_data_paths() -> bool:
	return get_boot_errors().is_empty()


func get_boot_errors() -> PackedStringArray:
	var errors: PackedStringArray = []
	for path: String in REQUIRED_DATA_PATHS:
		if not FileAccess.file_exists(path):
			errors.append("Missing data file: %s" % path)
	return errors
