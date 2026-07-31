---
id: level-design
type: reference
audience: [builder, builder_zone, architect]
phase: [1, 3, 5]
status: active
authority: world
tokens_est: 900
summary: "Zone layouts, interactables, encounter index"
---
# Level Design

**Hub** — load one pack below.

| Pack | Topic |
|------|-------|
| [`global_rules.md`](levels/global_rules.md) | Global level rules |
| [`beach_shore.md`](levels/beach_shore.md) | Zone beach_shore |
| [`ruined_village.md`](levels/ruined_village.md) | Zone ruined_village |
| [`tidal_caves.md`](levels/tidal_caves.md) | Zone tidal_caves |
| [`dragon_palace.md`](levels/dragon_palace.md) | Palace + endings |
| [`encounters_flags_qa.md`](levels/encounters_flags_qa.md) | Encounters, flags, QA |
# Tides of Urashima — Level Design Breakdown

**Version:** 1.0
**Scope:** Blockouts, pathways, interactables, encounters, camera beats per zone
**Cross-refs:** [WORLD_MAP_AND_FLOW.md](WORLD_MAP_AND_FLOW.md) (zone graph), [ENVIRONMENT_KITS.md](ENVIRONMENT_KITS.md) (art modules), [QUEST_AND_FLAGS.md](QUEST_AND_FLAGS.md) (flags), `game/data/story/scenes.json`

**Use this doc when:** Placing nodes in Godot, wiring triggers, or validating player path.

---
