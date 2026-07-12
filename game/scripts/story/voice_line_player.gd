extends RefCounted
class_name VoiceLinePlayer
## Resolves selective VO clip paths and playback hints from vo_prompts.json.


const VO_PROMPTS_PATH := "res://data/audio/vo_prompts.json"
const VOICE_ROOT := "res://assets/audio/voice"


static func voice_path(voice_id: String, locale: String, vo_dialect: String = "cant") -> String:
	if voice_id.is_empty():
		return ""
	if locale == "zh-Hant":
		var dialect := vo_dialect if vo_dialect in ["cant", "cmn"] else "cant"
		return "%s/zh-Hant/%s/%s.ogg" % [VOICE_ROOT, dialect, voice_id]
	return "%s/%s/%s.ogg" % [VOICE_ROOT, locale, voice_id]


static func clip_exists(voice_id: String, locale: String, vo_dialect: String = "cant") -> bool:
	var path := voice_path(voice_id, locale, vo_dialect)
	return path != "" and FileAccess.file_exists(path)


static func duck_bgm_db(voice_id: String) -> float:
	var spec := _clip_spec(voice_id)
	return float(spec.get("duck_bgm_db", -6.0))


static func _clip_spec(voice_id: String) -> Dictionary:
	if not FileAccess.file_exists(VO_PROMPTS_PATH):
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(VO_PROMPTS_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		return {}
	var clips: Variant = parsed.get("clips", {})
	if typeof(clips) != TYPE_DICTIONARY:
		return {}
	return clips.get(voice_id, {}) as Dictionary
