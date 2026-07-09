extends Control
## Full-screen ending presentation with localized title, body, credits, and return to menu.


@export var ending_id: String = "rewind"

@onready var _credits: Control = $CreditsRoll


func _ready() -> void:
	_refresh_labels()
	EventBus.locale_changed.connect(_on_locale_changed)
	FontThemeManager.apply_title($Margin/VBox/TitleLabel)
	FontThemeManager.apply_to_control($Margin/VBox)
	$Margin/VBox/MenuBtn.pressed.connect(_on_menu_pressed)
	$Margin/VBox/CreditsBtn.pressed.connect(_on_credits_pressed)
	_credits.finished.connect(_on_credits_finished)
	_credits.visible = false


func _refresh_labels() -> void:
	$Margin/VBox/TitleLabel.text = LocalizationManager.tr_key("ending.%s.title" % ending_id)
	$Margin/VBox/BodyLabel.text = LocalizationManager.tr_key("ending.%s.body" % ending_id)
	$Margin/VBox/TheEndLabel.text = LocalizationManager.tr_key("UI_THE_END")
	$Margin/VBox/CreditsBtn.text = LocalizationManager.tr_key("UI_VIEW_CREDITS")
	$Margin/VBox/MenuBtn.text = LocalizationManager.tr_key("UI_RETURN_MENU")


func _on_locale_changed(_locale_code: String) -> void:
	_refresh_labels()


func _on_credits_pressed() -> void:
	$Margin.visible = false
	_credits.visible = true
	_credits.play()


func _on_credits_finished() -> void:
	_on_menu_pressed()


func _on_menu_pressed() -> void:
	GameManager.chosen_ending = ""
	get_tree().change_scene_to_file("res://scenes/world/main_menu.tscn")
