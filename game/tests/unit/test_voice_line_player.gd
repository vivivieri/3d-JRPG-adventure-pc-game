class_name TestVoiceLinePlayer
extends RefCounted
## Unit tests — VoiceLinePlayer path resolution (no .ogg files required).

const VoiceLinePlayerScript := preload("res://scripts/story/voice_line_player.gd")


static func test_en_locale_path() -> String:
	var path: String = VoiceLinePlayerScript.voice_path("sc03_yuzu_01", "en")
	if path != "res://assets/audio/voice/en/sc03_yuzu_01.ogg":
		return "Expected en path, got: %s" % path
	return ""


static func test_ja_locale_path() -> String:
	var path := VoiceLinePlayerScript.voice_path("sc03_yuzu_01", "ja")
	if path != "res://assets/audio/voice/ja/sc03_yuzu_01.ogg":
		return "Expected ja path, got: %s" % path
	return ""


static func test_zh_hant_cant_path() -> String:
	var path := VoiceLinePlayerScript.voice_path("sc03_yuzu_01", "zh-Hant", "cant")
	if path != "res://assets/audio/voice/zh-Hant/cant/sc03_yuzu_01.ogg":
		return "Expected zh-Hant/cant path, got: %s" % path
	return ""


static func test_zh_hant_cmn_path() -> String:
	var path := VoiceLinePlayerScript.voice_path("sc03_yuzu_01", "zh-Hant", "cmn")
	if path != "res://assets/audio/voice/zh-Hant/cmn/sc03_yuzu_01.ogg":
		return "Expected zh-Hant/cmn path, got: %s" % path
	return ""


static func test_empty_voice_id() -> String:
	var path := VoiceLinePlayerScript.voice_path("", "en")
	if path != "":
		return "Empty voice_id should return empty path"
	return ""


static func test_invalid_dialect_falls_back_to_cant() -> String:
	var path := VoiceLinePlayerScript.voice_path("sc03_yuzu_01", "zh-Hant", "invalid")
	if path != "res://assets/audio/voice/zh-Hant/cant/sc03_yuzu_01.ogg":
		return "Invalid dialect should fall back to cant, got: %s" % path
	return ""
