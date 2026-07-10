extends Node
## Global signal bus for decoupled game systems.

signal flag_changed(flag_id: String, value: Variant)
signal quest_updated(quest_id: String)
signal party_changed
signal inventory_changed
signal gold_changed(amount: int)
signal zone_changed(zone_id: String)
signal dialogue_started(scene_id: String)
signal dialogue_finished(scene_id: String)
signal combat_started(encounter_id: String)
signal combat_finished(victory: bool)
signal scene_blocked_changed(blocked: bool)
signal lore_collected(lore_id: String)
signal game_saved
signal game_loaded
