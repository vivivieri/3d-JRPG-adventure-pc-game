class_name ItemEffectResolver
extends RefCounted
## Shared consumable effect resolution for battle and field.


static func apply_to_stats(stats: Dictionary, item_def: Dictionary) -> Dictionary:
	var effect: Dictionary = item_def.get("effect", {})
	var result := {
		"success": false,
		"message_key": "",
		"message_args": {},
		"healed_hp": 0,
		"restored_mp": 0,
		"cured_status": "",
	}
	match effect.get("type", ""):
		"heal_hp":
			var before: int = stats.get("hp", 0)
			var max_hp: int = stats.get("max_hp", before)
			stats["hp"] = mini(before + effect.get("value", 0), max_hp)
			result.healed_hp = stats["hp"] - before
			result.success = result.healed_hp > 0
			result.message_key = "field.item_heal_hp"
		"heal_mp":
			var before_mp: int = stats.get("mp", 0)
			var max_mp: int = stats.get("max_mp", before_mp)
			stats["mp"] = mini(before_mp + effect.get("value", 0), max_mp)
			result.restored_mp = stats["mp"] - before_mp
			result.success = result.restored_mp > 0
			result.message_key = "field.item_heal_mp"
		"cure_status":
			var status_type: String = effect.get("status", "poison")
			if status_type in statuses:
				statuses.erase(status_type)
				stats["statuses"] = statuses
				result.cured_status = status_type
				result.success = true
				result.message_key = "field.item_cure"
			else:
				result.message_key = "field.item_no_effect"
	return result
