extends Node
## Loads locale-appropriate Noto fonts and applies them to the UI tree.

const FONT_PATHS := {
	"en": {
		"regular": "res://assets/fonts/NotoSans-Regular.ttf",
		"bold": "res://assets/fonts/NotoSans-Bold.ttf",
	},
	"ja": {
		"regular": "res://assets/fonts/NotoSansJP-Regular.otf",
		"bold": "res://assets/fonts/NotoSansJP-Bold.otf",
	},
	"zh": {
		"regular": "res://assets/fonts/NotoSansSC-Regular.otf",
		"bold": "res://assets/fonts/NotoSansSC-Bold.otf",
	},
}

const DEFAULT_FONT_SIZE := 18
const TITLE_FONT_SIZE := 48
const SUBTITLE_FONT_SIZE := 18

var _regular: Font
var _bold: Font


func _ready() -> void:
	EventBus.locale_changed.connect(_on_locale_changed)
	call_deferred("apply_for_current_locale")


func apply_for_current_locale() -> void:
	_apply_theme(LocalizationManager.get_locale())


func get_regular_font() -> Font:
	return _regular


func get_bold_font() -> Font:
	return _bold


func apply_title(label: Label) -> void:
	if _bold:
		label.add_theme_font_override("font", _bold)
	label.add_theme_font_size_override("font_size", TITLE_FONT_SIZE)


func apply_subtitle(label: Label) -> void:
	if _regular:
		label.add_theme_font_override("font", _regular)
	label.add_theme_font_size_override("font_size", SUBTITLE_FONT_SIZE)


func apply_dialogue_speaker(label: Label) -> void:
	if _bold:
		label.add_theme_font_override(&"font", _bold)
	label.add_theme_font_size_override(&"font_size", 22)


func apply_dialogue_body(label: Label) -> void:
	if _regular:
		label.add_theme_font_override(&"font", _regular)
	label.add_theme_font_size_override(&"font_size", 20)


func apply_dialogue_hint(label: Label) -> void:
	if _regular:
		label.add_theme_font_override(&"font", _regular)
	label.add_theme_font_size_override(&"font_size", 14)


func apply_interaction_key(label: Label) -> void:
	if _bold:
		label.add_theme_font_override(&"font", _bold)
	label.add_theme_font_size_override(&"font_size", 18)


func apply_interaction_action(label: Label) -> void:
	if _regular:
		label.add_theme_font_override(&"font", _regular)
	label.add_theme_font_size_override(&"font_size", 18)


func apply_combat_title(label: Label) -> void:
	if _bold:
		label.add_theme_font_override(&"font", _bold)
	label.add_theme_font_size_override(&"font_size", 20)


func apply_combat_name(label: Label) -> void:
	if _bold:
		label.add_theme_font_override(&"font", _bold)
	label.add_theme_font_size_override(&"font_size", 16)


func apply_combat_action(control: Control) -> void:
	if _regular:
		control.add_theme_font_override(&"font", _regular)
	control.add_theme_font_size_override(&"font_size", 16)


func apply_combat_hint(label: Label) -> void:
	if _regular:
		label.add_theme_font_override(&"font", _regular)
	label.add_theme_font_size_override(&"font_size", 13)


func apply_combat_log(label: RichTextLabel) -> void:
	if _regular:
		label.add_theme_font_override(&"normal_font", _regular)
	label.add_theme_font_size_override(&"normal_font_size", 14)


func apply_to_control(root: Control) -> void:
	if _regular == null:
		return
	_apply_font_recursive(root)


func _on_locale_changed(_locale_code: String) -> void:
	_apply_theme(_locale_code)


func _apply_theme(locale_code: String) -> void:
	var paths: Dictionary = FONT_PATHS.get(locale_code, FONT_PATHS["en"])
	_regular = _load_font(str(paths.get("regular", "")))
	_bold = _load_font(str(paths.get("bold", "")))
	if _regular == null:
		push_error("FontThemeManager: failed to load regular font for %s" % locale_code)
		return
	var theme := Theme.new()
	theme.default_font = _regular
	theme.default_font_size = DEFAULT_FONT_SIZE
	_set_theme_font(theme, "Label", _regular)
	_set_theme_font(theme, "Button", _regular)
	_set_theme_font(theme, "OptionButton", _regular)
	var tree := get_tree()
	if tree and tree.root:
		tree.root.theme = theme


func _set_theme_font(theme: Theme, type_name: StringName, font: Font) -> void:
	theme.set_font(&"font", type_name, font)
	theme.set_font_size(&"font_size", type_name, DEFAULT_FONT_SIZE)


func _load_font(path: String) -> Font:
	if path.is_empty() or not ResourceLoader.exists(path):
		push_error("FontThemeManager: missing font at %s" % path)
		return null
	var font := FontFile.new()
	var err := font.load_dynamic_font(path)
	if err != OK:
		push_error("FontThemeManager: load_dynamic_font failed (%s) for %s" % [err, path])
		return null
	font.set_antialiasing(TextServer.FONT_ANTIALIASING_GRAY)
	font.set_hinting(TextServer.HINTING_LIGHT)
	return font


func _apply_font_recursive(node: Node) -> void:
	if node is Label:
		var label := node as Label
		if label.get_theme_font_size(&"font_size") >= 40:
			apply_title(label)
		elif label.name.to_lower().contains("subtitle"):
			apply_subtitle(label)
		elif _regular:
			label.add_theme_font_override(&"font", _regular)
	elif node is Button and _regular:
		(node as Button).add_theme_font_override(&"font", _regular)
	elif node is OptionButton and _regular:
		(node as OptionButton).add_theme_font_override(&"font", _regular)
	for child in node.get_children():
		_apply_font_recursive(child)
