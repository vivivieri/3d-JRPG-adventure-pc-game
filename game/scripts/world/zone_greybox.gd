extends Node3D
## Procedural greybox layout for a zone. Editor/dev only — replaced in M6 art rebuild.


@export var zone_id: String = "ruined_village"


func _ready() -> void:
	_build()


func _build() -> void:
	for child in get_children():
		child.queue_free()
	match zone_id:
		"beach_shore":
			_build_beach()
		"ruined_village":
			_build_village()
		"tidal_caves":
			_build_caves()
		"dragon_palace_gate":
			_build_palace()
		_:
			_build_village()


func _add_box(parent: Node3D, name: String, size: Vector3, pos: Vector3, role: String) -> void:
	var mesh := MeshInstance3D.new()
	mesh.name = name
	var box := BoxMesh.new()
	box.size = size
	mesh.mesh = box
	mesh.position = pos
	mesh.set_meta("greybox_role", role)
	parent.add_child(mesh)


func _add_plane(parent: Node3D, name: String, size: Vector2, pos: Vector3, role: String) -> void:
	var mesh := MeshInstance3D.new()
	mesh.name = name
	var plane := PlaneMesh.new()
	plane.size = size
	mesh.mesh = plane
	mesh.position = pos
	mesh.rotation_degrees.x = -90
	mesh.set_meta("greybox_role", role)
	parent.add_child(mesh)


func _add_marker(parent: Node3D, name: String, pos: Vector3) -> void:
	var m := Marker3D.new()
	m.name = name
	m.position = pos
	parent.add_child(m)


func _build_beach() -> void:
	_add_plane(self, "Ground", Vector2(60, 50), Vector3.ZERO, "ground")
	_add_plane(self, "Water", Vector2(60, 18), Vector3(0, -0.05, -22), "water")
	_add_box(self, "DriftwoodA", Vector3(3, 0.6, 1), Vector3(4, 0.3, 6), "structure")
	_add_box(self, "DriftwoodB", Vector3(2, 0.5, 0.8), Vector3(-3, 0.25, 8), "structure")
	_add_box(self, "GateSilhouette", Vector3(4, 5, 0.6), Vector3(0, 2.5, 18), "torii")
	_add_marker(self, "WorldSpawn", Vector3(0, 1, -8))
	_add_marker(self, "ToVillage", Vector3(0, 1, 22))


func _build_village() -> void:
	_add_plane(self, "Ground", Vector2(70, 60), Vector3.ZERO, "ground")
	_add_plane(self, "Sea", Vector2(70, 14), Vector3(0, -0.2, -28), "water")
	_add_box(self, "Pier", Vector3(4, 0.4, 16), Vector3(-6, 0.2, -18), "structure")
	_add_box(self, "ToriiLeft", Vector3(0.5, 5, 0.5), Vector3(-2.5, 2.5, 2), "torii")
	_add_box(self, "ToriiRight", Vector3(0.5, 5, 0.5), Vector3(2.5, 2.5, 2), "torii")
	_add_box(self, "ToriiLint", Vector3(6, 0.5, 0.5), Vector3(0, 5.2, 2), "torii")
	_add_box(self, "Shack", Vector3(6, 3.5, 5), Vector3(8, 1.75, -2), "shack")
	_add_box(self, "Well", Vector3(1.8, 1.2, 1.8), Vector3(-4, 0.6, -4), "structure")
	_add_box(self, "BannerPole", Vector3(0.2, 4, 0.2), Vector3(-8, 2, 6), "accent")
	_add_box(self, "CaveCliff", Vector3(10, 6, 3), Vector3(18, 3, 12), "structure")
	_add_plane(self, "Puddle", Vector2(2.5, 2.5), Vector3(-6, 0.02, 5), "water")
	_add_marker(self, "ToriiShrine", Vector3(0, 0, 2))
	_add_marker(self, "RokuShack", Vector3(8, 0, -2))
	_add_marker(self, "VillageWell", Vector3(-4, 0, -4))
	_add_marker(self, "InspectBanner", Vector3(-8, 0, 6))
	_add_marker(self, "InspectSandal", Vector3(-6, 0, 5))
	_add_marker(self, "TutorialEncounter", Vector3(2, 0, -8))
	_add_marker(self, "CaveEntrance", Vector3(18, 0, 12))
	_add_marker(self, "WorldSpawn", Vector3(0, 1, 10))


func _build_caves() -> void:
	_add_plane(self, "Floor", Vector2(50, 80), Vector3.ZERO, "ground")
	_add_box(self, "TunnelLeft", Vector3(1.5, 5, 30), Vector3(-8, 2.5, 0), "structure")
	_add_box(self, "TunnelRight", Vector3(1.5, 5, 30), Vector3(8, 2.5, 0), "structure")
	_add_box(self, "TunnelCeiling", Vector3(18, 1.5, 30), Vector3(0, 5.5, 0), "structure")
	_add_box(self, "AlgaeA", Vector3(2, 0.3, 2), Vector3(-6, 2, -8), "algae")
	_add_box(self, "AlgaeB", Vector3(2, 0.3, 2), Vector3(5, 1.5, 4), "algae")
	_add_plane(self, "FloodBasin", Vector2(12, 10), Vector3(0, -0.3, -10), "water")
	_add_plane(self, "DeepPool", Vector2(14, 12), Vector3(0, -0.8, -28), "water")
	_add_marker(self, "WaterPuzzle", Vector3(0, 0, -10))
	_add_marker(self, "DeepPoolEncounter", Vector3(0, 0, -28))
	_add_marker(self, "ShoreWraithBoss", Vector3(0, 0, -28))
	_add_marker(self, "WorldSpawn", Vector3(0, 1, 20))


func _build_palace() -> void:
	_add_plane(self, "MarbleFloor", Vector2(60, 70), Vector3.ZERO, "ground")
	_add_plane(self, "VoidSea", Vector2(80, 40), Vector3(0, -8, -40), "water")
	_add_box(self, "GateLeftPillar", Vector3(1.2, 12, 1.2), Vector3(-6, 6, 10), "pillar")
	_add_box(self, "GateRightPillar", Vector3(1.2, 12, 1.2), Vector3(6, 6, 10), "pillar")
	_add_box(self, "GateLint", Vector3(14, 1, 1.5), Vector3(0, 12, 10), "gold")
	_add_box(self, "Bridge", Vector3(4, 0.5, 20), Vector3(0, 0.25, 0), "structure")
	_add_box(self, "MirrorChamber", Vector3(10, 6, 10), Vector3(0, 3, -15), "structure")
	_add_box(self, "ThronePlatform", Vector3(16, 1, 12), Vector3(0, 0.5, -30), "gold")
	_add_marker(self, "GateArrival", Vector3(0, 0, 8))
	_add_marker(self, "MirrorChamber", Vector3(0, 0, -15))
	_add_marker(self, "PalaceSentinel", Vector3(-8, 0, -22))
	_add_marker(self, "TideKeeperBoss", Vector3(0, 0, -30))
	_add_marker(self, "WorldSpawn", Vector3(0, 1, 12))
