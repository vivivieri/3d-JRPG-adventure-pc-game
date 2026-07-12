extends SceneTree
## Headless unit test runner.
## Usage: godot4 --headless --path game -s res://tests/unit/test_runner.gd

const TestStoryDataPaths := preload("res://tests/unit/test_story_data_paths.gd")
const TestStoryDataJson := preload("res://tests/unit/test_story_data_json.gd")
const TestVoiceLinePlayer := preload("res://tests/unit/test_voice_line_player.gd")
const TestLocalizationManager := preload("res://tests/unit/test_localization_manager.gd")

var _passed := 0
var _failed := 0
var _failures: PackedStringArray = []


func _initialize() -> void:
	call_deferred("_run_all")


func _run_all() -> void:
	print("==> Godot unit tests")
	_run_test("story_data_paths.required_boot_paths_exist", TestStoryDataPaths.test_required_boot_paths_exist)
	_run_test("story_data_paths.core_data_catalog_exists", TestStoryDataPaths.test_core_data_catalog_exists)
	_run_test("story_data_json.scenes_json_parses", TestStoryDataJson.test_scenes_json_parses)
	_run_test("story_data_json.cinematic_hooks_json_parses", TestStoryDataJson.test_cinematic_hooks_json_parses)
	_run_test("story_data_json.flags_json_parses", TestStoryDataJson.test_flags_json_parses)
	_run_test("story_data_json.chapter_01_dialogue_parses", TestStoryDataJson.test_chapter_01_dialogue_parses)
	_run_test("voice_line_player.en_locale_path", TestVoiceLinePlayer.test_en_locale_path)
	_run_test("voice_line_player.ja_locale_path", TestVoiceLinePlayer.test_ja_locale_path)
	_run_test("voice_line_player.zh_hant_cant_path", TestVoiceLinePlayer.test_zh_hant_cant_path)
	_run_test("voice_line_player.zh_hant_cmn_path", TestVoiceLinePlayer.test_zh_hant_cmn_path)
	_run_test("voice_line_player.empty_voice_id", TestVoiceLinePlayer.test_empty_voice_id)
	_run_test("voice_line_player.invalid_dialect_fallback", TestVoiceLinePlayer.test_invalid_dialect_falls_back_to_cant)
	_run_test("localization_manager.tr_key_english", TestLocalizationManager.test_tr_key_english)
	_run_test("localization_manager.tr_key_japanese", TestLocalizationManager.test_tr_key_japanese)
	_run_test("localization_manager.tr_key_zh_hant", TestLocalizationManager.test_tr_key_zh_hant)
	_run_test("localization_manager.skill_name", TestLocalizationManager.test_skill_name)
	_run_test("localization_manager.enemy_name", TestLocalizationManager.test_enemy_name)
	_run_test("localization_manager.resolve_text_dict", TestLocalizationManager.test_resolve_text_dict)
	_run_test("localization_manager.combat_log_placeholders", TestLocalizationManager.test_combat_log_placeholders)
	_run_test("localization_manager.missing_key_returns_key", TestLocalizationManager.test_missing_key_returns_key)
	_run_test("localization_manager.vo_dialect_setting", TestLocalizationManager.test_vo_dialect_setting)
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
