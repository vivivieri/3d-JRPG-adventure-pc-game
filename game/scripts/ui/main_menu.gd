extends Control
## Main menu — New Game / Continue / Quit / Language.


func _ready() -> void:
	EventBus.locale_changed.connect(_on_locale_changed)
	$VBox/Continue.disabled = not SaveSystem.has_save()
	_setup_language_selector()
	_refresh_labels()
	_apply_fonts()
	AudioManager.play_bgm("main_menu")


func _apply_fonts() -> void:
	FontThemeManager.apply_title($VBox/Title)
	FontThemeManager.apply_subtitle($VBox/Subtitle)
	FontThemeManager.apply_to_control($VBox)


func _setup_language_selector() -> void:
	var option: OptionButton = $VBox/LanguageRow/LanguageOption
	option.clear()
	for locale in LocalizationManager.SUPPORTED_LOCALES:
		option.add_item(LocalizationManager.LOCALE_LABELS[locale], option.item_count)
		option.set_item_metadata(option.item_count - 1, locale)
	var current := LocalizationManager.get_locale()
	for i in option.item_count:
		if option.get_item_metadata(i) == current:
			option.select(i)
			break
	if not option.item_selected.is_connected(_on_language_selected):
		option.item_selected.connect(_on_language_selected)


func _refresh_labels() -> void:
	$VBox/Title.text = LocalizationManager.tr_key("UI_GAME_TITLE")
	$VBox/Subtitle.text = LocalizationManager.tr_key("UI_GAME_SUBTITLE")
	$VBox/NewGame.text = LocalizationManager.tr_key("UI_NEW_GAME")
	$VBox/Continue.text = LocalizationManager.tr_key("UI_CONTINUE")
	$VBox/Quit.text = LocalizationManager.tr_key("UI_QUIT")
	$VBox/LanguageRow/LanguageLabel.text = LocalizationManager.tr_key("UI_LANGUAGE")


func _on_locale_changed(_locale_code: String) -> void:
	_refresh_labels()
	_apply_fonts()


func _on_language_selected(index: int) -> void:
	var locale: String = $VBox/LanguageRow/LanguageOption.get_item_metadata(index)
	LocalizationManager.set_locale(locale)


func _on_new_game_pressed() -> void:
	GameManager.story_flags.clear()
	GameManager.party_ids = ["urashima"]
	GameManager.party_levels = { "urashima": 1 }
	GameManager.inventory.clear()
	GameManager.equipped.clear()
	GameManager.gold = 0
	GameManager.chosen_ending = ""
	GameManager.current_area = "ruined_village"
	GameManager.inventory = { "sea_salve": 2, "spirit_tonic": 1 }
	GameManager.reset_party_field_stats()
	QuestTracker.active_quests.clear()
	QuestTracker.completed_quests.clear()
	get_tree().change_scene_to_file("res://scenes/world/beach_shore.tscn")


func _on_continue_pressed() -> void:
	if SaveSystem.load_game():
		get_tree().change_scene_to_file("res://scenes/world/ruined_village.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
