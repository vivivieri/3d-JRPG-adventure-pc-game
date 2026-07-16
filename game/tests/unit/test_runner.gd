extends SceneTree
## Headless unit test runner.
## Usage: godot4 --headless --path game -s res://tests/unit/test_runner.gd

const TestStoryDataPaths := preload("res://tests/unit/test_story_data_paths.gd")
const TestStoryDataJson := preload("res://tests/unit/test_story_data_json.gd")
const TestZoneVisuals := preload("res://tests/unit/test_zone_visuals.gd")

var _passed := 0
var _failed := 0
var _failures: PackedStringArray = []


func _initialize() -> void:
	print("==> Godot unit tests")
	_run_test(
		"story_data_paths.required_boot_paths_exist",
		TestStoryDataPaths.test_required_boot_paths_exist,
	)
	_run_test(
		"story_data_paths.core_data_catalog_exists",
		TestStoryDataPaths.test_core_data_catalog_exists,
	)
	_run_test("story_data_json.scenes_json_parses", TestStoryDataJson.test_scenes_json_parses)
	_run_test("story_data_json.flags_json_parses", TestStoryDataJson.test_flags_json_parses)
	_run_test(
		"story_data_json.chapter_01_dialogue_parses",
		TestStoryDataJson.test_chapter_01_dialogue_parses,
	)
	_run_test("zone_visuals.hex_to_color", TestZoneVisuals.test_hex_to_color_parses_village_fog)
	_run_test(
		"zone_visuals.ruined_village_preset",
		TestZoneVisuals.test_ruined_village_preset_has_directional,
	)
	_run_test(
		"zone_visuals.build_environment",
		TestZoneVisuals.test_build_environment_fog_enabled,
	)
	print("")
	print("Passed: %d | Failed: %d" % [_passed, _failed])
	if _failed > 0:
		for msg in _failures:
			print("  [FAIL] %s" % msg)
	quit(_failed)


func _run_test(label: String, callable: Callable) -> void:
	var err: String = callable.call()
	if err.is_empty():
		print("[PASS] %s" % label)
		_passed += 1
	else:
		print("[FAIL] %s — %s" % [label, err])
		_failures.append("%s — %s" % [label, err])
		_failed += 1
