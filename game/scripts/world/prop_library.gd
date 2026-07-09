class_name PropLibrary
extends RefCounted
## Spawns CC0 props — prefers high-poly Poly Haven, falls back to Kenney.


const POLYHAVEN := {
	"tree_coastal_a": "res://assets/models/polyhaven/tree_coastal_a/tree_coastal_a_1k.gltf",
	"tree_coastal_b": "res://assets/models/polyhaven/tree_coastal_b/tree_coastal_b_1k.gltf",
	"pine_hd": "res://assets/models/polyhaven/pine_hd/pine_hd_1k.gltf",
	"fir_hd": "res://assets/models/polyhaven/fir_hd/fir_hd_1k.gltf",
	"cliff_coastal": "res://assets/models/polyhaven/cliff_coastal/cliff_coastal_1k.gltf",
	"boulder_a": "res://assets/models/polyhaven/boulder_a/boulder_a_1k.gltf",
	"rocks_moss_a": "res://assets/models/polyhaven/rocks_moss_a/rocks_moss_a_1k.gltf",
	"rocks_moss_b": "res://assets/models/polyhaven/rocks_moss_b/rocks_moss_b_1k.gltf",
	"dead_trunk": "res://assets/models/polyhaven/dead_trunk/dead_trunk_1k.gltf",
	"grass_hd": "res://assets/models/polyhaven/grass_hd/grass_hd_1k.gltf",
	"grass_clump": "res://assets/models/polyhaven/grass_clump/grass_clump_1k.gltf",
	"fern": "res://assets/models/polyhaven/fern/fern_1k.gltf",
	"shrub_hd": "res://assets/models/polyhaven/shrub_hd/shrub_hd_1k.gltf",
	"branches": "res://assets/models/polyhaven/branches/branches_1k.gltf",
}

const KENNEY := {
	"canoe": "res://assets/models/nature/canoe.glb",
	"canoe_paddle": "res://assets/models/nature/canoe_paddle.glb",
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
	"grass_small": "res://assets/models/nature/grass.glb",
	"grass_leafs": "res://assets/models/nature/grass_leafs.glb",
	"path_stone": "res://assets/models/nature/path_stone.glb",
	"path_corner": "res://assets/models/nature/path_stoneCorner.glb",
	"fence_gate": "res://assets/models/nature/fence_gate.glb",
	"cliff_slope": "res://assets/models/nature/cliff_blockSlope_stone.glb",
	"rock_tall_a": "res://assets/models/nature/rock_tallA.glb",
	"rock_tall_b": "res://assets/models/nature/rock_tallB.glb",
	"plant_flat": "res://assets/models/nature/plant_flatShort.glb",
	"tree_detailed": "res://assets/models/nature/tree_detailed.glb",
	"tree_fat": "res://assets/models/nature/tree_fat.glb",
	"mushroom_tan": "res://assets/models/nature/mushroom_tan.glb",
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
	"castle_tower_base": "res://assets/models/castle/towerSquareBase.obj",
	"castle_wall": "res://assets/models/castle/wall.obj",
	"castle_stairs": "res://assets/models/castle/stairsStone.obj",
}

# Prefer Poly Haven for detail props; trees/cliffs stay Kenney unless spawned by HD id directly.
const PROP_CHAIN := {
	"rock_large_a": ["boulder_a", "rock_large_a"],
	"rock_large_b": ["rocks_moss_b", "rock_large_b"],
	"rock_small_a": ["rocks_moss_a", "rock_small_a"],
	"rock_small_b": ["rocks_moss_b", "rock_small_b"],
	"bush": ["shrub_hd", "bush"],
	"grass_small": ["grass_hd", "grass_small"],
	"grass": ["grass_clump", "grass"],
	"grass_leafs": ["fern", "grass_leafs"],
	"log": ["dead_trunk", "log"],
	"stump": ["dead_trunk", "stump"],
	"log_stack": ["branches", "log_stack"],
	"plant_flat": ["fern", "plant_flat"],
	"mushroom": ["shrub_hd", "mushroom"],
	"mushroom_tan": ["shrub_hd", "mushroom_tan"],
}

# Real-world Poly Haven assets need per-asset scale correction vs Kenney props.
const HD_SCALE := {
	"tree_coastal_a": 1.0,
	"tree_coastal_b": 1.0,
	"pine_hd": 1.0,
	"fir_hd": 1.0,
	"cliff_coastal": 0.07,
	"boulder_a": 1.0,
	"rocks_moss_a": 0.45,
	"rocks_moss_b": 0.5,
	"dead_trunk": 0.4,
	"grass_hd": 14.0,
	"grass_clump": 4.0,
	"fern": 3.5,
	"shrub_hd": 18.0,
	"branches": 0.55,
}

static var _cache: Dictionary = {}


static func has_prop(prop_id: String) -> bool:
	return not _resolve_path(prop_id, true).is_empty()


static func spawn(
	prop_id: String,
	parent: Node3D,
	pos: Vector3 = Vector3.ZERO,
	rot_y_deg: float = 0.0,
	scale_factor: float = 1.0,
	prefer_hd: bool = true,
) -> Node3D:
	var resolved := _resolve_prop_id(prop_id, prefer_hd)
	if resolved.is_empty():
		return null
	var node := _instantiate(resolved)
	if node == null:
		return null
	parent.add_child(node)
	node.position = pos
	node.rotation_degrees.y = rot_y_deg
	var hd_mul: float = HD_SCALE.get(resolved, 1.0)
	var final_scale := scale_factor * hd_mul
	if final_scale != 1.0:
		node.scale = Vector3.ONE * final_scale
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


static func _resolve_prop_id(prop_id: String, prefer_hd: bool = true) -> String:
	if not prefer_hd:
		return prop_id if _resolve_path(prop_id, false) != "" else ""
	var chain: Array = PROP_CHAIN.get(prop_id, [prop_id])
	for candidate in chain:
		if _resolve_path(str(candidate), true) != "":
			return str(candidate)
	return ""


static func _resolve_path(prop_id: String, allow_polyhaven: bool = true) -> String:
	var path: String = ""
	if allow_polyhaven:
		path = POLYHAVEN.get(prop_id, "")
	if path.is_empty():
		path = KENNEY.get(prop_id, "")
	if path.is_empty() or not ResourceLoader.exists(path):
		return ""
	return path


static func _instantiate(prop_id: String) -> Node3D:
	if _cache.has(prop_id):
		var cached: Resource = _cache[prop_id]
		if cached is PackedScene:
			return (cached as PackedScene).instantiate() as Node3D
		if cached is Mesh:
			return _mesh_node(cached as Mesh)
	var path := _resolve_path(prop_id, true)
	if path.is_empty():
		push_warning("PropLibrary: missing prop '%s'" % prop_id)
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
