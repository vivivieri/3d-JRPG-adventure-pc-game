extends RefCounted
## Maps greybox markers to story actions per zone.

const INTERACTABLES := {
	"beach_shore": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-01", "once": true},
		"ToVillage": {"type": "zone", "zone": "ruined_village", "spawn": "WorldSpawn", "label": "Path to village"},
	},
	"ruined_village": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-02", "once": true},
		"InspectBanner": {"type": "dialogue", "scene": "SC-02-BANNER", "label": "Inspect banner"},
		"InspectSandal": {"type": "dialogue", "scene": "SC-02-SANDAL", "label": "Inspect sandal"},
		"VillageWell": {"type": "dialogue", "scene": "SC-02-WELL", "label": "Inspect well"},
		"ToriiShrine": {"type": "dialogue", "scene": "SC-03", "label": "Approach torii", "requires_not_scene": "SC-03"},
		"RokuShack": {"type": "dialogue", "scene": "SC-04", "label": "Enter shack", "requires_not_scene": "SC-04"},
		"RokuShop": {"type": "shop", "shop_id": "roku_shack", "label": "Browse wares", "requires_flag": "met_roku"},
		"TutorialEncounter": {"type": "encounter", "encounter": "enc_sc05_tutorial_crab", "label": "Fight Salt Crab", "requires_not_flag": "tutorial_combat_done"},
		"CaveEntrance": {"type": "zone", "zone": "tidal_caves", "spawn": "WorldSpawn", "label": "Enter caves", "requires_flag": "cave_entrance_unlocked"},
		"fishing_ledger": {"type": "lore", "lore": "fishing_ledger", "label": "Read ledger"},
		"festival_banner": {"type": "lore", "lore": "festival_banner", "label": "Read banner"},
		"yuzu_prayer": {"type": "lore", "lore": "yuzu_prayer", "label": "Read prayer slip"},
		"roku_dive_log": {"type": "lore", "lore": "roku_dive_log", "label": "Read dive log"},
		"VillageWellSave": {"type": "save", "label": "Save at well"},
	},
	"tidal_caves": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-06", "once": true},
		"CaveEntranceCrab": {"type": "encounter", "encounter": "enc_sc06_cave_crab", "label": "Salt Crab", "once": true},
		"WaterPuzzle": {"type": "puzzle", "label": "Water gate"},
		"FloodedChamberCrabs": {"type": "encounter", "encounter": "enc_sc07_optional_crabs", "label": "Optional crabs", "optional": true},
		"DeepPoolEncounter": {"type": "dialogue_then_encounter", "scene": "SC-08", "encounter": "enc_sc08_deep_pool", "label": "Deep pool"},
		"ShoreWraithBoss": {"type": "dialogue_then_encounter", "scene": "SC-09", "encounter": "enc_sc09_shore_wraith", "label": "Shore Wraith", "requires_not_flag": "shore_wraith_defeated"},
		"ShrineAlcove": {"type": "dialogue", "scene": "SC-10", "label": "Shrine alcove", "requires_flag": "shore_wraith_defeated", "requires_not_scene": "SC-10"},
		"PalaceVision": {"type": "dialogue", "scene": "SC-11", "label": "Palace vision", "requires_flag": "yuzu_joined", "requires_not_scene": "SC-11"},
		"ToPalace": {"type": "zone", "zone": "dragon_palace_gate", "spawn": "WorldSpawn", "label": "To palace gate", "requires_key_item": "wraith_pearl"},
		"ToVillage": {"type": "zone", "zone": "ruined_village", "spawn": "CaveEntrance", "label": "Return to village"},
		"cave_inscription": {"type": "lore", "lore": "cave_inscription", "label": "Read inscription"},
		"sailor_charm": {"type": "lore", "lore": "sailor_charm", "label": "Inspect charm"},
	},
	"dragon_palace_gate": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-12", "once": true, "requires_key_item": "wraith_pearl"},
		"GateApproachWraiths": {"type": "encounter", "encounter": "enc_sc12_palace_wraiths", "label": "Palace wraiths", "requires_flags": ["roku_combat_active", "yuzu_joined"], "once": true},
		"MirrorChamber": {"type": "dialogue", "scene": "SC-13", "label": "Mirror chamber", "requires_not_scene": "SC-13"},
		"PalaceSentinel": {"type": "dialogue_then_encounter", "scene": "SC-14", "encounter": "enc_sc14_sentinel", "label": "Palace Sentinel", "requires_not_flag": "sentinel_defeated"},
		"TideKeeperBoss": {"type": "dialogue_then_encounter", "scene": "SC-15", "encounter": "enc_sc15_tide_keeper", "label": "Tide Keeper", "requires_flag": "sentinel_defeated", "requires_not_flag": "tide_keeper_defeated"},
		"EndingChoice": {"type": "ending_choice", "label": "Face the tide", "requires_flag": "tide_keeper_phase3"},
		"palace_seal": {"type": "lore", "lore": "palace_seal", "label": "Read seal"},
		"otohime_letter": {"type": "lore", "lore": "otohime_letter", "label": "Read letter"},
	},
	"ending_rewind": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-17a", "once": true},
	},
	"ending_anchor": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-17b", "once": true},
	},
	"ending_drift": {
		"WorldSpawn": {"type": "auto_dialogue", "scene": "SC-17c", "once": true},
	},
	"beach_shore_extra": {},
}

const ZONE_TRANSITIONS := {
}

static func get_interactables(zone_id: String) -> Dictionary:
	return INTERACTABLES.get(zone_id, {})


static func get_zone_transitions(zone_id: String) -> Dictionary:
	return ZONE_TRANSITIONS.get(zone_id, {})
