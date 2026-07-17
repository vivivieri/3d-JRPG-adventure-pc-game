shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_toon, specular_toon;

uniform vec4 zone_tint : source_color = vec4(0.55, 0.72, 0.78, 1.0);
uniform float foam_edge_width : hint_range(0.0, 0.25, 0.01) = 0.08;
uniform float wave_height : hint_range(0.0, 0.5, 0.01) = 0.1;
uniform float wave_speed : hint_range(0.0, 2.0, 0.01) = 0.3;

void vertex() {
	float t = TIME * wave_speed;
	VERTEX.y += sin(VERTEX.x * 2.0 + t) * wave_height;
	VERTEX.y += cos(VERTEX.z * 1.5 + t * 0.8) * wave_height * 0.5;
}

void fragment() {
	vec3 base = zone_tint.rgb;
	float foam = smoothstep(1.0 - foam_edge_width, 1.0, abs(NORMAL.y));
	ALBEDO = mix(base * 0.85, vec3(0.92), foam);
	ROUGHNESS = 1.0;
	METALLIC = 0.0;
}
