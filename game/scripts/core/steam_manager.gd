extends Node
## Steam API wrapper — no-ops when GodotSteam is not installed.

signal steam_ready

var available := false


func _ready() -> void:
	if Engine.has_singleton("Steam"):
		available = true
		steam_ready.emit()
		print("SteamManager: GodotSteam detected")
	else:
		print("SteamManager: running without Steam (dev/export scaffold)")


func unlock_achievement(api_name: String) -> void:
	if not available:
		return
	var steam = Engine.get_singleton("Steam")
	if steam and steam.has_method("setAchievement"):
		steam.setAchievement(api_name)
		if steam.has_method("storeStats"):
			steam.storeStats()


func on_flag_set(flag_id: String, value: Variant) -> void:
	var mapping := {
		"met_roku": "ACH_MET_ROKU",
		"shore_wraith_defeated": "ACH_SHORE_WRAITH",
		"sentinel_defeated": "ACH_SENTINEL",
		"tide_keeper_defeated": "ACH_TIDE_KEEPER",
	}
	if flag_id in mapping and value:
		unlock_achievement(mapping[flag_id])
	if flag_id == "ending_chosen":
		match str(value):
			"rewind":
				unlock_achievement("ACH_ENDING_REWIND")
			"anchor":
				unlock_achievement("ACH_ENDING_ANCHOR")
			"drift":
				unlock_achievement("ACH_ENDING_DRIFT")
