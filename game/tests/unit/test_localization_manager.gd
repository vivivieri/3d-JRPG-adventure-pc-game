class_name TestLocalizationManager
extends RefCounted
## Unit tests — LocalizationManager CSV resolution via autoload.


static func _lm() -> Node:
	return Engine.get_main_loop().root.get_node("LocalizationManager")


static func test_tr_key_english() -> String:
	_lm().set_locale("en")
	var text: String = _lm().tr_key("UI_NEW_GAME")
	if text != "New Game":
		return "Expected 'New Game', got: %s" % text
	return ""


static func test_tr_key_japanese() -> String:
	_lm().set_locale("ja")
	var text: String = _lm().tr_key("UI_NEW_GAME")
	if text != "はじめから":
		return "Expected Japanese UI_NEW_GAME, got: %s" % text
	_lm().set_locale("en")
	return ""


static func test_tr_key_zh_hant() -> String:
	_lm().set_locale("zh-Hant")
	var text: String = _lm().tr_key("UI_NEW_GAME")
	if text != "新遊戲":
		return "Expected Traditional Chinese UI_NEW_GAME, got: %s" % text
	_lm().set_locale("en")
	return ""


static func test_skill_name() -> String:
	_lm().set_locale("en")
	var name: String = _lm().skill_name("tidal_slash")
	if name != "Tidal Slash":
		return "Expected 'Tidal Slash', got: %s" % name
	return ""


static func test_enemy_name() -> String:
	_lm().set_locale("ja")
	var name: String = _lm().enemy_name("salt_crab")
	if name != "塩蟹":
		return "Expected Japanese salt_crab name, got: %s" % name
	_lm().set_locale("en")
	return ""


static func test_resolve_text_dict() -> String:
	_lm().set_locale("zh")
	var text: String = _lm().resolve_text({
		"en": "Hello",
		"ja": "こんにちは",
		"zh": "你好",
		"zh-Hant": "你好",
	})
	if text != "你好":
		return "Expected Simplified Chinese resolve, got: %s" % text
	_lm().set_locale("en")
	return ""


static func test_combat_log_placeholders() -> String:
	_lm().set_locale("en")
	var line: String = _lm().combat_log("action_attack", {
		"actor": "Urashima",
		"target": "Salt Crab",
	})
	if line != "Urashima attacks Salt Crab!":
		return "Placeholder substitution failed: %s" % line
	return ""


static func test_missing_key_returns_key() -> String:
	_lm().set_locale("en")
	var text: String = _lm().tr_key("nonexistent.key.xyz")
	if text != "nonexistent.key.xyz":
		return "Missing key should return key string, got: %s" % text
	return ""


static func test_vo_dialect_setting() -> String:
	_lm().set_locale("zh-Hant")
	_lm().set_vo_dialect("cmn")
	if _lm().get_vo_dialect() != "cmn":
		return "Expected vo_dialect cmn"
	var settings: Node = Engine.get_main_loop().root.get_node("SettingsManager")
	if settings.get_vo_dialect() != "cmn":
		return "SettingsManager should persist vo_dialect"
	_lm().set_vo_dialect("cant")
	_lm().set_locale("en")
	return ""
