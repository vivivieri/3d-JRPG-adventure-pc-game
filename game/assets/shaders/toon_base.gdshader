shader_type spatial;
render_mode diffuse_toon, specular_toon, cull_back;

uniform vec4 albedo_color : source_color = vec4(1.0);
uniform sampler2D albedo_texture : source_color, filter_linear_mipmap, repeat_enable;
uniform float roughness_amount : hint_range(0.0, 1.0) = 1.0;
uniform float emission_strength : hint_range(0.0, 4.0) = 0.0;
uniform vec4 emission_color : source_color = vec4(0.0);

void fragment() {
	vec4 tex = texture(albedo_texture, UV);
	ALBEDO = tex.rgb * albedo_color.rgb;
	ROUGHNESS = roughness_amount;
	METALLIC = 0.0;
	SPECULAR = 0.15;
	if (emission_strength > 0.0) {
		EMISSION = emission_color.rgb * emission_strength * tex.rgb;
	}
}
