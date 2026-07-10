extends Node
## Persists user settings and applies graphics quality presets (RENDERING_GUIDE §10).

const SETTINGS_PATH := "user://settings.json"

const PRESETS := {
	"low": {
		"shadows": false,
		"msaa": 0,
		"glow": false,
		"fog_scale": 0.5,
		"shadow_size": 0,
	},
	"medium": {
		"shadows": true,
		"msaa": 2,
		"glow": true,
		"fog_scale": 1.0,
		"shadow_size": 1024,
	},
	"high": {
		"shadows": true,
		"msaa": 4,
		"glow": true,
		"fog_scale": 1.0,
		"shadow_size": 2048,
	},
}

var graphics_quality: String = "medium"
var master_volume: float = 0.8
var music_volume: float = 0.7
var sfx_volume: float = 0.8
var screen_shake: bool = true
var text_speed_cps: float = 40.0


func _ready() -> void:
	load_settings()
	apply_project_graphics()


func load_settings() -> void:
	if not FileAccess.file_exists(SETTINGS_PATH):
		return
	var data = JSON.parse_string(FileAccess.get_file_as_string(SETTINGS_PATH))
	if data is Dictionary:
		graphics_quality = str(data.get("graphics_quality", graphics_quality))
		master_volume = float(data.get("master_volume", master_volume))
		music_volume = float(data.get("music_volume", music_volume))
		sfx_volume = float(data.get("sfx_volume", sfx_volume))
		screen_shake = bool(data.get("screen_shake", screen_shake))
		text_speed_cps = _text_speed_to_cps(str(data.get("text_speed", "normal")))


func save_settings() -> void:
	var data := {
		"graphics_quality": graphics_quality,
		"master_volume": master_volume,
		"music_volume": music_volume,
		"sfx_volume": sfx_volume,
		"screen_shake": screen_shake,
		"text_speed": _cps_to_text_speed(text_speed_cps),
	}
	var file := FileAccess.open(SETTINGS_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data, "\t"))


func set_graphics_quality(preset: String) -> void:
	if preset not in PRESETS:
		return
	graphics_quality = preset
	save_settings()
	apply_project_graphics()
	EventBus.graphics_settings_changed.emit(preset)


func get_preset() -> Dictionary:
	return PRESETS.get(graphics_quality, PRESETS.medium)


func apply_project_graphics() -> void:
	var preset: Dictionary = get_preset()
	ProjectSettings.set_setting("rendering/anti_aliasing/quality/msaa_3d", int(preset.msaa))


func apply_to_environment(env: Environment) -> void:
	var preset: Dictionary = get_preset()
	if not preset.glow:
		env.glow_enabled = false
	if preset.fog_scale != 1.0:
		env.fog_density *= float(preset.fog_scale)


func apply_to_directional_light(light: DirectionalLight3D) -> void:
	var preset: Dictionary = get_preset()
	if not preset.shadows:
		light.shadow_enabled = false
		return
	light.shadow_enabled = true
	var size: int = int(preset.shadow_size)
	if size > 0:
		light.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
		light.directional_shadow_max_distance = 80.0


func _text_speed_to_cps(label: String) -> float:
	match label:
		"slow":
			return 25.0
		"fast":
			return 60.0
		"instant":
			return 999.0
		_:
			return 40.0


func _cps_to_text_speed(cps: float) -> String:
	if cps <= 30.0:
		return "slow"
	if cps >= 80.0:
		return "instant"
	if cps >= 50.0:
		return "fast"
	return "normal"
