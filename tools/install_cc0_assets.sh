#!/usr/bin/env bash
# Copy curated CC0 Kenney models into game/assets/models/ for Godot import.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DL="${ROOT}/.asset-dl"
OUT="${ROOT}/game/assets/models"
NATURE_SRC="${DL}/nature-kit/Models/GLTF format"
CASTLE_SRC="${DL}/castle/Models"

if [[ ! -d "$NATURE_SRC" ]]; then
  echo "Missing nature kit at $NATURE_SRC — extract nature-kit.zip to .asset-dl/" >&2
  exit 1
fi
if [[ ! -d "$CASTLE_SRC" ]]; then
  echo "Missing castle kit at $CASTLE_SRC — extract castle.zip to .asset-dl/" >&2
  exit 1
fi

mkdir -p "${OUT}/nature" "${OUT}/castle"

NATURE_MODELS=(
  canoe.glb
  bridge_wood.glb
  tree_pineDefaultA.glb
  tree_oak.glb
  tree_default.glb
  rock_largeA.glb
  rock_largeB.glb
  rock_smallA.glb
  rock_smallB.glb
  cliff_block_stone.glb
  cliff_cave_stone.glb
  cliff_corner_stone.glb
  fence_simple.glb
  fence_planks.glb
  log.glb
  log_stack.glb
  stump_round.glb
  plant_bush.glb
  mushroom_red.glb
  grass_large.glb
)

CASTLE_MODELS=(
  gate
  metalGate
  towerSquareTop
  towerTop
  flagBannerLong
  bridge
  knightRed
  door
  wallPillar
  towerSquareArch
)

for f in "${NATURE_MODELS[@]}"; do
  cp -f "${NATURE_SRC}/${f}" "${OUT}/nature/${f}"
done

for base in "${CASTLE_MODELS[@]}"; do
  cp -f "${CASTLE_SRC}/${base}.obj" "${OUT}/castle/${base}.obj"
  [[ -f "${CASTLE_SRC}/${base}.mtl" ]] && cp -f "${CASTLE_SRC}/${base}.mtl" "${OUT}/castle/${base}.mtl"
done

mkdir -p "${OUT}/castle/Textures"
cp -f "${CASTLE_SRC}/Textures/"*.png "${OUT}/castle/Textures/" 2>/dev/null || true

cp -f "${DL}/castle/License.txt" "${OUT}/castle/LICENSE_KENNEY.txt"
cp -f "${DL}/nature-kit/License.txt" "${OUT}/nature/LICENSE_KENNEY.txt" 2>/dev/null || \
  printf '%s\n' "CC0 — Kenney Nature Kit (opengameart.org)" > "${OUT}/nature/LICENSE_KENNEY.txt"

# Manifest for license verification
MANIFEST="${OUT}/asset_manifest.json"
python3 - <<'PY' "$OUT" "$MANIFEST"
import json, os, sys
out, manifest = sys.argv[1], sys.argv[2]
files = []
for dirpath, _, names in os.walk(out):
    for name in sorted(names):
        if name.endswith((".glb", ".obj", ".mtl", ".png")):
            rel = os.path.relpath(os.path.join(dirpath, name), out).replace("\\", "/")
            files.append(rel)
payload = {
    "license": "CC0 1.0",
    "source": "Kenney Nature Kit + Kenney Castle Kit (www.kenney.nl)",
    "files": files,
}
with open(manifest, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)
    f.write("\n")
print(f"Wrote {len(files)} model files to {out}")
PY

echo "CC0 models installed to game/assets/models/"
