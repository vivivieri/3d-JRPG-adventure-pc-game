---
id: layouts
type: reference
phase: [1, 5]
audience: [architect, builder, narrative]
status: active
authority: world
tokens_est: 427
summary: "World Map & Flow — Zone layouts — covers 4. Ruined village layout (hub); 5. Tidal caves layout (linear with branch); 6. Dragon Palace Gate layout"
---
# World Map & Flow — Zone layouts

**Hub:** [`WORLD_MAP_AND_FLOW.md`](../WORLD_MAP_AND_FLOW.md)

## When to read

Use **World Map & Flow — Zone layouts** (roles: architect, builder, narrative) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4. Ruined village layout (hub)](#4-ruined-village-layout-hub)
- [5. Tidal caves layout (linear with branch)](#5-tidal-caves-layout-linear-with-branch)
- [6. Dragon Palace Gate layout](#6-dragon-palace-gate-layout)


## 4. Ruined village layout (hub)

```
        [Torii / SC-03]
              |
    [Well save] — [Shack / Roku SC-04]
              |
    [Festival ground — banner inspect]
              |
    [Pier] — [Path to SC-05 crab]
              |
         [Cave entrance ↓]
```

| Landmark | Scene / function |
|----------|------------------|
| Well | Manual save + full heal first use |
| Shack | Shop, Roku, `cave_map` |
| Torii | Yuzu spirit SC-03 |
| Cave mouth | Zone load to `tidal_caves` |

**Quest pointer:** Soft arrow to torii after 2 inspects (`GAME_FEEL.md`).

---


## 5. Tidal caves layout (linear with branch)

```
[Entrance SC-06]
      ↓
[Flooded chamber SC-07 puzzle]
      ↓
[Deep pool SC-08]
      ↓
[Boss arena SC-09]
      ↓
[Shrine alcove SC-10]
      ↓
[Flashback wall SC-11]
      ↓
[Exit → Palace gate SC-12]
```

**Blockers:** SC-08 gated by `water_puzzle_solved`. SC-12 gated by `wraith_pearl`.

---


## 6. Dragon Palace Gate layout

```
[Exterior gate SC-12] — save point
      ↓
[Mirror chamber SC-13]
      ↓
[Sentinel hall SC-14]
      ↓
[Throne arena SC-15 → SC-16 choice]
```

No reverse-gravity rooms v1 (`STORYBOARD.md` SC-12).

---
