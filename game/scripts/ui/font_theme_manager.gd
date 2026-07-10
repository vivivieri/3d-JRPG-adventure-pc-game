extends Node
## Font stub — swap for Noto bundle in localization phase.


static func apply_dialogue_speaker(label: Label) -> void:
	if label:
		label.add_theme_font_size_override("font_size", 22)


static func apply_dialogue_body(label: Label) -> void:
	if label:
		label.add_theme_font_size_override("font_size", 18)


static func apply_dialogue_hint(label: Label) -> void:
	if label:
		label.add_theme_font_size_override("font_size", 14)


static func apply_interaction_key(label: Label) -> void:
	if label:
		label.add_theme_font_size_override("font_size", 16)


static func apply_interaction_action(label: Label) -> void:
	if label:
		label.add_theme_font_size_override("font_size", 15)
