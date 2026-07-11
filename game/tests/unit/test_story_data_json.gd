class_name TestStoryDataJson
extends RefCounted
## Unit tests — story JSON files parse without error.


static func _parse_json_file(path: String) -> Variant:
	if not FileAccess.file_exists(path):
		return null
	var text := FileAccess.get_file_as_string(path)
	if text.is_empty():
		return null
	return JSON.parse_string(text)


static func test_scenes_json_parses() -> String:
	var data = _parse_json_file("res://data/story/scenes.json")
	if data == null:
		return "scenes.json missing or invalid JSON"
	if typeof(data) != TYPE_DICTIONARY:
		return "scenes.json root must be a Dictionary"
	if not data.has("scenes"):
		return "scenes.json must contain 'scenes' key"
	if typeof(data["scenes"]) != TYPE_ARRAY:
		return "scenes.json 'scenes' must be an Array"
	if data["scenes"].is_empty():
		return "scenes.json 'scenes' must not be empty"
	return ""


static func test_cinematic_hooks_json_parses() -> String:
	var data = _parse_json_file("res://data/story/cinematic_hooks.json")
	if data == null:
		return "cinematic_hooks.json missing or invalid JSON"
	if typeof(data) != TYPE_DICTIONARY:
		return "cinematic_hooks.json root must be a Dictionary"
	if not data.has("hooks"):
		return "cinematic_hooks.json must contain 'hooks' key"
	return ""


static func test_flags_json_parses() -> String:
	var data = _parse_json_file("res://data/story/flags.json")
	if data == null:
		return "flags.json missing or invalid JSON"
	if typeof(data) != TYPE_DICTIONARY:
		return "flags.json root must be a Dictionary"
	return ""


static func test_chapter_01_dialogue_parses() -> String:
	var data = _parse_json_file("res://data/dialogue/chapter_01.json")
	if data == null:
		return "chapter_01.json missing or invalid JSON"
	if typeof(data) != TYPE_DICTIONARY:
		return "chapter_01.json root must be a Dictionary"
	if not data.has("scenes"):
		return "chapter_01.json must contain 'scenes' key"
	return ""
