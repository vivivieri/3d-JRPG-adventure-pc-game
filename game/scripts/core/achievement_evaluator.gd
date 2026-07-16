extends RefCounted
class_name AchievementEvaluator
## Evaluate achievement triggers from game/data/achievements/achievements.json.

static func trigger_met(
	trigger: Dictionary,
	flags: Dictionary,
	settings: Dictionary,
	profile_meta: Dictionary,
) -> bool:
	if trigger.is_empty():
		return false

	if trigger.has("flag"):
		if not bool(flags.get(str(trigger["flag"]), false)):
			return false
		var setting_key = trigger.get("setting")
		if setting_key != null and not bool(settings.get(str(setting_key), false)):
			return false
		return true

	if trigger.has("all_flags"):
		for fl in trigger["all_flags"]:
			if not bool(flags.get(str(fl), false)):
				return false
		return true

	if trigger.has("flag_equals"):
		for fk in trigger["flag_equals"].keys():
			if str(flags.get(str(fk), "")) != str(trigger["flag_equals"][fk]):
				return false
		return true

	if trigger.has("meta_endings_count"):
		var endings: Array = profile_meta.get("endings_unlocked", [])
		return endings.size() >= int(trigger["meta_endings_count"])

	if trigger.has("lore_count"):
		return int(profile_meta.get("lore_count", 0)) >= int(trigger["lore_count"])

	return false


static func evaluate_catalog(
	achievements: Array,
	flags: Dictionary,
	settings: Dictionary,
	profile_meta: Dictionary,
) -> Array[String]:
	var unlocked: Array[String] = []
	for ach in achievements:
		if typeof(ach) != TYPE_DICTIONARY:
			continue
		var trig: Dictionary = ach.get("trigger", {})
		if trigger_met(trig, flags, settings, profile_meta):
			unlocked.append(str(ach.get("id", "")))
	return unlocked
