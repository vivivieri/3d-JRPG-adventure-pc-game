extends Node3D
## World zone root — applies ZoneVisuals on ready.
## Attach to each zone scene; set zone_id in the inspector.

@export var zone_id: String = "ruined_village"


func _ready() -> void:
	ZoneVisuals.apply_to_scene(self, zone_id)
