class_name WaterMaterial
extends RefCounted
## Shared stylized water surface material with optional UV animation.


const RIPPLE_TEX := "res://assets/textures/zones/water_ripple.png"


static func make_surface(
	palette: Dictionary,
	zone_id: String,
	shallow: bool = false,
) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	var base: Color = palette.get("water", Color("#1A4A5A"))
	if shallow:
		base = base.lerp(Color.WHITE, 0.18)
	mat.roughness = 0.04
	mat.metallic = 0.18
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED if shallow else BaseMaterial3D.CULL_BACK
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA if shallow else BaseMaterial3D.TRANSPARENCY_DISABLED
	var has_ripple := ResourceLoader.exists(RIPPLE_TEX)
	if has_ripple:
		mat.albedo_texture = load(RIPPLE_TEX)
		mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		mat.uv1_scale = Vector3(2.5, 2.5, 1.0)
		mat.albedo_color = Color.WHITE if shallow else Color(0.82, 0.95, 1.0)
		mat.roughness = 0.03
	else:
		mat.albedo_color = base
	if shallow:
		mat.albedo_color.a = 0.78
	mat.emission_enabled = true
	var accent: Color = palette.get("accent", Color.CYAN)
	mat.emission = accent * (0.1 if shallow else 0.14)
	_apply_zone_accent(mat, zone_id)
	return mat


static func apply_to_mesh(mesh: MeshInstance3D, palette: Dictionary, zone_id: String, shallow: bool = false) -> void:
	if mesh == null:
		return
	mesh.material_override = make_surface(palette, zone_id, shallow)
	_attach_animator(mesh)


static func _attach_animator(mesh: MeshInstance3D) -> void:
	if mesh.get_node_or_null("WaterAnimator"):
		return
	var anim := Node.new()
	anim.name = "WaterAnimator"
	anim.set_script(load("res://scripts/world/water_surface_animator.gd"))
	mesh.add_child(anim)


static func _apply_zone_accent(mat: StandardMaterial3D, zone_id: String) -> void:
	if zone_id == "tidal_caves":
		mat.albedo_color = Color(0.42, 0.82, 0.78)
		mat.emission = Color(0.25, 0.85, 0.78) * 0.18
	elif zone_id == "beach_shore":
		mat.emission = Color(0.18, 0.72, 0.62) * 0.14
