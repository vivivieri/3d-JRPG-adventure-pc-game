extends CanvasLayer
## Compact quest objective display (top-left).


@onready var _panel: PanelContainer = $Panel
@onready var _title: Label = $Panel/Margin/VBox/TitleLabel
@onready var _stage: Label = $Panel/Margin/VBox/StageLabel
@onready var _progress: Label = $Panel/Margin/VBox/ProgressLabel


func _ready() -> void:
	layer = 3
	_panel.visible = false
	EventBus.quest_tracker_changed.connect(_refresh)
	EventBus.game_state_changed.connect(func(_s): _refresh())
	EventBus.locale_changed.connect(_on_locale_changed)
	call_deferred("_refresh")


func _refresh() -> void:
	var data := QuestTracker.get_hud_data()
	if data.is_empty():
		_panel.visible = false
		return
	_panel.visible = GameManager.state == GameManager.GameState.EXPLORATION
	_title.text = data.get("title", "")
	_stage.text = data.get("stage_text", "")
	var idx: int = data.get("stage_index", 0)
	var total: int = data.get("stage_total", 0)
	_progress.text = LocalizationManager.tr_key("UI_QUEST_PROGRESS", { "current": idx, "total": total })
	FontThemeManager.apply_to_control(_panel)


func _on_locale_changed(_locale: String) -> void:
	_refresh()
