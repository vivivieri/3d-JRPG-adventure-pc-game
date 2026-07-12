@tool
extends EditorScenePostImport
## Sanitize AI-generated GLB on import (docs/MODEL_QA.md §M2b).
## Assign in Godot: select .glb → Import → Scene → Advanced → Post Import Script.

const TOON_ROUGHNESS := 1.0
const TOON_METALLIC := 0.0

const MIXAMO_BONE_HINTS := [
	"Hips", "Spine", "Spine1", "Spine2", "Neck", "Head",
	"LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot",
	"LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand",
]


func _post_import(scene: Node) -> Object:
	_normalize_tree(scene)
	return scene


func _normalize_tree(node: Node) -> void:
	if node is MeshInstance3D:
		_sanitize_mesh(node)
	if node is Skeleton3D:
		_warn_skeleton(node)
	for child in node.get_children():
		_normalize_tree(child)


func _sanitize_mesh(mi: MeshInstance3D) -> void:
	var mesh: Mesh = mi.mesh
	if mesh == null:
		return
	for i in mesh.get_surface_count():
		var mat := mesh.surface_get_material(i)
		if mat is StandardMaterial3D:
			var std := mat as StandardMaterial3D
			std.metallic = TOON_METALLIC
			std.roughness = TOON_ROUGHNESS
			std.specular_mode = BaseMaterial3D.SPECULAR_DISABLED
			mesh.surface_set_material(i, std)


func _warn_skeleton(sk: Skeleton3D) -> void:
	var names: Array[String] = []
	for i in sk.get_bone_count():
		names.append(sk.get_bone_name(i))
	var hits := 0
	for hint in MIXAMO_BONE_HINTS:
		if hint in names:
			hits += 1
	if hits < 4:
		push_warning(
			"GLB skeleton may not be Mixamo humanoid (found %d/%d hint bones). See CHARACTER_BIBLE.md"
			% [hits, MIXAMO_BONE_HINTS.size()]
		)
