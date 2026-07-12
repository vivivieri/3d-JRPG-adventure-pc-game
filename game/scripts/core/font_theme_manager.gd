extends Node
## Resolves locale-specific Noto font files and applies them to UI themes.


const FONT_ROOT := "res://assets/fonts/"

const LOCALE_FONTS := {
	"en": {
		"regular": "NotoSans-Regular.ttf",
		"bold": "NotoSans-Bold.ttf",
	},
	"ja": {
		"regular": "NotoSansJP-Regular.otf",
		"bold": "NotoSansJP-Bold.otf",
	},
	"zh": {
		"regular": "NotoSansSC-Regular.otf",
		"bold": "NotoSansSC-Bold.otf",
	},
	"zh-Hant": {
		"regular": "NotoSansTC-Regular.otf",
		"bold": "NotoSansTC-Bold.otf",
	},
}

var _regular: Font
var _bold: Font
var _current_locale: String = "en"


func _ready() -> void:
	apply_locale(SettingsManager.get_locale())


func apply_locale(locale: String) -> void:
	_current_locale = locale if LOCALE_FONTS.has(locale) else "en"
	_regular = _load_font("regular")
	_bold = _load_font("bold")


func get_regular_font() -> Font:
	return _regular


func get_bold_font() -> Font:
	return _bold


func get_current_locale() -> String:
	return _current_locale


func apply_to_control(root: Control) -> void:
	if root == null:
		return
	var theme := root.theme
	if theme == null:
		theme = Theme.new()
		root.theme = theme
	if _regular != null:
		theme.default_font = _regular
	if _bold != null:
		theme.default_font_size = theme.default_font_size


func apply_dialogue_fonts(label: Label, speaker_label: Label = null) -> void:
	if label != null and _regular != null:
		label.add_theme_font_override("font", _regular)
	if speaker_label != null and _bold != null:
		speaker_label.add_theme_font_override("font", _bold)


func _load_font(weight: String) -> Font:
	var file_name: String = LOCALE_FONTS[_current_locale][weight]
	var path := FONT_ROOT + file_name
	if not FileAccess.file_exists(path):
		return ThemeDB.fallback_font
	var font := FontFile.new()
	font.load_dynamic_font(path)
	return font
