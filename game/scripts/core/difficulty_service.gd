extends RefCounted
class_name DifficultyService
## Combat difficulty — Normal default + optional Hard (docs/COMBAT_SYSTEMS.md §10).

const CATALOG_PATH := "res://data/combat/difficulty.json"

static var _catalog: Dictionary = {}


static func load_catalog() -> Dictionary:
	if not _catalog.is_empty():
		return _catalog
	if not FileAccess.file_exists(CATALOG_PATH):
		push_error("DifficultyService: missing %s" % CATALOG_PATH)
		return {}
	var file := FileAccess.open(CATALOG_PATH, FileAccess.READ)
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("DifficultyService: invalid difficulty.json")
		return {}
	_catalog = parsed
	return _catalog


static func active_mode_id(settings: Dictionary) -> String:
	var catalog := load_catalog()
	var key: String = str(catalog.get("policy", {}).get("hard_mode_setting", "hard_mode"))
	return "hard" if settings.get(key, false) else "normal"


static func mode_config(settings: Dictionary) -> Dictionary:
	var catalog := load_catalog()
	return catalog.get("modes", {}).get(active_mode_id(settings), {})


static func scale_enemy_hp(base: int, settings: Dictionary) -> int:
	return int(round(float(base) * float(mode_config(settings).get("enemy_hp_multiplier", 1.0))))


static func scale_enemy_atk(base: int, settings: Dictionary) -> int:
	return int(round(float(base) * float(mode_config(settings).get("enemy_atk_multiplier", 1.0))))


static func scale_xp(base: int, settings: Dictionary) -> int:
	return int(round(float(base) * float(mode_config(settings).get("xp_multiplier", 1.0))))


static func boss_shows_intent_preview(phase: int, is_boss: bool, settings: Dictionary) -> bool:
	if not is_boss:
		return true
	var cfg := mode_config(settings)
	if phase >= 2:
		return bool(cfg.get("boss_intent_preview_in_phase_2_plus", true))
	return int(cfg.get("boss_intent_preview_turns", 1)) > 0


static func tide_keeper_choice_gate_hp_percent(settings: Dictionary) -> float:
	return float(mode_config(settings).get("tide_keeper_choice_gate_hp_percent", 0.1))


static func is_hard_mode(settings: Dictionary) -> bool:
	return active_mode_id(settings) == "hard"


static func suggest_hard_after_clear(profile_meta: Dictionary) -> bool:
	var catalog := load_catalog()
	if not bool(catalog.get("policy", {}).get("suggest_hard_after_game_completed", true)):
		return false
	return bool(profile_meta.get("game_completed_once", false))
