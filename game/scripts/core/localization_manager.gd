extends Node
## Minimal localization stub for GDAI regen branch (full i18n added in later phase).


signal locale_changed(locale_code: String)

var locale: String = "en"


func tr_key(key: String) -> String:
	match key:
		"UI_INTERACT_EXAMINE":
			return "Examine"
		"UI_INTERACT_TALK":
			return "Talk"
		"UI_INTERACT_FIGHT":
			return "Fight"
		"UI_INTERACT_ENTER":
			return "Enter"
		"UI_INTERACT_KEY":
			return "E"
		"UI_DIALOGUE_ADVANCE":
			return "Space / E - continue"
		_:
			return key.replace("UI_", "").replace("_", " ").capitalize()


func resolve_text(value: Variant) -> String:
	if value is String:
		return value
	if value is Dictionary:
		return String(value.get(locale, value.get("en", "")))
	return str(value)
