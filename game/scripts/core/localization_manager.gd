extends Node
class_name LocalizationManagerNode
## Loads translations.csv and resolves locale-aware strings.


const TRANSLATIONS_PATH := "res://locale/translations.csv"
const SUPPORTED_LOCALES := ["en", "ja", "zh", "zh-Hant"]
const VO_DIALECTS := ["cant", "cmn"]

var _table: Dictionary = {}
var _locale: String = "en"
var _vo_dialect: String = "cant"


func _ready() -> void:
	_load_csv()
	_locale = SettingsManager.get_locale()
	_vo_dialect = SettingsManager.get_vo_dialect()
	FontThemeManager.apply_locale(_locale)


func get_locale() -> String:
	return _locale


func get_vo_dialect() -> String:
	return _vo_dialect


func set_locale(locale: String) -> void:
	if locale not in SUPPORTED_LOCALES:
		push_warning("LocalizationManager: unsupported locale %s" % locale)
		return
	if _locale == locale:
		return
	_locale = locale
	SettingsManager.set_locale(locale)
	SettingsManager.save_settings()
	FontThemeManager.apply_locale(_locale)
	EventBus.locale_changed.emit(_locale)


func set_vo_dialect(dialect: String) -> void:
	if dialect not in VO_DIALECTS:
		push_warning("LocalizationManager: unsupported dialect %s" % dialect)
		return
	if _vo_dialect == dialect:
		return
	_vo_dialect = dialect
	SettingsManager.set_vo_dialect(dialect)
	SettingsManager.save_settings()
	EventBus.vo_dialect_changed.emit(_vo_dialect)


func tr_key(key: String, placeholders: Dictionary = {}) -> String:
	if _table.is_empty():
		_load_csv()
	var row: Dictionary = _table.get(key, {})
	var text := str(row.get(_locale, row.get("en", key)))
	return _apply_placeholders(text, placeholders)


func resolve_text(text_obj: Variant) -> String:
	if typeof(text_obj) == TYPE_STRING:
		return text_obj
	if typeof(text_obj) != TYPE_DICTIONARY:
		return str(text_obj)
	var dict := text_obj as Dictionary
	if dict.has(_locale):
		return str(dict[_locale])
	if dict.has("en"):
		return str(dict["en"])
	return ""


func skill_name(skill_id: String) -> String:
	return tr_key("skill.%s.name" % skill_id)


func skill_desc(skill_id: String) -> String:
	return tr_key("skill.%s.desc" % skill_id)


func enemy_name(enemy_id: String) -> String:
	return tr_key("enemy.%s.name" % enemy_id)


func speaker_name(speaker_id: String) -> String:
	return tr_key("speaker.%s" % speaker_id)


func character_name(character_id: String) -> String:
	return tr_key("character.%s.name" % character_id)


func status_name(status_id: String) -> String:
	return tr_key("status.%s" % status_id)


func combat_log(key: String, placeholders: Dictionary = {}) -> String:
	return tr_key("combat.%s" % key, placeholders)


func has_key(key: String) -> bool:
	return _table.has(key)


func _load_csv() -> void:
	_table.clear()
	if not FileAccess.file_exists(TRANSLATIONS_PATH):
		push_error("LocalizationManager: missing %s" % TRANSLATIONS_PATH)
		return
	var file := FileAccess.open(TRANSLATIONS_PATH, FileAccess.READ)
	if file == null:
		push_error("LocalizationManager: failed to open %s" % TRANSLATIONS_PATH)
		return
	var headers: PackedStringArray = file.get_csv_line()
	if headers.size() < 2 or headers[0] != "keys":
		push_error("LocalizationManager: invalid CSV header")
		return
	while not file.eof_reached():
		var row: PackedStringArray = file.get_csv_line()
		if row.is_empty() or row[0].is_empty():
			continue
		var entry: Dictionary = {}
		for i in range(1, min(row.size(), headers.size())):
			entry[headers[i]] = row[i]
		_table[row[0]] = entry


func _apply_placeholders(text: String, placeholders: Dictionary) -> String:
	var result := text
	for key in placeholders.keys():
		result = result.replace("{%s}" % key, str(placeholders[key]))
	return result
