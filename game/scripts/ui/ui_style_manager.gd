extends Node
## Loads generated UI textures and provides reusable StyleBox helpers.


const PORTRAITS := {
	"urashima": "res://assets/ui/portraits/urashima.png",
	"yuzu": "res://assets/ui/portraits/yuzu.png",
	"roku": "res://assets/ui/portraits/roku.png",
	"shore_wraith": "res://assets/ui/portraits/shore_wraith.png",
	"tide_keeper": "res://assets/ui/portraits/tide_keeper.png",
	"otohime": "res://assets/ui/portraits/tide_keeper.png",
}

const PORTRAIT_ALIASES := {
	"urashima_weary": "urashima",
	"urashima_shocked": "urashima",
	"urashima_resolved": "urashima",
	"urashima_guilty": "urashima",
	"urashima_young": "urashima",
	"yuzu_sad": "yuzu",
	"yuzu_resolved": "yuzu",
	"roku_grim": "roku",
	"roku_serious": "roku",
	"otohime_ethereal": "otohime",
}


func portrait_texture(portrait_key: String) -> Texture2D:
	if portrait_key.is_empty():
		return null
	var base: String = str(PORTRAIT_ALIASES.get(portrait_key, portrait_key))
	var path: String = PORTRAITS.get(base, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		return null
	return load(path) as Texture2D


func panel_style(texture_path: String, margin: int = 16) -> StyleBoxTexture:
	var box := StyleBoxTexture.new()
	if ResourceLoader.exists(texture_path):
		box.texture = load(texture_path)
	box.texture_margin_left = margin
	box.texture_margin_top = margin
	box.texture_margin_right = margin
	box.texture_margin_bottom = margin
	box.set_content_margin_all(margin)
	return box


func dialogue_panel() -> StyleBox:
	return panel_style("res://assets/ui/panel_dialogue.png", 18)


func menu_panel() -> StyleBox:
	return panel_style("res://assets/ui/panel_menu.png", 20)


func bar_fill(kind: String = "hp") -> StyleBoxTexture:
	var path: String = "res://assets/ui/bar_%s_fill.png" % kind
	var box := StyleBoxTexture.new()
	if ResourceLoader.exists(path):
		box.texture = load(path)
	box.set_content_margin_all(2)
	return box


func bar_background() -> StyleBoxTexture:
	var box := StyleBoxTexture.new()
	var path: String = "res://assets/ui/bar_bg.png"
	if ResourceLoader.exists(path):
		box.texture = load(path)
	box.set_content_margin_all(2)
	return box


func apply_to_panel(panel: PanelContainer, style: StyleBox) -> void:
	if style:
		panel.add_theme_stylebox_override(&"panel", style)
