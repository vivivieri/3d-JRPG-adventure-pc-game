# Blender background script — render 4 turntable views of a GLB.
# Invoked by tools/render_model_turntable.py only.
import math
import sys
from pathlib import Path

import bpy  # type: ignore
import mathutils  # type: ignore


def main() -> None:
    argv = sys.argv
    if "--" not in argv:
        raise SystemExit("usage: blender --background --python blender_turntable_render.py -- <glb> <out_dir>")
    args = argv[argv.index("--") + 1 :]
    if len(args) < 2:
        raise SystemExit("missing glb and out_dir")
    glb_path = Path(args[0])
    out_dir = Path(args[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb_path))

    # Compute bounds
    mins = [1e9, 1e9, 1e9]
    maxs = [-1e9, -1e9, -1e9]
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        raise SystemExit("no meshes in GLB")
    for obj in meshes:
        for corner in obj.bound_box:
            world = obj.matrix_world @ mathutils.Vector(corner)
            for i in range(3):
                mins[i] = min(mins[i], world[i])
                maxs[i] = max(maxs[i], world[i])
    center = [(mins[i] + maxs[i]) / 2 for i in range(3)]
    span = max(maxs[i] - mins[i] for i in range(3)) or 1.0
    dist = span * 2.2

    # Camera + light
    cam_data = bpy.data.cameras.new("TurntableCam")
    cam = bpy.data.objects.new("TurntableCam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    light_data = bpy.data.lights.new("Key", type="AREA")
    light_data.energy = 800
    light = bpy.data.objects.new("Key", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (center[0] + dist, center[1] - dist, center[2] + dist * 0.8)

    fill = bpy.data.lights.new("Fill", type="AREA")
    fill.energy = 200
    fill_obj = bpy.data.objects.new("Fill", fill)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (center[0] - dist, center[1] + dist * 0.5, center[2])

    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    bpy.context.scene.render.resolution_x = 768
    bpy.context.scene.render.resolution_y = 768
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.55, 0.58, 0.62, 1.0)

    views = {
        "front": (0, -1, 0.15),
        "side": (1, 0, 0.1),
        "back": (0, 1, 0.15),
        "three_quarter": (0.7, -0.7, 0.25),
    }

    for name, direction in views.items():
        dx, dy, dz = direction
        norm = math.sqrt(dx * dx + dy * dy + dz * dz)
        cam.location = (
            center[0] + dx / norm * dist,
            center[1] + dy / norm * dist,
            center[2] + dz / norm * dist + span * 0.3,
        )
        target = mathutils.Vector(center)
        cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
        out_file = out_dir / f"{name}.png"
        bpy.context.scene.render.filepath = str(out_file)
        bpy.ops.render.render(write_still=True)
        print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
