class_name PropLibrary
extends RefCounted
## Spawns curated CC0 Kenney models (GLB/OBJ) with caching.


const PROPS := {
	# Nature kit
	"canoe": "res://assets/models/nature/canoe.glb",
	"bridge_wood": "res://assets/models/nature/bridge_wood.glb",
	"tree_pine": "res://assets/models/nature/tree_pineDefaultA.glb",
	"tree_oak": "res://assets/models/nature/tree_oak.glb",
	"tree_default": "res://assets/models/nature/tree_default.glb",
	"rock_large_a": "res://assets/models/nature/rock_largeA.glb",
	"rock_large_b": "res://assets/models/nature/rock_largeB.glb",
	"rock_small_a": "res://assets/models/nature/rock_smallA.glb",
	"rock_small_b": "res://assets/models/nature/rock_smallB.glb",
	"cliff_block": "res://assets/models/nature/cliff_block_stone.glb",
	"cliff_cave": "res://assets/models/nature/cliff_cave_stone.glb",
	"cliff_corner": "res://assets/models/nature/cliff_corner_stone.glb",
	"fence_simple": "res://assets/models/nature/fence_simple.glb",
	"fence_planks": "res://assets/models/nature/fence_planks.glb",
	"log": "res://assets/models/nature/log.glb",
	"log_stack": "res://assets/models/nature/log_stack.glb",
	"stump": "res://assets/models/nature/stump_round.glb",
	"bush": "res://assets/models/nature/plant_bush.glb",
	"mushroom": "res://assets/models/nature/mushroom_red.glb",
	"grass": "res://assets/models/nature/grass_large.glb",
	# Castle kit
	"castle_gate": "res://assets/models/castle/gate.obj",
	"castle_metal_gate": "res://assets/models/castle/metalGate.obj",
	"castle_tower_top": "res://assets/models/castle/towerSquareTop.obj",
	"castle_tower": "res://assets/models/castle/towerTop.obj",
	"castle_banner": "res://assets/models/castle/flagBannerLong.obj",
	"castle_bridge": "res://assets/models/castle/bridge.obj",
	"knight_red": "res://assets/models/castle/knightRed.obj",
	"castle_door": "res://assets/models/castle/door.obj",
	"castle_pillar": "res://assets/models/castle/wallPillar.obj",
	"castle_arch": "res://assets/models/castle/towerSquareArch.obj",
}

static var _cache: Dictionary = {}


static func has_prop(prop_id: String) -> bool:
	var path: String = PROPS.get(prop_id, "")
	return not path.is_empty() and ResourceLoader.exists(path)


static func spawn(
	prop_id: String,
	parent: Node3D,
	pos: Vector3 = Vector3.ZERO,
	rot_y_deg: float = 0.0,
	scale_factor: float = 1.0,
) -> Node3D:
	var node := _instantiate(prop_id)
	if node == null:
		return null
	parent.add_child(node)
	node.position = pos
	node.rotation_degrees.y = rot_y_deg
	if scale_factor != 1.0:
		node.scale = Vector3.ONE * scale_factor
	return node


static func spawn_many(
	prop_id: String,
	parent: Node3D,
	positions: Array,
	scale_factor: float = 1.0,
) -> void:
	for entry in positions:
		var pos: Vector3 = entry if entry is Vector3 else Vector3(entry[0], entry[1], entry[2])
		var rot_y: float = entry.get("rot_y", 0.0) if entry is Dictionary else 0.0
		spawn(prop_id, parent, pos, rot_y, scale_factor)


static func _instantiate(prop_id: String) -> Node3D:
	if _cache.has(prop_id):
		var cached: Resource = _cache[prop_id]
		if cached is PackedScene:
			return (cached as PackedScene).instantiate() as Node3D
		if cached is Mesh:
			return _mesh_node(cached as Mesh)
	var path: String = PROPS.get(prop_id, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		push_warning("PropLibrary: missing prop '%s' at %s" % [prop_id, path])
		return null
	var res: Resource = load(path)
	_cache[prop_id] = res
	if res is PackedScene:
		return (res as PackedScene).instantiate() as Node3D
	if res is Mesh:
		return _mesh_node(res as Mesh)
	push_warning("PropLibrary: unsupported resource type for '%s': %s" % [prop_id, res.get_class()])
	return null


static func _mesh_node(mesh: Mesh) -> MeshInstance3D:
	var inst := MeshInstance3D.new()
	inst.mesh = mesh
	return inst
