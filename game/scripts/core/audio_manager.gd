extends Node
## BGM crossfade and SFX playback. Hooks into EventBus and zone changes.


const BGM := {
	"main_menu": "res://assets/audio/bgm/menu.ogg",
	"beach_shore": "res://assets/audio/bgm/village.ogg",
	"ruined_village": "res://assets/audio/bgm/village.ogg",
	"tidal_caves": "res://assets/audio/bgm/caves.ogg",
	"dragon_palace_gate": "res://assets/audio/bgm/palace.ogg",
	"combat": "res://assets/audio/bgm/combat.ogg",
	"boss": "res://assets/audio/bgm/boss.ogg",
}

const SFX := {
	"ui_confirm": "res://assets/audio/sfx/ui_confirm.ogg",
	"ui_cancel": "res://assets/audio/sfx/ui_cancel.ogg",
	"interact": "res://assets/audio/sfx/interact.ogg",
	"heal": "res://assets/audio/sfx/heal.ogg",
	"victory": "res://assets/audio/sfx/victory.ogg",
	"defeat": "res://assets/audio/sfx/defeat.ogg",
	"hit": "res://assets/audio/sfx/hit.ogg",
	"footstep": "res://assets/audio/sfx/footstep.ogg",
	"item": "res://assets/audio/sfx/item.ogg",
	"equip": "res://assets/audio/sfx/equip.ogg",
}

const FADE_SEC := 1.2

var _bgm_a: AudioStreamPlayer
var _bgm_b: AudioStreamPlayer
var _use_a := true
var _current_bgm := ""
var _sfx_players: Array[AudioStreamPlayer] = []
var _footstep_cooldown := 0.0


func _ready() -> void:
	_bgm_a = _make_bgm_player()
	_bgm_b = _make_bgm_player()
	add_child(_bgm_a)
	add_child(_bgm_b)
	for i in 4:
		var p := AudioStreamPlayer.new()
		p.bus = "SFX"
		add_child(p)
		_sfx_players.append(p)
	EventBus.combat_started.connect(_on_combat_started)
	EventBus.combat_ended.connect(_on_combat_ended)
	EventBus.combat_escaped.connect(_on_combat_escaped)
	EventBus.damage_dealt.connect(_on_damage_dealt)
	EventBus.game_state_changed.connect(_on_game_state_changed)


func _process(delta: float) -> void:
	_footstep_cooldown = maxf(0.0, _footstep_cooldown - delta)


func play_bgm(track_key: String) -> void:
	if track_key == _current_bgm:
		return
	var path: String = BGM.get(track_key, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		return
	_current_bgm = track_key
	var stream: AudioStream = load(path)
	stream.loop = true
	var outgoing := _bgm_a if _use_a else _bgm_b
	var incoming := _bgm_b if _use_a else _bgm_a
	_use_a = not _use_a
	incoming.stream = stream
	incoming.volume_db = -80.0
	incoming.play()
	var tween := create_tween()
	tween.set_parallel(true)
	tween.tween_property(incoming, "volume_db", 0.0, FADE_SEC)
	if outgoing.playing:
		tween.tween_property(outgoing, "volume_db", -80.0, FADE_SEC)
		tween.chain().tween_callback(outgoing.stop)


func play_sfx(sfx_key: String) -> void:
	var path: String = SFX.get(sfx_key, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		return
	var player := _next_sfx_player()
	player.stream = load(path)
	player.play()


func play_footstep() -> void:
	if _footstep_cooldown > 0.0:
		return
	_footstep_cooldown = 0.32
	play_sfx("footstep")


func _make_bgm_player() -> AudioStreamPlayer:
	var p := AudioStreamPlayer.new()
	p.bus = "BGM"
	return p


func _next_sfx_player() -> AudioStreamPlayer:
	for p in _sfx_players:
		if not p.playing:
			return p
	return _sfx_players[0]


func _sync_zone_bgm() -> void:
	if GameManager.state == GameManager.GameState.COMBAT:
		return
	var area := GameManager.current_area
	if BGM.has(area):
		play_bgm(area)


func _on_combat_started() -> void:
	var track := "boss" if CombatManager.is_boss_battle() else "combat"
	play_bgm(track)


func _on_combat_ended(victory: bool) -> void:
	play_sfx("victory" if victory else "defeat")
	call_deferred("_sync_zone_bgm")


func _on_combat_escaped() -> void:
	call_deferred("_sync_zone_bgm")


func _on_damage_dealt(_target_id: String, amount: int, _element: String) -> void:
	if amount > 0:
		play_sfx("hit")


func _on_game_state_changed(new_state: int) -> void:
	if new_state == GameManager.GameState.EXPLORATION:
		call_deferred("_sync_zone_bgm")
