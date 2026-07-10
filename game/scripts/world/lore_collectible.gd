extends StaticBody3D
## World lore pickup — examine to add a journal entry.


@export var lore_id: String = ""


func _ready() -> void:
	if lore_id.is_empty():
		return
	if LoreJournal.is_collected(lore_id):
		visible = false
		return
	_ensure_collision()
	_add_glow()


func interact() -> void:
	if lore_id.is_empty() or LoreJournal.is_collected(lore_id):
		return
	AudioManager.play_sfx("interact")
	if LoreJournal.collect(lore_id):
		DialogueRunner.show_lore_popup(lore_id)
		visible = false


func get_prompt() -> String:
	if lore_id.is_empty() or LoreJournal.is_collected(lore_id):
		return ""
	return LocalizationManager.tr_key("UI_INTERACT_LORE")


func _ensure_collision() -> void:
	if get_node_or_null("Collision"):
		return
	var shape := SphereShape3D.new()
	shape.radius = 0.9
	var col := CollisionShape3D.new()
	col.name = "Collision"
	col.shape = shape
	col.position = Vector3(0, 0.8, 0)
	add_child(col)


func _add_glow() -> void:
	if get_node_or_null("Glow"):
		return
	var orb := MeshInstance3D.new()
	orb.name = "Glow"
	var sphere := SphereMesh.new()
	sphere.radius = 0.22
	sphere.height = 0.44
	orb.mesh = sphere
	orb.position = Vector3(0, 1.1, 0)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("#D4A55A")
	mat.emission_enabled = true
	mat.emission = Color("#FFD890") * 0.55
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	orb.material_override = mat
	add_child(orb)
