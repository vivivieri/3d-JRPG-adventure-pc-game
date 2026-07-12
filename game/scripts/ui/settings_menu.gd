extends Control
class_name SettingsMenu
## Settings overlay — language, zh-Hant VO dialect, volume sliders.


@onready var _locale_option: OptionButton = %LocaleOption
@onready var _locale_label: Label = %LocaleLabel
@onready var _dialect_label: Label = %DialectLabel
@onready var _master_label: Label = %MasterLabel
@onready var _music_label: Label = %MusicLabel
@onready var _sfx_label: Label = %SfxLabel
@onready var _dialect_row: HBoxContainer = %DialectRow
@onready var _dialect_option: OptionButton = %DialectOption
@onready var _master_slider: HSlider = %MasterSlider
@onready var _music_slider: HSlider = %MusicSlider
@onready var _sfx_slider: HSlider = %SfxSlider
@onready var _back: Button = %BackButton
@onready var _title: Label = %TitleLabel


func _ready() -> void:
	FontThemeManager.apply_to_control(self)
	_build_locale_options()
	_build_dialect_options()
	_load_from_settings()
	_refresh_labels()
	_back.pressed.connect(_on_back_pressed)
	_locale_option.item_selected.connect(_on_locale_selected)
	_dialect_option.item_selected.connect(_on_dialect_selected)
	_master_slider.value_changed.connect(_on_master_volume_changed)
	_music_slider.value_changed.connect(_on_music_volume_changed)
	_sfx_slider.value_changed.connect(_on_sfx_volume_changed)
	EventBus.locale_changed.connect(_on_locale_changed)
	visible = false


func show_settings() -> void:
	_load_from_settings()
	_refresh_labels()
	visible = true


func hide_settings() -> void:
	visible = false


func _build_locale_options() -> void:
	_locale_option.clear()
	var locales := [
		["en", "English"],
		["ja", "日本語"],
		["zh", "简体中文"],
		["zh-Hant", "繁體中文"],
	]
	for entry in locales:
		_locale_option.add_item(entry[1])
		_locale_option.set_item_metadata(_locale_option.item_count - 1, entry[0])


func _build_dialect_options() -> void:
	_dialect_option.clear()
	_dialect_option.add_item(LocalizationManager.tr_key("UI_VOICE_DIALECT_CANT"))
	_dialect_option.set_item_metadata(0, "cant")
	_dialect_option.add_item(LocalizationManager.tr_key("UI_VOICE_DIALECT_CMN"))
	_dialect_option.set_item_metadata(1, "cmn")


func _load_from_settings() -> void:
	var locale := SettingsManager.get_locale()
	for i in _locale_option.item_count:
		if _locale_option.get_item_metadata(i) == locale:
			_locale_option.select(i)
			break
	var dialect := SettingsManager.get_vo_dialect()
	for i in _dialect_option.item_count:
		if _dialect_option.get_item_metadata(i) == dialect:
			_dialect_option.select(i)
			break
	_master_slider.value = float(SettingsManager.get_value("master_volume")) * 100.0
	_music_slider.value = float(SettingsManager.get_value("music_volume")) * 100.0
	_sfx_slider.value = float(SettingsManager.get_value("sfx_volume")) * 100.0
	_update_dialect_visibility()


func _refresh_labels() -> void:
	_title.text = LocalizationManager.tr_key("UI_SETTINGS")
	_back.text = LocalizationManager.tr_key("UI_BACK")
	_locale_label.text = LocalizationManager.tr_key("UI_LANGUAGE")
	_dialect_label.text = LocalizationManager.tr_key("UI_VOICE_DIALECT")
	_master_label.text = LocalizationManager.tr_key("UI_MASTER_VOLUME")
	_music_label.text = LocalizationManager.tr_key("UI_MUSIC_VOLUME")
	_sfx_label.text = LocalizationManager.tr_key("UI_SFX_VOLUME")
	_build_dialect_options()
	var dialect_idx := 0
	var dialect := SettingsManager.get_vo_dialect()
	for i in _dialect_option.item_count:
		if _dialect_option.get_item_metadata(i) == dialect:
			dialect_idx = i
			break
	_dialect_option.select(dialect_idx)


func _update_dialect_visibility() -> void:
	_dialect_row.visible = LocalizationManager.get_locale() == "zh-Hant"


func _on_locale_selected(index: int) -> void:
	var locale: String = _locale_option.get_item_metadata(index)
	LocalizationManager.set_locale(locale)
	_update_dialect_visibility()


func _on_dialect_selected(index: int) -> void:
	var dialect: String = _dialect_option.get_item_metadata(index)
	LocalizationManager.set_vo_dialect(dialect)


func _on_master_volume_changed(value: float) -> void:
	SettingsManager.set_value("master_volume", value / 100.0)
	SettingsManager.save_settings()


func _on_music_volume_changed(value: float) -> void:
	SettingsManager.set_value("music_volume", value / 100.0)
	SettingsManager.save_settings()


func _on_sfx_volume_changed(value: float) -> void:
	SettingsManager.set_value("sfx_volume", value / 100.0)
	SettingsManager.save_settings()


func _on_locale_changed(_locale: String) -> void:
	_refresh_labels()
	_update_dialect_visibility()


func _on_back_pressed() -> void:
	hide_settings()
