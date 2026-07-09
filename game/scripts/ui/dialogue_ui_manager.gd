extends Node
## Instantiates the dialogue box overlay on the root viewport (persists across scenes).


const DIALOGUE_BOX_SCENE := preload("res://scenes/ui/dialogue_box.tscn")

var _dialogue_box: CanvasLayer


func _ready() -> void:
	_dialogue_box = DIALOGUE_BOX_SCENE.instantiate()
	get_tree().root.call_deferred("add_child", _dialogue_box)
