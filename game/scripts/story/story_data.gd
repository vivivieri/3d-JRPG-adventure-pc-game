extends RefCounted
class_name StoryData
## Helpers for loading story JSON and filtering dialogue lines by flags.


static func load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("StoryData: missing %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("StoryData: invalid JSON %s" % path)
		return {}
	return parsed


static func filter_dialogue_lines(lines: Array, flags: Dictionary) -> Array:
	var out: Array = []
	for line: Variant in lines:
		if typeof(line) != TYPE_DICTIONARY:
			continue
		var requires: Variant = line.get("requires_flags", {})
		if typeof(requires) == TYPE_DICTIONARY and not requires.is_empty():
			var ok := true
			for key: Variant in requires.keys():
				if flags.get(str(key)) != requires[key]:
					ok = false
					break
			if not ok:
				continue
		out.append(line)
	return out
