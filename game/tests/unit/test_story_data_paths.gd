class_name TestStoryDataPaths
extends RefCounted
## Unit tests — required story data files exist on disk.


static func test_required_boot_paths_exist() -> String:
	var required := [
		"res://data/story/scenes.json",
		"res://data/story/flags.json",
		"res://data/story/cinematic_hooks.json",
		"res://data/dialogue/chapter_01.json",
	]
	for path in required:
		if not FileAccess.file_exists(path):
			return "Missing required data file: %s" % path
	return ""


static func test_core_data_catalog_exists() -> String:
	var paths := [
		"res://data/quests/main_quests.json",
		"res://data/encounters/story_encounters.json",
		"res://data/items/items.json",
		"res://data/skills/skills.json",
		"res://data/enemies/enemies.json",
		"res://data/starting/new_game.json",
	]
	for path in paths:
		if not FileAccess.file_exists(path):
			return "Missing catalog file: %s" % path
	return ""
