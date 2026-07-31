---
id: technical-design
type: reference
audience: [architect, builder]
phase: [1, 2, 3, 4, 5, 6]
status: active
authority: engineering
tokens_est: 238
summary: "Runtime architecture — load the stack for your feature"
---
# Technical Design

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`principles_runtime.md`](tdd/principles_runtime.md) | Design principles + runtime architecture |
| [`scene_data_save.md`](tdd/scene_data_save.md) | Scene flow, data loading, save/load |
| [`narrative_combat.md`](tdd/narrative_combat.md) | Narrative + combat stacks |
| [`exploration_audio_ui.md`](tdd/exploration_audio_ui.md) | Exploration, audio, UI |
| [`testing_phases.md`](tdd/testing_phases.md) | Testing hooks, phase map, related |
**Version:** 1.1
**Engine:** Godot 4.7 stable, Forward+
**Architecture:** Scene-tree JRPG with autoload singletons — **not** ECS
**Status:** Pre-build spec — Phase 2+ implementation

