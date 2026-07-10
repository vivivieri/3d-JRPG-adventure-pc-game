class_name ShaderFactory
extends RefCounted

const TOON_SHADER := preload("res://assets/shaders/toon_base.gdshader")
const WATER_SHADER := preload("res://assets/shaders/water_stylized.gdshader")


static func make_toon(color: Color, emission: Color = Color.BLACK, emission_strength: float = 0.0) -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.shader = TOON_SHADER
	mat.set_shader_parameter("albedo_color", color)
	mat.set_shader_parameter("emission_color", emission)
	mat.set_shader_parameter("emission_strength", emission_strength)
	return mat


static func make_water(shallow: Color, deep: Color) -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.shader = WATER_SHADER
	mat.set_shader_parameter("shallow_color", shallow)
	mat.set_shader_parameter("deep_color", deep)
	return mat
