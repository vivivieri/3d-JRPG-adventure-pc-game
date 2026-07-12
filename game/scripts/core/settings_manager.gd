extends Node
## Persists player options to user://settings.json.


const SETTINGS_PATH := "user://settings.json"

const DEFAULTS := {
	"locale": "en",
	"vo_dialect": "cant",
	"master_volume": 0.8,
	"music_volume": 0.7,
	"sfx_volume": 0.8,
	"fullscreen": "windowed",
	"resolution": "1920x1080",
	"vsync": true,
	"text_speed": "normal",
	"dialogue_auto": false,
	"screen_shake": true,
	"hard_mode": false,
	"hints_enabled": true,
	"intent_contrast": "standard",
	"graphics_quality": "medium",
}

var _settings: Dictionary = {}


func _ready() -> void:
	load_settings()


func load_settings() -> void:
	_settings = DEFAULTS.duplicate(true)
	if not FileAccess.file_exists(SETTINGS_PATH):
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SETTINGS_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("SettingsManager: invalid settings file, using defaults")
		return
	for key in parsed.keys():
		if DEFAULTS.has(key):
			_settings[key] = parsed[key]


func save_settings() -> void:
	var file := FileAccess.open(SETTINGS_PATH, FileAccess.WRITE)
	if file == null:
		push_error("SettingsManager: failed to write %s" % SETTINGS_PATH)
		return
	file.store_string(JSON.stringify(_settings, "\t"))
	EventBus.settings_changed.emit()


func get_value(key: String) -> Variant:
	return _settings.get(key, DEFAULTS.get(key))


func set_value(key: String, value: Variant) -> void:
	if not DEFAULTS.has(key):
		push_warning("SettingsManager: unknown key %s" % key)
		return
	_settings[key] = value


func get_locale() -> String:
	return str(get_value("locale"))


func set_locale(locale: String) -> void:
	set_value("locale", locale)


func get_vo_dialect() -> String:
	return str(get_value("vo_dialect"))


func set_vo_dialect(dialect: String) -> void:
	set_value("vo_dialect", dialect)
