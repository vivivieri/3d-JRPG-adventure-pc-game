extends RefCounted
## Builds simple stylized humanoid proxies from primitives (pre-art phase).

const PALETTES := {
	"urashima": {"body": Color(0.42, 0.58, 0.78), "accent": Color(0.2, 0.35, 0.55)},
	"yuzu": {"body": Color(0.82, 0.48, 0.62), "accent": Color(0.95, 0.82, 0.55)},
	"roku": {"body": Color(0.38, 0.52, 0.4), "accent": Color(0.55, 0.42, 0.28)},
}

const ENEMY_PALETTES := {
	"salt_crab": Color(0.92, 0.55, 0.18),
	"tide_wraith": Color(0.35, 0.72, 0.92),
	"shore_wraith": Color(0.62, 0.32, 0.88),
	"palace_sentinel": Color(0.88, 0.75, 0.22),
	"tide_keeper": Color(0.18, 0.42, 0.82),
}


static func build_character(parent: Node3D, char_id: String) -> Node3D:
	var root := Node3D.new()
	root.name = "CharacterVisual_%s" % char_id
	var palette: Dictionary = PALETTES.get(char_id, PALETTES.urashima)
	_add_part(root, "Torso", Vector3(0.55, 0.75, 0.32), Vector3(0, 1.05, 0), palette.body)
	_add_part(root, "Head", Vector3(0.34, 0.34, 0.34), Vector3(0, 1.62, 0), palette.body.lightened(0.08))
	_add_part(root, "ArmL", Vector3(0.14, 0.55, 0.14), Vector3(-0.38, 1.05, 0), palette.accent)
	_add_part(root, "ArmR", Vector3(0.14, 0.55, 0.14), Vector3(0.38, 1.05, 0), palette.accent)
	_add_part(root, "LegL", Vector3(0.18, 0.62, 0.18), Vector3(-0.16, 0.35, 0), palette.accent.darkened(0.1))
	_add_part(root, "LegR", Vector3(0.18, 0.62, 0.18), Vector3(0.16, 0.35, 0), palette.accent.darkened(0.1))
	match char_id:
		"urashima":
			_add_part(root, "Katana", Vector3(0.05, 0.7, 0.05), Vector3(0.42, 1.0, 0.1), Color(0.75, 0.78, 0.82))
		"yuzu":
			_add_part(root, "Ribbon", Vector3(0.28, 0.08, 0.08), Vector3(0, 1.78, 0.12), palette.accent)
		"roku":
			_add_part(root, "Tank", Vector3(0.42, 0.5, 0.28), Vector3(-0.42, 1.0, 0), Color(0.45, 0.5, 0.52))
			_add_part(root, "Helmet", Vector3(0.38, 0.18, 0.38), Vector3(0, 1.78, 0), palette.accent)
	parent.add_child(root)
	return root


static func build_enemy_placeholder(parent: Node3D, enemy_id: String) -> Node3D:
	var root := Node3D.new()
	root.name = "EnemyVisual_%s" % enemy_id
	var color: Color = ENEMY_PALETTES.get(enemy_id, Color(0.7, 0.3, 0.3))
	if enemy_id == "salt_crab":
		_add_part(root, "Shell", Vector3(0.8, 0.35, 0.7), Vector3(0, 0.35, 0), color)
		_add_part(root, "ClawL", Vector3(0.25, 0.12, 0.35), Vector3(-0.45, 0.25, 0.2), color.darkened(0.15))
		_add_part(root, "ClawR", Vector3(0.25, 0.12, 0.35), Vector3(0.45, 0.25, 0.2), color.darkened(0.15))
	else:
		_add_part(root, "Body", Vector3(0.55, 1.1, 0.35), Vector3(0, 0.75, 0), color)
		_add_part(root, "Crown", Vector3(0.2, 0.35, 0.2), Vector3(0, 1.45, 0), color.lightened(0.15))
	parent.add_child(root)
	return root


static func _add_part(parent: Node3D, part_name: String, size: Vector3, pos: Vector3, color: Color) -> void:
	var mesh := MeshInstance3D.new()
	mesh.name = part_name
	var box := BoxMesh.new()
	box.size = size
	mesh.mesh = box
	mesh.position = pos
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mesh.material_override = mat
	parent.add_child(mesh)
