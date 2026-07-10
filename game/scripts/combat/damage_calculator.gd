extends RefCounted


static func physical_damage(attacker_atk: int, defender_def: int, power: float = 1.0, pierce: float = 0.0) -> int:
	var eff_def := int(defender_def * (1.0 - pierce))
	return max(1, int((attacker_atk * power) - eff_def * 0.5))


static func magic_damage(attacker_mag: int, defender_res: int, power: float = 1.0) -> int:
	return max(1, int((attacker_mag * power) - defender_res * 0.4))


static func flee_chance(party_spd: int, enemy_spd: int) -> float:
	return clamp(0.5 + (party_spd - enemy_spd) * 0.05, 0.2, 0.8)
