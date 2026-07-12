@tool
extends EditorScenePostImport
## Sanitize AI-generated GLB on import (docs/MODEL_QA.md §M2b).
## Assign via tools/install_glb_import_pipeline.sh or Import dock per GLB.

const TOON_SHADER := "res://assets/shaders/toon_base.gdshader"
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


func _toon_material_from(src: Material) -> ShaderMaterial:
	var shader_mat := ShaderMaterial.new()
	var shader := load(TOON_SHADER) as Shader
	if shader == null:
		push_warning("GLB post-import: missing toon shader at %s" % TOON_SHADER)
		return shader_mat
	shader_mat.shader = shader
	if src is StandardMaterial3D:
		var std := src as StandardMaterial3D
		if std.albedo_texture:
			shader_mat.set_shader_parameter("albedo_texture", std.albedo_texture)
		shader_mat.set_shader_parameter("base_color", std.albedo_color)
		if std.emission_enabled:
			shader_mat.set_shader_parameter("emission_color", std.emission)
			shader_mat.set_shader_parameter("emission_energy", std.emission_energy)
	elif src is ORMMaterial3D:
		var orm := src as ORMMaterial3D
		if orm.albedo_texture:
			shader_mat.set_shader_parameter("albedo_texture", orm.albedo_texture)
		shader_mat.set_shader_parameter("base_color", orm.albedo_color)
	else:
		push_warning(
			"GLB post-import: unsupported material type %s — assign toon shader manually"
			% src.get_class()
		)
	return shader_mat


func _sanitize_mesh(mi: MeshInstance3D) -> void:
	var mesh: Mesh = mi.mesh
	if mesh == null:
		return
	for i in mesh.get_surface_count():
		var mat := mesh.surface_get_material(i)
		if mat == null:
			continue
		var toon := _toon_material_from(mat.duplicate())
		mesh.surface_set_material(i, toon)
	mi.material_override = null


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
