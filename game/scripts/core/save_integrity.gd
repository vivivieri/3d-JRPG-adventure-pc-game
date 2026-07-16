extends RefCounted
class_name SaveIntegrity
## HMAC save-slot integrity — wire from SaveSystem (docs/SECURITY.md §9).
## Reference until SaveSystem lands on game/development.

const INTEGRITY_FIELD := "_integrity"
const DEV_PEPPER := "dev-pepper-not-for-ship"
const PROJECT_PEPPER_KEY := "application/config/save_hmac_pepper"


static func pepper() -> String:
	if ProjectSettings.has_setting(PROJECT_PEPPER_KEY):
		var value: String = str(ProjectSettings.get_setting(PROJECT_PEPPER_KEY))
		if not value.is_empty():
			return value
	return DEV_PEPPER


static func canonical_json(save: Dictionary) -> String:
	var payload := {}
	var fields: PackedStringArray = [
		"version",
		"timestamp",
		"scene",
		"spawn_marker",
		"flags",
		"party",
		"inventory",
		"quests",
		"encounters_completed",
		"lore_read",
		"chests_opened",
		"tutorial_seen",
		"run_ending",
	]
	for field in fields:
		if save.has(field):
			payload[field] = save[field]
	return JSON.stringify(payload)


static func _hmac_sha256_hex(key: String, message: String) -> String:
	var ctx := HMACContext.new()
	ctx.start(HashingContext.HASH_SHA256, key.to_utf8_buffer())
	ctx.update(message.to_utf8_buffer())
	return ctx.finish().hex_encode()


static func sign(save: Dictionary, pepper_override: String = "") -> String:
	var key := pepper_override if not pepper_override.is_empty() else pepper()
	return _hmac_sha256_hex(key, canonical_json(save))


static func attach(save: Dictionary, pepper_override: String = "") -> Dictionary:
	var out := save.duplicate(true)
	out.erase(INTEGRITY_FIELD)
	out[INTEGRITY_FIELD] = sign(out, pepper_override)
	return out


static func verify(save: Dictionary, pepper_override: String = "") -> bool:
	if not save.has(INTEGRITY_FIELD):
		return false
	var expected: String = str(save[INTEGRITY_FIELD])
	var copy := save.duplicate(true)
	copy.erase(INTEGRITY_FIELD)
	var actual := sign(copy, pepper_override)
	return expected == actual
