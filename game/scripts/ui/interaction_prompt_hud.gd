extends CanvasLayer
## Shows "Press E — {action}" when the player focuses an interactable.

@onready var _panel: PanelContainer = $PromptPanel
@onready var _key_label: Label = $PromptPanel/Margin/HBox/KeyLabel
@onready var _separator_label: Label = $PromptPanel/Margin/HBox/SeparatorLabel
@onready var _action_label: Label = $PromptPanel/Margin/HBox/ActionLabel

var _current_action := ""


func _ready() -> void:
	layer = 9
	_panel.visible = false
	EventBus.locale_changed.connect(_on_locale_changed)
	_apply_fonts()


func show_prompt(action_text: String) -> void:
	_current_action = action_text
	_action_label.text = action_text
	_key_label.text = LocalizationManager.tr_key("UI_INTERACT_KEY")
	_panel.visible = true


func hide_prompt() -> void:
	_panel.visible = false
	_current_action = ""


func is_showing() -> bool:
	return _panel.visible


func _on_locale_changed(_locale_code: String) -> void:
	_apply_fonts()
	if _panel.visible:
		_key_label.text = LocalizationManager.tr_key("UI_INTERACT_KEY")


func _apply_fonts() -> void:
	FontThemeManager.apply_interaction_key(_key_label)
	FontThemeManager.apply_interaction_action(_separator_label)
	FontThemeManager.apply_interaction_action(_action_label)
