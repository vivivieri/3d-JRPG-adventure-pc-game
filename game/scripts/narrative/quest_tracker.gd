extends Node
## Tracks active quest stages from story flags and quest start events.


var active_quests: Array[String] = []
var completed_quests: Array[String] = []


func _ready() -> void:
	EventBus.quest_updated.connect(_on_quest_updated)
	EventBus.story_flag_changed.connect(_on_flag_changed)


func restore(saved_active: Array, saved_completed: Array) -> void:
	active_quests.clear()
	completed_quests.clear()
	for q in saved_active:
		active_quests.append(str(q))
	for q in saved_completed:
		completed_quests.append(str(q))
	_refresh_all_quests()


func get_snapshot() -> Dictionary:
	return {
		"active_quests": active_quests.duplicate(),
		"completed_quests": completed_quests.duplicate(),
	}


func get_hud_data() -> Dictionary:
	for quest_id in active_quests:
		if quest_id in completed_quests:
			continue
		var stage := _get_current_stage(quest_id)
		if stage.is_empty():
			continue
		return {
			"quest_id": quest_id,
			"title": LocalizationManager.quest_title(quest_id),
			"stage_id": stage.get("id", ""),
			"stage_text": LocalizationManager.quest_stage_description(quest_id, stage.get("id", "")),
			"stage_index": stage.get("index", 0),
			"stage_total": stage.get("total", 1),
		}
	return {}


func _on_quest_updated(quest_id: String) -> void:
	if quest_id.is_empty():
		return
	if quest_id not in active_quests and quest_id not in completed_quests:
		active_quests.append(quest_id)
	EventBus.quest_tracker_changed.emit()


func _on_flag_changed(_flag: String, _value: bool) -> void:
	_refresh_all_quests()


func _refresh_all_quests() -> void:
	var changed := false
	for quest_id in active_quests.duplicate():
		if _is_quest_complete(quest_id) and quest_id not in completed_quests:
			completed_quests.append(quest_id)
			changed = true
	if changed:
		EventBus.quest_tracker_changed.emit()


func _is_quest_complete(quest_id: String) -> bool:
	var quest := _find_quest(quest_id)
	if quest.is_empty():
		return true
	for stage in quest.get("stages", []):
		var flag: String = stage.get("completion", {}).get("flag", "")
		if not flag.is_empty() and not GameManager.has_flag(flag):
			return false
	return true


func _get_current_stage(quest_id: String) -> Dictionary:
	var quest := _find_quest(quest_id)
	var stages: Array = quest.get("stages", [])
	for i in stages.size():
		var stage: Dictionary = stages[i]
		var flag: String = stage.get("completion", {}).get("flag", "")
		if flag.is_empty() or not GameManager.has_flag(flag):
			return { "id": stage.get("id", ""), "index": i + 1, "total": stages.size() }
	return {}


func _find_quest(quest_id: String) -> Dictionary:
	var data: Dictionary = GameManager.get_data("quests")
	for quest in data.get("quests", []):
		if quest.get("id") == quest_id:
			return quest
	return {}
