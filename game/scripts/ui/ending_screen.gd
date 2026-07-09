extends Control
## Full-screen ending presentation with localized title, body, and return to menu.


@export var ending_id: String = "rewind"


func _ready() -> void:
	_refresh_labels()
	EventBus.locale_changed.connect(_on_locale_changed)
	FontThemeManager.apply_title($Margin/VBox/TitleLabel)
	FontThemeManager.apply_to_control($Margin/VBox)
	$Margin/VBox/MenuBtn.pressed.connect(_on_menu_pressed)


func _refresh_labels() -> void:
	$Margin/VBox/TitleLabel.text = LocalizationManager.tr_key("ending.%s.title" % ending_id)
	$Margin/VBox/BodyLabel.text = LocalizationManager.tr_key("ending.%s.body" % ending_id)
	$Margin/VBox/TheEndLabel.text = LocalizationManager.tr_key("UI_THE_END")
	$Margin/VBox/MenuBtn.text = LocalizationManager.tr_key("UI_RETURN_MENU")


func _on_locale_changed(_locale_code: String) -> void:
	_refresh_labels()


func _on_menu_pressed() -> void:
	GameManager.chosen_ending = ""
	get_tree().change_scene_to_file("res://scenes/world/main_menu.tscn")
