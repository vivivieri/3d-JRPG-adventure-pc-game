extends Node3D
## World zone root — applies ZoneVisuals on ready.

const ZoneVisualsLib = preload("res://scripts/world/zone_visuals.gd")

@export var zone_id: String = "ruined_village"


func _ready() -> void:
	ZoneVisualsLib.apply_to_scene(self, zone_id)
