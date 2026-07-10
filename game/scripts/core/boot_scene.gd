extends Control
## Placeholder boot screen until main menu is implemented (Phase 2).


@onready var _status: Label = %Status


func _ready() -> void:
	_status.text = "Dev build %s\nData: game/data/ | Docs: docs/\nPhase 1 zones: res://scenes/world/zone_hub.tscn" % ProjectSettings.get_setting("application/config/version", "0.1.0")
