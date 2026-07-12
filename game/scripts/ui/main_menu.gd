extends Control
## Main menu — New Game / Continue / Settings / Gallery / Quit.


@onready var _new_game: Button = %NewGame
@onready var _continue: Button = %Continue
@onready var _settings: Button = %Settings
@onready var _gallery: Button = %Gallery
@onready var _quit: Button = %Quit
@onready var _settings_panel: Control = %SettingsPanel


func _ready() -> void:
	FontThemeManager.apply_to_control(self)
	_refresh_labels()
	EventBus.locale_changed.connect(_on_locale_changed)
	_new_game.pressed.connect(_on_new_game_pressed)
	_continue.pressed.connect(_on_continue_pressed)
	_settings.pressed.connect(_on_settings_pressed)
	_gallery.pressed.connect(_on_gallery_pressed)
	_quit.pressed.connect(_on_quit_pressed)
	_continue.disabled = not FileAccess.file_exists("user://save_slot_0.json")


func _refresh_labels() -> void:
	_new_game.text = LocalizationManager.tr_key("UI_NEW_GAME")
	_continue.text = LocalizationManager.tr_key("UI_CONTINUE")
	_settings.text = LocalizationManager.tr_key("UI_SETTINGS")
	_gallery.text = LocalizationManager.tr_key("UI_GALLERY")
	_quit.text = LocalizationManager.tr_key("UI_QUIT")


func _on_locale_changed(_locale: String) -> void:
	_refresh_labels()


func _on_new_game_pressed() -> void:
	# Phase 2.4 — SC-00 prologue not yet built; stay on menu for now.
	pass


func _on_continue_pressed() -> void:
	# Phase 2.4 — SaveSystem not yet built.
	pass


func _on_settings_pressed() -> void:
	_settings_panel.show_settings()


func _on_gallery_pressed() -> void:
	# Phase 6 — Ending gallery not yet built.
	pass


func _on_quit_pressed() -> void:
	get_tree().quit()
