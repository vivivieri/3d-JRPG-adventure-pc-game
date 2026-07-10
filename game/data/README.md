# Data Schema — Tides of Urashima

All gameplay content is JSON-driven for fast iteration with AI tooling.

---

## File layout

```
data/
  characters/party.json      # Playable party definitions
  enemies/enemies.json       # Enemy + boss stats, AI, loot
  skills/skills.json         # Skill definitions
  items/items.json           # Consumables and equipment
  dialogue/chapter_01.json   # Scene dialogue by ID
  quests/main_quests.json    # Quest state machine
```

Load via `GameManager.load_json(path)`.

---

## characters/party.json

```json
{
  "id": "urashima",
  "display_name": "Urashima",
  "title": "The Returned Fisherman",
  "element": "water",
  "base_stats": {
    "max_hp": 120,
    "max_mp": 30,
    "atk": 14,
    "def": 10,
    "mag": 8,
    "res": 9,
    "spd": 11
  },
  "growth_per_level": {
    "max_hp": 12,
    "max_mp": 3,
    "atk": 2,
    "def": 1,
    "mag": 1,
    "res": 1,
    "spd": 1
  },
  "starting_skills": ["strike", "tidal_slash"],
  "skill_unlocks": [
    { "level": 5, "skill_id": "ocean_veil" },
    { "level": 10, "skill_id": "returning_wave" }
  ],
  "limit_skill": "box_unbound"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique key |
| `element` | string | `water`, `spirit`, `physical` |
| `base_stats` | object | Level 1 stats |
| `growth_per_level` | object | Added each level up |
| `starting_skills` | string[] | Skill IDs known at recruit |
| `limit_skill` | string | Ultimate when limit gauge full |

---

## enemies/enemies.json

```json
{
  "id": "salt_crab",
  "display_name": "Salt Crab",
  "tier": "normal",
  "element": "physical",
  "stats": {
    "max_hp": 45,
    "atk": 8,
    "def": 6,
    "mag": 4,
    "res": 4,
    "spd": 6
  },
  "skills": ["claw_snap"],
  "ai": {
    "type": "weighted",
    "weights": [
      { "skill_id": "claw_snap", "weight": 80 },
      { "skill_id": "shell_harden", "weight": 20, "hp_below": 0.5 }
    ]
  },
  "rewards": {
    "xp": 18,
    "gold": 12,
    "drops": [{ "item_id": "shell_coin", "chance": 0.3 }]
  },
  "intent_display": "attack"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `tier` | string | `normal`, `elite`, `boss` |
| `ai.type` | string | `weighted`, `sequence`, `phase` |
| `ai.weights` | array | Weighted random skill pick; optional `hp_below` |
| `intent_display` | string | UI icon: `attack`, `defend`, `charge`, `debuff` |
| `phases` | array | Boss only — HP thresholds with new AI/skills |

---

## skills/skills.json

```json
{
  "id": "tidal_slash",
  "display_name": "Tidal Slash",
  "description": "A swift strike infused with sea current.",
  "mp_cost": 6,
  "target": "single_enemy",
  "element": "water",
  "power": 1.35,
  "effects": [],
  "animation": "slash_water",
  "sfx": "skill_water_light"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `target` | string | `self`, `single_ally`, `all_allies`, `single_enemy`, `all_enemies` |
| `power` | float | Multiplier on ATK (physical) or MAG (magical) |
| `effects` | array | Status effects applied on hit |
| `power_stat` | string | `atk` (default) or `mag` |

### Effect object

```json
{
  "type": "poison",
  "chance": 0.6,
  "duration": 3,
  "potency": 5
}
```

Supported `type`: `poison`, `regen`, `stun`, `def_up`, `def_down`, `atk_up`, `taunt`.

---

## items/items.json

```json
{
  "id": "sea_salve",
  "display_name": "Sea Salve",
  "type": "consumable",
  "description": "Restores 80 HP.",
  "battle_use": true,
  "field_use": true,
  "effect": { "type": "heal_hp", "value": 80 },
  "buy_price": 40,
  "sell_price": 20
}
```

Equipment adds `slot`: `weapon`, `armor`, `charm` and `stat_bonus` object.

---

## dialogue/chapter_01.json

```json
{
  "speaker": "yuzu",
  "text": {
    "en": "You left. We waited.",
    "ja": "あなたは去った。私たちは待っていた。",
    "zh": "你离开了。我们一直等着。"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `text` | object | **Required** — `en`, `ja`, `zh` strings (see `docs/LOCALIZATION.md`) |
| `speaker` | string | Speaker id → localized via `speaker.{id}` CSV key |
| `on_complete` | object | Flags, quests, item rewards |

---

## quests/main_quests.json

```json
{
  "id": "echoes_at_torii",
  "title": "Echoes at the Torii",
  "stages": [
    {
      "id": "investigate_shrine",
      "description": "Investigate the cracked torii gate.",
      "completion": { "flag": "met_yuzu_spirit" }
    },
    {
      "id": "enter_caves",
      "description": "Find the path to the Tidal Caves.",
      "completion": { "flag": "caves_unlocked" }
    }
  ],
  "rewards": { "xp": 50, "gold": 0 }
}
```

---

## Combat math (reference)

**Physical damage:**
```
damage = max(1, floor(attacker.atk * skill.power - defender.def * 0.5))
```

**Magical damage:**
```
damage = max(1, floor(attacker.mag * skill.power - defender.res * 0.5))
```

**Element modifier:** 1.25 weak, 0.75 resist, 1.0 neutral (table in `skill_resolver.gd`).

**Defend:** 50% damage reduction for the turn.

**Limit gauge:** +8 on attack, +12 on damage taken; at 100, unlock Limit skill.
