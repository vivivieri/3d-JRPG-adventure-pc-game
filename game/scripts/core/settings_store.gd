extends RefCounted
class_name SettingsStore
## Persisted player settings — user://settings.json (docs/SETTINGS_ACCESSIBILITY.md).

const DEFAULTS_PATH := "res://data/settings/settings_defaults.json"
const SAVE_PATH := "user://settings.json"

static var _cache: Dictionary = {}


static func defaults() -> Dictionary:
	if not FileAccess.file_exists(DEFAULTS_PATH):
		return {"hard_mode": false}
	var file := FileAccess.open(DEFAULTS_PATH, FileAccess.READ)
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return {"hard_mode": false}
	return (parsed.get("defaults", {}) as Dictionary).duplicate(true)


static func load_settings() -> Dictionary:
	if not _cache.is_empty():
		return _cache.duplicate(true)
	var merged := defaults()
	if FileAccess.file_exists(SAVE_PATH):
		var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
		if file:
			var parsed: Variant = JSON.parse_string(file.get_as_text())
			if typeof(parsed) == TYPE_DICTIONARY:
				for key in parsed.keys():
					merged[key] = parsed[key]
	_cache = merged.duplicate(true)
	return merged.duplicate(true)


static func save_settings(settings: Dictionary) -> void:
	_cache = settings.duplicate(true)
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("SettingsStore: cannot write %s" % SAVE_PATH)
		return
	file.store_string(JSON.stringify(settings, "\t"))


static func get_value(key: String, fallback: Variant = null) -> Variant:
	var settings := load_settings()
	if settings.has(key):
		return settings[key]
	return fallback


static func set_value(key: String, value: Variant) -> void:
	var settings := load_settings()
	var prior_hard: bool = bool(settings.get("hard_mode", false))
	settings[key] = value
	save_settings(settings)
	if key == "hard_mode" and bool(value) != prior_hard:
		_emit_hard_mode_changed(bool(value))


static func _emit_hard_mode_changed(enabled: bool) -> void:
	var tree := Engine.get_main_loop()
	if tree == null:
		return
	var bus := tree.root.get_node_or_null("/root/EventBus")
	if bus and bus.has_signal("hard_mode_changed"):
		bus.hard_mode_changed.emit(enabled)


static func is_hard_mode() -> bool:
	return bool(get_value("hard_mode", false))


static func set_hard_mode(enabled: bool) -> void:
	set_value("hard_mode", enabled)
