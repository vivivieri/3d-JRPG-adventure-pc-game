extends Node
## Steam API wrapper — uses GodotSteam when the GDExtension is present.


signal steam_ready

var is_available := false
var steam_id: int = 0

const ACHIEVEMENTS := {
	"met_roku": "ACH_MET_ROKU",
	"shore_wraith_defeated": "ACH_SHORE_WRAITH",
	"sentinel_defeated": "ACH_SENTINEL",
	"tide_keeper_defeated": "ACH_TIDE_KEEPER",
	"ending_rewind": "ACH_ENDING_REWIND",
	"ending_anchor": "ACH_ENDING_ANCHOR",
	"ending_drift": "ACH_ENDING_DRIFT",
}


func _ready() -> void:
	if Engine.has_singleton("Steam"):
		_init_steam()
	else:
		print("[Steam] GodotSteam not loaded — running in offline mode.")
	EventBus.story_flag_changed.connect(_on_flag_changed)


func _init_steam() -> void:
	var steam: Object = Engine.get_singleton("Steam")
	var restart := false
	if steam.has_method("steamInitEx"):
		var init_result: Dictionary = steam.steamInitEx()
		is_available = init_result.get("status", 0) == 1
		restart = init_result.get("verbal", "") == "Steam game server needs restart"
	elif steam.has_method("steamInit"):
		is_available = steam.steamInit()
	if restart and steam.has_method("restartAppIfNecessary"):
		steam.restartAppIfNecessary(480)
		get_tree().quit()
	if is_available and steam.has_method("getSteamID"):
		steam_id = steam.getSteamID()
		steam_ready.emit()
		print("[Steam] Initialized. SteamID=%s" % steam_id)


func unlock_achievement(achievement_api_name: String) -> void:
	if not is_available or not Engine.has_singleton("Steam"):
		return
	var steam: Object = Engine.get_singleton("Steam")
	if steam.has_method("setAchievement") and steam.has_method("storeStats"):
		if steam.setAchievement(achievement_api_name):
			steam.storeStats()


func _on_flag_changed(flag: String, value: bool) -> void:
	if not value:
		return
	if ACHIEVEMENTS.has(flag):
		unlock_achievement(ACHIEVEMENTS[flag])
	if flag.begins_with("ending_"):
		unlock_achievement(ACHIEVEMENTS.get(flag, ""))
