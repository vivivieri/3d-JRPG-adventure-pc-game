class_name LoreSpawner
extends RefCounted
## Spawns lore collectibles for the active zone from data.


static func spawn_for_zone(root: Node3D, zone_id: String) -> void:
	if root.get_node_or_null("LoreCollectibles"):
		return
	var data = GameManager.load_json("res://data/lore/lore_placements.json")
	if data == null:
		return
	var parent := Node3D.new()
	parent.name = "LoreCollectibles"
	root.add_child(parent)
	var script := load("res://scripts/world/lore_collectible.gd") as Script
	for placement in data.get("placements", []):
		if placement.get("zone", "") != zone_id:
			continue
		var lore_id: String = placement.get("id", "")
		if lore_id.is_empty():
			continue
		var pos_arr: Array = placement.get("position", [0, 0, 0])
		var node := StaticBody3D.new()
		node.name = "Lore_%s" % lore_id
		node.set_script(script)
		node.set("lore_id", lore_id)
		node.position = Vector3(pos_arr[0], pos_arr[1], pos_arr[2])
		parent.add_child(node)
