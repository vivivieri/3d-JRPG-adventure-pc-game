extends Node
## Global signals — autoload target (docs/TECHNICAL_DESIGN.md §2).
## Scene/UI systems connect here; no gameplay logic.

signal locale_changed(locale_code: String)
signal vo_dialect_changed(dialect_code: String)
signal hard_mode_changed(enabled: bool)
signal combat_started(encounter_id: String)
signal combat_ended(encounter_id: String, victory: bool)
signal flag_changed(flag_id: String, value: Variant)
signal save_slot_written(slot: int)
signal achievement_unlocked(achievement_id: String)
