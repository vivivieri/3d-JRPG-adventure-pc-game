extends Node
## Validates XP grant and level-up logic.
## godot4 --headless --path game res://tests/xp_level_test.tscn

func _ready() -> void:
	GameManager.reset_new_game()
	var before_level: int = GameManager.party_state["urashima"].level
	var before_xp: int = GameManager.party_state["urashima"].xp
	var ups: Array = GameManager.add_xp("urashima", 45)
	var after_level: int = GameManager.party_state["urashima"].level
	var after_xp: int = GameManager.party_state["urashima"].xp
	print("XP_TEST before=%d/%d after=%d/%d ups=%d" % [before_level, before_xp, after_level, after_xp, ups.size()])
	var ok := after_level > before_level and ups.size() > 0
	get_tree().quit(0 if ok else 1)
