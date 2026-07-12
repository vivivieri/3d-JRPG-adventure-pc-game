extends Node
## Global cross-system signals. Producers emit; consumers connect via .connect().


signal flag_changed(flag_name: String, value: Variant)
signal locale_changed(locale: String)
signal vo_dialect_changed(dialect: String)
signal zone_entered(zone_id: String)
signal combat_started(encounter_id: String)
signal combat_ended(victory: bool)
signal settings_changed()
