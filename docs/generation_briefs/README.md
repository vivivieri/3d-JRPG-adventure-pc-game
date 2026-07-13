# Generation briefs

Per-asset and per-zone prompts for autonomous AI 3D pipelines. Template: `docs/GENERATION_READINESS.md` §3.

## Characters & enemies

| Brief | Scope | Phase |
|-------|-------|-------|
| [urashima.md](urashima.md) | Protagonist | 1 |
| [yuzu.md](yuzu.md) | Party healer spirit | M5 / SC-10 |
| [roku.md](roku.md) | Party tank diver | M5 / SC-04 |
| [salt_crab.md](salt_crab.md) | Tutorial enemy | M5 / SC-05 |
| [tide_wraith.md](tide_wraith.md) | Standard enemy | M5 |
| [shore_wraith.md](shore_wraith.md) | First boss | M5 / SC-09 |
| [palace_sentinel.md](palace_sentinel.md) | Miniboss | M5 / SC-14 |
| [tide_keeper_p1.md](tide_keeper_p1.md) | Final boss (P1–P3) | M5 / SC-15–16 |

## Props & set-pieces

| Brief | Scope | Phase |
|-------|-------|-------|
| [lacquer_box.md](lacquer_box.md) | Hero story prop | P0 |
| [village_torii_damaged.md](village_torii_damaged.md) | Hub vista torii | 1 |
| [village_well_stone.md](village_well_stone.md) | Save point | 1 |
| [village_shack_roku.md](village_shack_roku.md) | Roku shop | 1 |
| [palace_gate_main.md](palace_gate_main.md) | Palace entrance | M5 / SC-12 |

## Zones

| Brief | Scope | Phase |
|-------|-------|-------|
| [ruined_village.md](ruined_village.md) | Hub vertical slice | 1 |
| [beach_shore.md](beach_shore.md) | Prologue arrival | 2 |
| [tidal_caves.md](tidal_caves.md) | Dungeon + first boss | 5 |
| [dragon_palace_gate.md](dragon_palace_gate.md) | Finale palace | 6 |

## Not yet briefed

| ID | Action |
|----|--------|
| `otohime` | Bust only — add when palace dialogue ships |
| `villager_spirit`, `rebuilder` | Low-poly crowd silhouettes — ending zones only |
| `ending_*` environments | Defer to Phase 7 per `ENVIRONMENT_KITS.md` §7 |

**Pipeline:** READ brief (incl. Emotional intent) → GEN → `palette_remap.py` → register → GDAI place → measure → jury (M7/M8, V7/V8) → L6.
