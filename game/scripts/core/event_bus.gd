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
signal combat_escaped
signal combat_log_appended(message: String)
signal combat_stats_changed
signal turn_started(actor_data: Dictionary)
signal turn_ended(actor_data: Dictionary)
signal enemy_intent_shown(enemy_id: String, skill_id: String, intent_key: String)
signal boss_phase_announced(enemy_id: String, message: String)
signal boss_choice_required(enemy_id: String)
signal damage_dealt(target_id: String, amount: int, element: String)
signal actor_defeated(actor_id: String)
signal quest_updated(quest_id: String)
signal ending_chosen(ending_id: String)
signal field_item_used(character_id: String, item_id: String)
signal equipment_changed(character_id: String)
signal quest_tracker_changed
signal save_message(message: String)
signal locale_changed(locale_code: String)
