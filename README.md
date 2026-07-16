# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4.7 stable (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文, 繁體中文（粵語／國語配音）(Noto Sans — bundled at ship; all four written locales in `game/data/` + `game/locale/translations.csv`)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **`main` is docs + design data only** — no `project.godot`, scenes, or gameplay code.  
> **Implementation** lives on **`game/development`** until M6 ship. See [`docs/BRANCHING.md`](docs/BRANCHING.md).

Build via GodotPrompter + MCP stack per [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).

---

## Agent quick refs (printable)

| Cheat sheet | Purpose |
|-------------|---------|
| [`docs/RR_CHEATSHEET.md`](docs/RR_CHEATSHEET.md) | **Who** owns what — roles, handoffs, tools |
| [`docs/CONTROLS_CHEATSHEET.md`](docs/CONTROLS_CHEATSHEET.md) | **How** roles are enforced — CI, PR templates, gates |

Full index: [`docs/README.md`](docs/README.md) · Cloud agents: [`AGENTS.md`](AGENTS.md)

---

## Project status

| Stage | Status |
|-------|--------|
| **M0** — GDD, storyboard, specs | Done |
| **M0b** — i18n (en / ja / zh / zh-Hant) | Written data in `game/data/` + `translations.csv`; runtime `LocalizationManager` Phase 2+ via GDAI; VO clips Phase 7 |
| **M0c–M0h** — Art, gameplay, narrative, data, AI workflow docs | Done |
| **Phase 0** — Dev environment + design baseline | **Done** (on `main`) |
| **Phases 1–6** — Zones, systems, combat, full story | **`game/development`** — not started |
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
| Build next phase | [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) on branch `game/development` |
| Branch policy | [BRANCHING.md](docs/BRANCHING.md) |
| Roles & handoffs | [RR_CHEATSHEET.md](docs/RR_CHEATSHEET.md) · [MULTI_AGENT_TEAM.md](docs/MULTI_AGENT_TEAM.md) |
| Enforcement / CI | [CONTROLS_CHEATSHEET.md](docs/CONTROLS_CHEATSHEET.md) · [CI.md](docs/CI.md) |
| Sprints (Linear) | [AGILE_WITHIN_PHASES.md](docs/AGILE_WITHIN_PHASES.md) |
| MCP toolchain | [MCP_STACK.md](docs/MCP_STACK.md) |
| QA gates | [ACCEPTANCE_CRITERIA.md](docs/ACCEPTANCE_CRITERIA.md) |
| Code base classes | [CODE_BASE_CLASS_RULES.md](docs/CODE_BASE_CLASS_RULES.md) |
| Ship / CD | [CD.md](docs/CD.md) · [STEAM_RELEASE_CHECKLIST.md](docs/STEAM_RELEASE_CHECKLIST.md) |
| Story / combat JSON | [DATA_ARCHITECTURE.md](docs/DATA_ARCHITECTURE.md) + `game/data/` |

**Authority:** IMPLEMENTATION_PLAN → BRANCHING → MILESTONES → DATA_ARCHITECTURE → ACCEPTANCE_CRITERIA → MCP_STACK / `.cursorrules`

---

## Quick start

**On `main` (docs + data only):**

```bash
bash tools/setup_dev_environment.sh
python3 tools/validate_story_data.py
bash tools/run_docs_ci_checks.sh
```

**On `game/development` (Godot implementation):**

```bash
git checkout game/development
bash tools/install_cloud_dev.sh
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/run_ci_checks.sh
# Open game/project.godot in Godot 4.7 → GDAI MCP → F5
```

| Tool | Role |
|------|------|
| GodotPrompter | Plan + write `.gd`, shaders, tests |
| GDAI MCP | Build scenes in editor |
| Godotiq | Debug signals, Output panel |
| Godot MCP Pro | L4/L5 test scenarios |
| GameLab MCP | UI art — frames, icon sheets **(required)** |
| ComfyUI / Material Maker | Zone NPR albedos (offline) |

Cloud: [`AGENTS.md`](AGENTS.md) · [`docs/GDAI_CLOUD_SETUP.md`](docs/GDAI_CLOUD_SETUP.md)

---

## Repository layout

```
docs/README.md           # Documentation index (start here)
docs/RR_CHEATSHEET.md    # Roles (who)
docs/CONTROLS_CHEATSHEET.md  # Enforcement (how)
game/data/               # Story JSON spine (on main)
game/locale/             # translations.csv
game/scenes/README.md    # GDAI scene policy (no .tscn on main)
tools/                   # Validators, CI, CD scripts
steam/                   # Store copy + trailer
```

**Godot project** (`project.godot`, scripts, assets, scenes): branch **`game/development`** only.

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
