extends Control
## Dev boot screen — validates data paths via GameBootstrap autoload.
## Gameplay scenes rebuild via GodotPrompter + GDAI MCP (see docs/IMPLEMENTATION_PLAN.md).


@onready var _status: Label = %Status


func _ready() -> void:
	var version: String = ProjectSettings.get_setting("application/config/version", "0.1.0")
	_status.text = (
		"Fresh rebuild %s\n"
		+ "Data: game/data/ | Docs: docs/\n"
		+ "Next: Phase 1 — ruined_village vertical slice (GDAI MCP)"
	) % version
