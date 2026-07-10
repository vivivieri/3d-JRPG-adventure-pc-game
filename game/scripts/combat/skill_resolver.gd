class_name SkillResolver
extends RefCounted
## Resolves skill effects, damage math, and elemental modifiers.

const WEAKNESS := 1.25
const RESIST := 0.75

const ELEMENT_MATRIX := {
	"water": { "spirit": WEAKNESS, "physical": RESIST },
	"spirit": { "water": WEAKNESS, "physical": RESIST },
	"physical": { "spirit": WEAKNESS },
}


static func get_element_modifier(attack_element: String, defender_element: String) -> float:
	if ELEMENT_MATRIX.has(attack_element):
		return ELEMENT_MATRIX[attack_element].get(defender_element, 1.0)
	return 1.0


static func resolve_damage(
	attacker: Combatant,
	defender: Combatant,
	skill: Dictionary
) -> int:
	if skill.get("power", 0.0) <= 0.0:
		return 0
	var stat_name: String = skill.get("power_stat", "atk")
	var attack_stat: int = attacker.atk if stat_name == "atk" else attacker.mag
	var defense_stat: int = defender.def if stat_name == "atk" else defender.res
	var pierce: float = skill.get("pierce_def", 0.0)
	var effective_def := int(defense_stat * (1.0 - pierce))
	var base := int(attack_stat * skill.get("power", 1.0)) - int(effective_def * 0.5)
	var modifier := get_element_modifier(skill.get("element", "physical"), defender.element)
	return maxi(1, int(base * modifier))


static func apply_skill_effects(
	attacker: Combatant,
	targets: Array,
	skill: Dictionary
) -> Array[String]:
	var messages: Array[String] = []
	for effect in skill.get("effects", []):
		var type: String = effect.get("type", "")
		if type == "heal":
			for t in targets:
				if t is Combatant:
					var healed: int = t.heal(effect.get("potency", 0))
					messages.append("%s heals %d HP." % [t.display_name, healed])
		elif type == "cleanse":
			for t in targets:
				if t is Combatant:
					t.statuses.clear()
					messages.append("%s is cleansed." % t.display_name)
		else:
			for t in targets:
				if t is Combatant and randf() <= effect.get("chance", 1.0):
					t.apply_status(effect)
					messages.append("%s is affected by %s." % [t.display_name, type])
	return messages


static func pick_enemy_skill(enemy: Combatant) -> String:
	var ai: Dictionary = enemy.ai_data
	if ai.is_empty():
		return enemy.skills[0] if enemy.skills.size() > 0 else "strike"
	var hp_ratio := float(enemy.hp) / float(enemy.max_hp)
	match ai.get("type", "weighted"):
		"phase":
			for phase in ai.get("phases", []):
				if hp_ratio > phase.get("hp_above", 0.0):
					return _weighted_pick(phase.get("weights", []), hp_ratio)
		"weighted", _:
			return _weighted_pick(ai.get("weights", []), hp_ratio)
	return enemy.skills[0] if enemy.skills.size() > 0 else "strike"


static func _weighted_pick(weights: Array, hp_ratio: float) -> String:
	var pool: Array[Dictionary] = []
	var total := 0
	for entry in weights:
		if entry.has("hp_below") and hp_ratio > entry.get("hp_below", 1.0):
			continue
		pool.append(entry)
		total += entry.get("weight", 0)
	if total == 0:
		return "strike"
	var roll := randi_range(1, total)
	var cumulative := 0
	for entry in pool:
		cumulative += entry.get("weight", 0)
		if roll <= cumulative:
			return entry.get("skill_id", "strike")
	return pool[0].get("skill_id", "strike")
