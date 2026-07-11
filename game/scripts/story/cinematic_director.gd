extends Node
## Plays data-driven cinematic hooks from story/cinematic_hooks.json.
## Zone triggers call play_hook(); then-chain hands off to DialogueRunner / CombatManager (Phase 2+).

signal cinematic_started(hook_id: String, scene_id: String)
signal cinematic_finished(hook_id: String, skipped: bool)
signal then_step_requested(step: Dictionary)

const HOOKS_PATH := "res://data/story/cinematic_hooks.json"

var _hooks_by_id: Dictionary = {}
var _playing := false


func _ready() -> void:
	_load_hooks()


func _load_hooks() -> void:
	_hooks_by_id.clear()
	if not FileAccess.file_exists(HOOKS_PATH):
		push_error("CinematicDirector: missing %s" % HOOKS_PATH)
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(HOOKS_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("CinematicDirector: invalid JSON in %s" % HOOKS_PATH)
		return
	for hook: Variant in parsed.get("hooks", []):
		if typeof(hook) != TYPE_DICTIONARY:
			continue
		var hook_id: String = str(hook.get("id", ""))
		if hook_id.is_empty():
			continue
		_hooks_by_id[hook_id] = hook


func get_hook(hook_id: String) -> Dictionary:
	return _hooks_by_id.get(hook_id, {}) as Dictionary


func list_hooks_for_zone(zone_id: String) -> Array[String]:
	var out: Array[String] = []
	for hook_id: String in _hooks_by_id.keys():
		var hook: Dictionary = _hooks_by_id[hook_id]
		if str(hook.get("zone", "")) == zone_id:
			out.append(hook_id)
	out.sort()
	return out


func can_play(hook_id: String, flags: Dictionary, inventory: Array = []) -> bool:
	if _playing:
		return false
	var hook := get_hook(hook_id)
	if hook.is_empty():
		return false
	var skip_flag: String = str(hook.get("skip_if_flag", ""))
	if not skip_flag.is_empty() and _flag_true(flags, skip_flag):
		return false
	if not _requirements_met(hook.get("requires_flags", {}), flags):
		return false
	for item_id: Variant in hook.get("requires_items", []):
		if str(item_id) not in inventory:
			return false
	return true


func should_skip_immediately(hook_id: String, flags: Dictionary) -> bool:
	var hook := get_hook(hook_id)
	if hook.is_empty():
		return true
	var skip_flag: String = str(hook.get("skip_if_flag", ""))
	return not skip_flag.is_empty() and _flag_true(flags, skip_flag)


func play_hook(
	hook_id: String,
	flags: Dictionary,
	inventory: Array = [],
	flag_setter: Callable = Callable(),
	skipped: bool = false
) -> void:
	var hook := get_hook(hook_id)
	if hook.is_empty():
		push_warning("CinematicDirector: unknown hook %s" % hook_id)
		_emit_then_chain(hook_id, hook, skipped)
		return

	_playing = true
	var scene_id: String = str(hook.get("scene_id", ""))
	cinematic_started.emit(hook_id, scene_id)

	if not skipped:
		for flag_name: Variant in hook.get("sets_flags", []):
			_apply_flag(flag_setter, str(flag_name), true)

	_playing = false
	cinematic_finished.emit(hook_id, skipped)
	_emit_then_chain(hook_id, hook, skipped)


func run_then_chain(hook_id: String) -> Array[Dictionary]:
	var hook := get_hook(hook_id)
	var steps: Array[Dictionary] = []
	if hook.is_empty():
		return steps
	for step: Variant in hook.get("then", []):
		if typeof(step) == TYPE_DICTIONARY:
			steps.append(step)
	return steps


func _emit_then_chain(hook_id: String, hook: Dictionary, skipped: bool) -> void:
	for step: Dictionary in run_then_chain(hook_id):
		var payload := step.duplicate()
		payload["hook_id"] = hook_id
		payload["scene_id"] = str(hook.get("scene_id", ""))
		payload["cinematic_skipped"] = skipped
		then_step_requested.emit(payload)


func _requirements_met(requirements: Variant, flags: Dictionary) -> bool:
	if typeof(requirements) != TYPE_DICTIONARY:
		return true
	for key: Variant in requirements.keys():
		if not _flag_equals(flags, str(key), requirements[key]):
			return false
	return true


func _flag_true(flags: Dictionary, flag_name: String) -> bool:
	return _flag_equals(flags, flag_name, true)


func _flag_equals(flags: Dictionary, flag_name: String, expected: Variant) -> bool:
	if not flags.has(flag_name):
		return false
	return flags[flag_name] == expected


func _apply_flag(flag_setter: Callable, flag_name: String, value: Variant) -> void:
	if flag_setter.is_valid():
		flag_setter.call(flag_name, value)
