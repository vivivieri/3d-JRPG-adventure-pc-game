# Git LFS — Large Asset Tracking

**Version:** 1.0
**Applies to:** `game/development` — hero meshes, textures, audio (M5+)
**Patterns:** `.gitattributes` at repo root
**Cross-refs:** `docs/art/ASSET_COMPLIANCE.md`, `docs/workflow/DEVELOPMENT_LIFECYCLE.md` §10.4

---

## 1. Why LFS

3D JRPG assets (GLB, textures, OGG) bloat `.git` when stored as plain blobs. LFS stores pointers in git and binaries in LFS storage.

**Orthogonal to branching** — works with trunk + `cursor/*` feature branches.

---

## 2. Tracked patterns

| Pattern | Examples |
|---------|----------|
| `*.glb`, `*.gltf`, `*.blend`, `*.fbx` | Hero meshes, Blender sources |
| `game/assets/**/*.png` etc. | Zone NPR albedos, UI sheets |
| `game/assets/audio/**/*.ogg` | BGM/SFX ship assets |

Small files (SVG icons, JSON, `.gd`) stay in normal git.

---

## 3. Setup (once per machine)

```bash
bash tools/install_git_lfs.sh
```

CI and cloud dev call this automatically (`install_ci_deps.sh`, `install_cloud_dev.sh`).

### First commit of a large file

```bash
git add game/assets/models/hero_urashima.glb
git commit -m "feat(assets): register hero mesh via LFS"
git push
```

GitHub LFS bandwidth/storage quotas apply on the remote.

---

## 4. Clone / CI

Workflows use `actions/checkout@v4` with `lfs: true` on branches that may contain assets.

After clone locally:

```bash
git lfs pull
```

---

## 5. Verify

```bash
git lfs ls-files
git lfs status
```

---

## 6. Cross-refs

- `tools/register_asset.py` — manifest after adding assets
- `bash tools/check_asset_compliance.sh` — license gate before ship
