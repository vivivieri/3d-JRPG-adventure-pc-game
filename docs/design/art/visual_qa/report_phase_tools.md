---
id: report-phase-tools
type: how-to
audience: [visual, builder, qa]
phase: [1, 5]
status: active
authority: art
tokens_est: 512
summary: "Visual QA — Report template, phase gates, tools — [VISUAL QA] scene=ruined_village.tscn zone=ruined_village"
---
# Visual QA — Report template, phase gates, tools

**Hub:** [`VISUAL_QA.md`](../VISUAL_QA.md)

## When to read

Use **Visual QA — Report template, phase gates, tools** (roles: visual, builder, qa) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4. Agent report template (paste every visual task)](#4-agent-report-template-paste-every-visual-task)
- [5. Phase gates](#5-phase-gates)
- [6. Related tools](#6-related-tools)


## 4. Agent report template (paste every visual task)

```
[VISUAL QA] scene=ruined_village.tscn zone=ruined_village
  check_scene_visuals.sh: PASS
  screenshots:
    - artifacts/screenshots/phase1_ruined_village_establishing.png
    - artifacts/screenshots/phase1_ruined_village_gameplay.png
  palette_check: PASS (avg distance 0.12)
  vision_jury: PASS (2/3 models — see artifacts/visual_reviews/phase1_ruined_village_gameplay.jury.json)
  vision V1 primitives visible: NO
  vision V2 muted palette: YES
  vision V3 NPR not PBR: YES
  vision V4 Japanese coastal: YES
  vision V5 silhouette read: YES
  vision V6 UI clean: N/A (zone only)
  result: PASS
```

---


## 5. Phase gates

| Phase | Visual requirement |
|-------|-------------------|
| 1 — ruined_village | SC-02 §10 checklist + screenshots + `check_scene_visuals.sh` |
| 2–6 | Same per touched zone scene |
| 7 — M5 | Zero primitive lint failures; golden masters for all zones |
| 8 — ship | L6 human + compliance |

---


## 6. Related tools

| Tool | Role |
|------|------|
| `tools/check_scene_visuals.sh` | Static primitive / banned asset scan |
| `tools/check_screenshot_palette.py` | Post-screenshot palette distance |
| `tools/palette_remap.py` | Pre-import texture palette |
| `tools/run_visual_smoke_checks.sh` | L2 smoke: palette + jury (WARN until screenshots) |
| `tools/review_screenshot_vision.py` | Multi-LLM vision jury (2-of-N consensus) |
| `tools/check_asset_compliance.sh` | **License** only — not visual QA |

**Do not confuse** license compliance with look-and-feel approval.
