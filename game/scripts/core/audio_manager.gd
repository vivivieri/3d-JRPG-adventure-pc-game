extends Node
## BGM/SFX playback with settings-aware buses.

const BGM_FIELD := "res://assets/audio/bgm/field.ogg"
const BGM_COMBAT := "res://assets/audio/bgm/combat.ogg"
const BGM_MENU := "res://assets/audio/bgm/menu.ogg"

var _bgm: AudioStreamPlayer
var _sfx: AudioStreamPlayer
var _current_bgm := ""


func _ready() -> void:
	_setup_buses()
	_bgm = AudioStreamPlayer.new()
	_bgm.name = "BGMPlayer"
	_bgm.bus = "Music"
	add_child(_bgm)
	_sfx = AudioStreamPlayer.new()
	_sfx.name = "SFXPlayer"
	_sfx.bus = "SFX"
	add_child(_sfx)
	EventBus.zone_changed.connect(_on_zone_changed)
	EventBus.combat_started.connect(_on_combat_started)
	EventBus.combat_finished.connect(_on_combat_finished)
	call_deferred("_apply_volumes")


func _setup_buses() -> void:
	if AudioServer.get_bus_index("Music") == -1:
		AudioServer.add_bus()
		AudioServer.set_bus_name(AudioServer.bus_count - 1, "Music")
	if AudioServer.get_bus_index("SFX") == -1:
		AudioServer.add_bus()
		AudioServer.set_bus_name(AudioServer.bus_count - 1, "SFX")
	_apply_volumes()


func _apply_volumes() -> void:
	var master := SettingsManager.master_volume if SettingsManager else 0.8
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), linear_to_db(master))
	var music_idx := AudioServer.get_bus_index("Music")
	if music_idx >= 0:
		var music := SettingsManager.music_volume if SettingsManager else 0.7
		AudioServer.set_bus_volume_db(music_idx, linear_to_db(music * master))
	var sfx_idx := AudioServer.get_bus_index("SFX")
	if sfx_idx >= 0:
		var sfx := SettingsManager.sfx_volume if SettingsManager else 0.8
		AudioServer.set_bus_volume_db(sfx_idx, linear_to_db(sfx * master))


func play_bgm(path: String, restart: bool = false) -> void:
	if path == "" or (path == _current_bgm and _bgm.playing and not restart):
		return
	if not ResourceLoader.exists(path):
		return
	_current_bgm = path
	_bgm.stream = load(path)
	_bgm.play()


func stop_bgm() -> void:
	_bgm.stop()
	_current_bgm = ""


func play_sfx(kind: String) -> void:
	var path := "res://assets/audio/sfx/%s.ogg" % kind
	if not ResourceLoader.exists(path):
		return
	_sfx.stream = load(path)
	_sfx.play()


func _on_zone_changed(zone_id: String) -> void:
	if zone_id.begins_with("ending_"):
		play_bgm(BGM_FIELD)
	else:
		play_bgm(BGM_FIELD)


func _on_combat_started(_encounter_id: String) -> void:
	play_bgm(BGM_COMBAT, true)


func _on_combat_finished(_victory: bool) -> void:
	play_bgm(BGM_FIELD, true)
	if _victory:
		play_sfx("victory")
