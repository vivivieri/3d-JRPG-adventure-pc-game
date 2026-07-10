shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_disabled, diffuse_toon, specular_toon;

uniform vec4 shallow_color : source_color = vec4(0.1, 0.42, 0.38, 0.75);
uniform vec4 deep_color : source_color = vec4(0.04, 0.18, 0.22, 0.9);
uniform vec4 foam_color : source_color = vec4(0.85, 0.9, 0.88, 1.0);
uniform float wave_speed : hint_range(0.0, 2.0) = 0.35;
uniform float wave_height : hint_range(0.0, 0.3) = 0.04;
uniform float foam_edge : hint_range(0.0, 1.0) = 0.55;

void vertex() {
	float wave = sin(TIME * wave_speed + VERTEX.x * 1.7 + VERTEX.z * 1.3) * wave_height;
	VERTEX.y += wave;
}

void fragment() {
	float depth_mix = clamp(1.0 - abs(NORMAL.y), 0.0, 1.0);
	vec3 water = mix(shallow_color.rgb, deep_color.rgb, depth_mix);
	float foam = smoothstep(foam_edge, foam_edge + 0.12, abs(sin(TIME * 0.8 + UV.x * 12.0) * UV.y));
	vec3 final_color = mix(water, foam_color.rgb, foam * 0.35);
	ALBEDO = final_color;
	ALPHA = mix(shallow_color.a, deep_color.a, depth_mix);
	ROUGHNESS = 0.15;
	METALLIC = 0.0;
	SPECULAR = 0.35;
}
