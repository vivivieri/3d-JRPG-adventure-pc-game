extends Node
## Resolves inline i18n objects `{en, ja, zh}` from story data.

const FALLBACK_LOCALE := "en"

var locale: String = FALLBACK_LOCALE


func _ready() -> void:
	var sys := TranslationServer.get_locale()
	if sys.length() >= 2:
		locale = sys.substr(0, 2)
	if locale not in ["en", "ja", "zh"]:
		locale = FALLBACK_LOCALE


func tr_text(value: Variant, fallback: String = "") -> String:
	if value is String:
		return value
	if value is Dictionary:
		if value.has(locale):
			return str(value[locale])
		if value.has(FALLBACK_LOCALE):
			return str(value[FALLBACK_LOCALE])
		for key in value:
			return str(value[key])
	return fallback
