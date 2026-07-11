# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4.7 stable (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans — bundled at ship)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **`main` is the clean baseline:** design docs, story JSON (`game/data/`), workflow rules, and a minimal Godot boot shell. **Gameplay is not implemented yet** — rebuild via GodotPrompter + full MCP stack per [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).

---

## Project status

| Stage | Status |
|-------|--------|
| **M0** — GDD, storyboard, specs | Done |
| **M0b** — i18n (en / ja / zh / zh-Hant) | Spec done — `LocalizationManager` Phase 2+ |
| **M0c–M0h** — Art, gameplay, narrative, data, AI workflow docs | Done |
| **Phase 0** — Dev environment + boot shell | **Done** |
| **Phases 1–6** — Zones, systems, combat, full story | **Not started** |
| **M5 / Phase 7** — Art rebuild (NPR zones, hero meshes, curated audio) | Not started |
| **M6 / Phase 8** — Steam export, compliance, Windows playtest | Not started |

**Next build step:** Phase 1 — `ruined_village` vertical slice (SC-02). Checklist: [`docs/MILESTONES.md`](docs/MILESTONES.md).

| Phase | Milestone | Focus |
|-------|-----------|-------|
| 1 | — | Environment + SC-02 vertical slice gate |
| 2–3 | M1 | Core systems + narrative exploration |
| 4 | M2 | Combat vertical slice |
| 5 | M3 | Chapter 1 (caves, puzzle, Shore Wraith) |
| 6 | M4 | Full story + three endings |
| 7 | **M5** | Art rebuild |
| 8 | **M6** | Steam ship — GodotSteam 4.20+ |

---

## Documentation

**Full index:** [`docs/README.md`](docs/README.md)

| Task | Read |
|------|------|
| Build next phase | [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) |
| Runtime architecture (TDD) | [TECHNICAL_DESIGN.md](docs/TECHNICAL_DESIGN.md) |
| GDScript conventions | [CODE_STYLE.md](docs/CODE_STYLE.md) |
| Zones, interactables, triggers | [LEVEL_DESIGN.md](docs/LEVEL_DESIGN.md) |
| Story / combat JSON | [DATA_ARCHITECTURE.md](docs/DATA_ARCHITECTURE.md) + `game/data/` |
| MCP toolchain | [MCP_STACK.md](docs/MCP_STACK.md) |
| QA gates & acceptance | [ACCEPTANCE_CRITERIA.md](docs/ACCEPTANCE_CRITERIA.md) |

**Authority:** IMPLEMENTATION_PLAN → MILESTONES → TECHNICAL_DESIGN → DATA_ARCHITECTURE → ACCEPTANCE_CRITERIA → MCP_STACK / `.cursorrules`

---

## Quick start

```bash
bash tools/setup_dev_environment.sh
bash tools/ensure_mcp_stack.sh
bash tools/check_dev_environment.sh
bash tools/run_unit_tests.sh
python3 tools/validate_story_data.py
python3 tools/validate_acceptance_criteria.py
bash tools/run_playtest_smoke.sh       # L2 smoke (recommended every commit)
```

Open `game/project.godot` in Godot 4.7 → **F5** (boot screen only).

| Tool | Role |
|------|------|
| GodotPrompter | Plan + write `.gd`, shaders, tests |
| GDAI MCP | Build scenes in editor |
| Godotiq | Debug signals, Output panel |
| Godot MCP Pro | L4/L5 test scenarios |
| GameLab MCP *(P1)* | UI art — frames, icon sheets |
| ComfyUI / Material Maker | Zone NPR albedos (offline) |

Cloud: [`AGENTS.md`](AGENTS.md) · [`docs/GDAI_CLOUD_SETUP.md`](docs/GDAI_CLOUD_SETUP.md)

---

## Repository layout

```
docs/README.md           # Documentation index (start here)
game/data/               # Story JSON spine
game/scenes/boot.tscn    # Dev boot only
game/scripts/            # Boot + story stubs (Phase 2+ expands)
tools/validate_story_data.py
steam/                   # Store copy + trailer
```

---

## Design highlights

- **Story:** Dark Urashima retelling — ruined village, lacquer box, stolen years
- **Combat:** Turn-based, speed-initiative, JSON-driven skills/enemies
- **Endings:** Rewind / Anchor / Drift
- **Cinematics:** Godot cameras — no FMV
- **VO:** 12 selective clips — not full dialogue
- **Visuals:** Muted Japanese coastal 3D; greybox until M5 art pass

---

## Steam (M6)

[`steam/STORE_PAGE.md`](steam/STORE_PAGE.md) · GodotSteam 4.20+ · [`steam/GODOTSTEAM_SETUP.md`](steam/GODOTSTEAM_SETUP.md)

---

## Credits

- Story: *Urashima Tarō* (public domain)
- Engine: [Godot](https://godotengine.org) (MIT)
