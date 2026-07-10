extends Node3D
## Field gameplay layer — player, camera, interactables, zone story hooks.

const ZoneContentLib = preload("res://scripts/world/zone_content.gd")
const PLAYER_SCENE = preload("res://scenes/player/player.tscn")

@export var zone_id: String = "ruined_village"

var _player: CharacterBody3D = null
var _camera_rig: Node3D = null
var _markers: Dictionary = {}
var _blocked := false
var _nearest: String = ""
var _hud: Node = null


func _ready() -> void:
	add_to_group("field_controller")
	_cache_markers()
	_spawn_player()
	_spawn_lore_markers()
	_connect_events()
	call_deferred("_on_zone_enter")


func _connect_events() -> void:
	EventBus.scene_blocked_changed.connect(_on_blocked)
	EventBus.dialogue_finished.connect(_on_dialogue_finished)
	CombatManager.battle_ended.connect(_on_battle_ended)


func _cache_markers() -> void:
	_markers.clear()
	var greybox := get_parent().get_node_or_null("Greybox")
	if greybox:
		for child in greybox.get_children():
			if child is Marker3D:
				_markers[child.name] = child


func _spawn_player() -> void:
	_player = PLAYER_SCENE.instantiate()
	add_child(_player)
	_camera_rig = Node3D.new()
	_camera_rig.name = "CameraRig"
	_camera_rig.set_script(load("res://scripts/player/player_camera_rig.gd"))
	add_child(_camera_rig)
	_camera_rig.set_target(_player)
	var spawn_name := GameManager.pending_spawn if GameManager.pending_spawn != "" else "WorldSpawn"
	spawn_at_marker(spawn_name)
	GameManager.pending_spawn = ""


func spawn_at_marker(marker_name: String) -> void:
	if not _player:
		return
	var marker: Marker3D = _markers.get(marker_name, _markers.get("WorldSpawn"))
	if marker:
		_player.global_position = marker.global_position + Vector3(0, 0.5, 0)


func _spawn_lore_markers() -> void:
	for placement in GameManager.lore_placements:
		if placement.zone != zone_id:
			continue
		var m := Marker3D.new()
		m.name = str(placement.id)
		var pos: Array = placement.position
		m.position = Vector3(pos[0], pos[1], pos[2])
		var greybox := get_parent().get_node_or_null("Greybox")
		if greybox:
			greybox.add_child(m)
		_markers[m.name] = m


func _on_zone_enter() -> void:
	GameManager.current_zone = zone_id
	EventBus.zone_changed.emit(zone_id)
	_ensure_hud()
	_set_field_blocked(DialogueRunner.is_active())
	if GameManager.pending_dialogue != "":
		var scene := GameManager.pending_dialogue
		GameManager.pending_dialogue = ""
		DialogueRunner.play(scene)
		return
	call_deferred("_try_auto_events")


func _set_field_blocked(on: bool) -> void:
	_blocked = on
	if _player and _player.has_method("set_enabled"):
		_player.set_enabled(not on)
	if not on and _player:
		get_viewport().gui_release_focus()
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func _ensure_hud() -> void:
	if _hud:
		return
	var existing := get_tree().root.get_node_or_null("FieldHUD")
	if existing:
		_hud = existing
		return
	var packed := preload("res://scenes/ui/field_hud.tscn")
	_hud = packed.instantiate()
	_hud.name = "FieldHUD"
	get_tree().root.add_child(_hud)


func _try_auto_events() -> void:
	for key in ZoneContentLib.get_interactables(zone_id):
		var data: Dictionary = ZoneContentLib.get_interactables(zone_id)[key]
		if data.get("type", "") != "auto_dialogue":
			continue
		if data.get("once", false) and GameManager.scene_done(str(data.scene)):
			continue
		if _player and _markers.has(key):
			if _player.global_position.distance_to(_markers[key].global_position) < 20.0:
				_trigger_interact(key, data)
				return
	# Also check zone transitions on beach
	for key in ZoneContentLib.get_zone_transitions(zone_id):
		pass


func _process(_delta: float) -> void:
	if _blocked or not _player:
		return
	_update_nearest()


func _update_nearest() -> void:
	_nearest = ""
	var best_dist := 2.8
	var defs: Dictionary = ZoneContentLib.get_interactables(zone_id)
	for key in defs:
		if not _markers.has(key):
			continue
		if not _can_use(defs[key]):
			continue
		var dist := _player.global_position.distance_to(_markers[key].global_position)
		if dist < best_dist:
			best_dist = dist
			_nearest = key
	if _hud and _hud.has_method("set_prompt"):
		var label := ""
		if _nearest != "":
			var d: Dictionary = defs.get(_nearest, {})
			label = str(d.get("label", "Interact"))
		_hud.set_prompt(label)


func _unhandled_input(event: InputEvent) -> void:
	if _blocked:
		return
	if event.is_action_pressed("interact") and _nearest != "":
		var defs: Dictionary = ZoneContentLib.get_interactables(zone_id)
		var data: Dictionary = defs.get(_nearest, {})
		_trigger_interact(_nearest, data)


func _can_use(data: Dictionary) -> bool:
	if data.get("requires_flag", "") != "" and not GameManager.has_flag(str(data.requires_flag)):
		return false
	if data.has("requires_flags"):
		for f in data.requires_flags:
			if not GameManager.has_flag(str(f)):
				return false
	if data.get("requires_not_flag", "") != "" and GameManager.has_flag(str(data.requires_not_flag)):
		return false
	if data.get("requires_not_scene", "") != "" and GameManager.scene_done(str(data.requires_not_scene)):
		return false
	if data.get("requires_key_item", "") != "" and not GameManager.has_key_item(str(data.requires_key_item)):
		return false
	if data.get("once", false) and data.has("encounter"):
		var enc: Dictionary = GameManager.encounters.get(str(data.encounter), {})
		var sid := str(enc.get("scene_id", data.encounter))
		if GameManager.scene_done(sid):
			return false
	return true


func _trigger_interact(marker_name: String, data: Dictionary) -> void:
	if not _can_use(data):
		return
	match data.get("type", ""):
		"dialogue", "auto_dialogue":
			DialogueRunner.play(str(data.scene))
		"encounter":
			_start_encounter(str(data.encounter))
		"dialogue_then_encounter":
			DialogueRunner.play(str(data.scene))
			_pending_encounter = str(data.encounter)
		"zone":
			GameManager.pending_spawn = str(data.get("spawn", "WorldSpawn"))
			GameManager.go_to_zone(str(data.zone))
		"lore":
			_show_lore(str(data.lore))
		"save":
			SaveSystem.save_game()
			if _hud and _hud.has_method("toast"):
				_hud.toast("Game saved.")
		"puzzle":
			_open_puzzle()
		"ending_choice":
			_open_ending_choice()


var _pending_encounter := ""


func _show_lore(lore_id: String) -> void:
	var entry: Dictionary = GameManager.lore_entries.get(lore_id, {})
	if entry.is_empty():
		return
	GameManager.collect_lore(lore_id)
	_blocked = true
	if _hud and _hud.has_method("show_lore_popup"):
		_hud.show_lore_popup(entry, _on_lore_closed)


func _on_lore_closed() -> void:
	_blocked = false


func _open_puzzle() -> void:
	_blocked = true
	if _hud and _hud.has_method("open_water_puzzle"):
		_hud.open_water_puzzle(_on_puzzle_solved)


func _on_puzzle_solved() -> void:
	_blocked = false
	GameManager.set_flag("water_puzzle_solved")
	GameManager.add_item("tide_cut_saber", 1)
	GameManager.mark_scene_done("SC-07")


func _open_ending_choice() -> void:
	_blocked = true
	if _hud and _hud.has_method("open_ending_choice"):
		_hud.open_ending_choice()


func _start_encounter(encounter_id: String) -> void:
	_blocked = true
	if _player and _player.has_method("set_enabled"):
		_player.set_enabled(false)
	CombatManager.start_encounter(encounter_id)


func _on_blocked(on: bool) -> void:
	_set_field_blocked(on)


func _on_dialogue_finished(_scene_id: String) -> void:
	_set_field_blocked(false)
	if GameManager.pending_dialogue != "":
		var scene := GameManager.pending_dialogue
		GameManager.pending_dialogue = ""
		DialogueRunner.play(scene)
		return
	if GameManager.has_flag("game_completed"):
		get_tree().change_scene_to_file("res://scenes/ui/credits.tscn")
		return
	if _pending_encounter != "":
		var enc := _pending_encounter
		_pending_encounter = ""
		_start_encounter(enc)
		return
	call_deferred("_try_auto_events")


func _on_battle_ended(_victory: bool) -> void:
	_set_field_blocked(false)
