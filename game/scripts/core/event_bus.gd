extends Node
## Global signal bus for decoupled systems.

signal game_state_changed(new_state: int)
signal story_flag_changed(flag: String, value: bool)
signal party_changed
signal dialogue_started(scene_id: String)
signal dialogue_line(line: Dictionary)
signal dialogue_finished(scene_id: String)
signal combat_started
signal combat_ended(victory: bool)
signal turn_started(actor: Node)
signal turn_ended(actor: Node)
signal damage_dealt(target: Node, amount: int, element: String)
signal actor_defeated(actor: Node)
signal quest_updated(quest_id: String)
signal ending_chosen(ending_id: String)
