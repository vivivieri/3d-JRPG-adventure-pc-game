extends Node
## Runtime localization — English, Japanese, Simplified Chinese.

const SETTINGS_PATH := "user://settings.json"
const TRANSLATIONS_CSV := "res://locale/translations.csv"

const LOCALE_EN := "en"
const LOCALE_JA := "ja"
const LOCALE_ZH := "zh"

const SUPPORTED_LOCALES: Array[String] = [LOCALE_EN, LOCALE_JA, LOCALE_ZH]

const LOCALE_LABELS := {
	LOCALE_EN: "English",
	LOCALE_JA: "日本語",
	LOCALE_ZH: "简体中文",
}

var current_locale: String = LOCALE_EN

var _translations: Dictionary = {}  # locale -> { key -> text }


func _ready() -> void:
	_load_csv(TRANSLATIONS_CSV)
	_apply_translations_to_server()
	_load_settings()
	set_locale(current_locale)


func set_locale(locale_code: String) -> void:
	if locale_code not in SUPPORTED_LOCALES:
		push_warning("Unsupported locale: %s" % locale_code)
		return
	current_locale = locale_code
	TranslationServer.set_locale(locale_code)
	_save_settings()
	EventBus.locale_changed.emit(locale_code)


func get_locale() -> String:
	return current_locale


func tr_key(key: String, placeholders: Dictionary = {}) -> String:
	var text := _lookup(key, current_locale)
	if text.is_empty():
		text = _lookup(key, LOCALE_EN)
	if text.is_empty():
		return key
	return _format(text, placeholders)


func resolve_text(value: Variant) -> String:
	if value == null:
		return ""
	if value is String:
		if value.is_empty():
			return ""
		# String may be a translation key (contains a dot) or literal fallback.
		var translated := tr_key(value)
		return translated if translated != value else value
	if value is Dictionary:
		if value.has(current_locale):
			return str(value[current_locale])
		if value.has(LOCALE_EN):
			return str(value[LOCALE_EN])
		for loc in SUPPORTED_LOCALES:
			if value.has(loc):
				return str(value[loc])
	return str(value)


func resolve_field(data: Dictionary, field: String) -> String:
	var key_name := "%s_key" % field
	if data.has(key_name):
		return tr_key(str(data[key_name]))
	if data.has(field):
		return resolve_text(data[field])
	return ""


func speaker_name(speaker_id: String) -> String:
	return tr_key("speaker.%s" % speaker_id)


func skill_name(skill_id: String) -> String:
	return tr_key("skill.%s.name" % skill_id)


func skill_description(skill_id: String) -> String:
	return tr_key("skill.%s.desc" % skill_id)


func enemy_name(enemy_id: String) -> String:
	return tr_key("enemy.%s.name" % enemy_id)


func item_name(item_id: String) -> String:
	return tr_key("item.%s.name" % item_id)


func item_description(item_id: String) -> String:
	return tr_key("item.%s.desc" % item_id)


func character_name(char_id: String) -> String:
	return tr_key("character.%s.name" % char_id)


func character_title(char_id: String) -> String:
	return tr_key("character.%s.title" % char_id)


func quest_title(quest_id: String) -> String:
	return tr_key("quest.%s.title" % quest_id)


func quest_description(quest_id: String) -> String:
	return tr_key("quest.%s.desc" % quest_id)


func quest_stage_description(quest_id: String, stage_id: String) -> String:
	return tr_key("quest.%s.stage.%s" % [quest_id, stage_id])


func _lookup(key: String, locale_code: String) -> String:
	var bucket: Variant = _translations.get(locale_code, {})
	if bucket is Dictionary:
		return bucket.get(key, "")
	return ""


func _format(text: String, placeholders: Dictionary) -> String:
	var result := text
	for key in placeholders.keys():
		result = result.replace("{%s}" % key, str(placeholders[key]))
	return result


func _load_csv(path: String) -> void:
	for loc in SUPPORTED_LOCALES:
		_translations[loc] = {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("Missing translations CSV: %s" % path)
		return
	var header: PackedStringArray = file.get_csv_line()
	if header.size() < 2:
		push_error("Invalid translations CSV header")
		file.close()
		return
	var locale_columns: Dictionary = {}
	for i in range(1, header.size()):
		var col_locale := header[i].strip_edges().to_lower()
		if col_locale in SUPPORTED_LOCALES:
			locale_columns[i] = col_locale
	while not file.eof_reached():
		var row: PackedStringArray = file.get_csv_line()
		if row.size() < 2 or row[0].strip_edges().is_empty():
			continue
		if row[0].begins_with("#"):
			continue
		var row_key := row[0].strip_edges()
		for col_index in locale_columns.keys():
			var loc: String = locale_columns[col_index]
			if col_index < row.size():
				_translations[loc][row_key] = row[col_index]
	file.close()


func _apply_translations_to_server() -> void:
	for loc in SUPPORTED_LOCALES:
		var translation := Translation.new()
		translation.locale = loc
		var bucket: Dictionary = _translations.get(loc, {})
		for key in bucket.keys():
			translation.add_message(key, bucket[key])
		TranslationServer.add_translation(translation)


func _load_settings() -> void:
	if not FileAccess.file_exists(SETTINGS_PATH):
		current_locale = _detect_system_locale()
		return
	var file := FileAccess.open(SETTINGS_PATH, FileAccess.READ)
	if file == null:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	file.close()
	if parsed is Dictionary and parsed.get("locale", "") in SUPPORTED_LOCALES:
		current_locale = parsed.get("locale")


func _save_settings() -> void:
	var file := FileAccess.open(SETTINGS_PATH, FileAccess.WRITE)
	if file == null:
		return
	file.store_string(JSON.stringify({ "locale": current_locale }, "\t"))
	file.close()


func _detect_system_locale() -> String:
	var locale := TranslationServer.get_locale().to_lower()
	if locale.begins_with("ja"):
		return LOCALE_JA
	if locale.begins_with("zh"):
		return LOCALE_ZH
	return LOCALE_EN
