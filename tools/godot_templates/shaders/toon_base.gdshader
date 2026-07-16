shader_type spatial;
render_mode diffuse_toon, specular_toon;

uniform vec4 base_color : source_color = vec4(1.0);
uniform sampler2D albedo_texture : source_color, filter_linear_mipmap;
uniform vec4 emission_color : source_color = vec4(0.0);
uniform float emission_energy : hint_range(0.0, 4.0, 0.01) = 0.0;

void fragment() {
	vec4 tex = texture(albedo_texture, UV);
	ALBEDO = tex.rgb * base_color.rgb;
	ROUGHNESS = 1.0;
	METALLIC = 0.0;
	if (emission_energy > 0.0) {
		EMISSION = emission_color.rgb * emission_energy;
	}
}
