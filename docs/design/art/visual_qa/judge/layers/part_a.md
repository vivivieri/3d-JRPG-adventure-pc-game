---
id: part-a
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 590
summary: "Visual QA — Defense Layers (A)"
---
# Visual QA — Defense Layers — Visual QA — Defense Layers (A)

**Hub:** [`defense_layers.md`](../defense_layers.md)

### Layer A — Static scene lint (before commit)

```bash
bash tools/check_scene_visuals.sh
```

Fails if player-facing `.tscn` files contain banned primitive mesh types (`BoxMesh`, `CapsuleMesh`, etc.) or Kenney castle assets. Greybox paths (`greybox/`, `_dev/`, `*.greybox.tscn`) are excluded.

**Run in:** `run_playtest_smoke.sh`, Phase 1+ PRs, M5 gate.

`bash tools/run_visual_smoke_checks.sh` runs palette + multi-LLM jury when `artifacts/screenshots/phase1_<zone>_gameplay.png` exists; **WARNs and skips** until Phase 1 captures screenshots.


### Layer B — Mandatory screenshot (every zone/UI task)

Per `docs/ops/qa/AI_TESTING_SPEC.md` §5.2 step 7:

1. GDAI MCP (or Godotiq / MCP Pro) captures **gameplay camera** viewport at **1920×1080**
2. Save to `artifacts/screenshots/<phase>_<scene>_<view>_<date>.png`
3. Agent **must open and analyze the image** — not only record the path

**Minimum views per zone (Phase 1+):**

| View | Camera |
|------|--------|
| Establishing | Wide — silhouette read (torii, gate, hub layout) |
| Gameplay | Default follow / exploration height |
| Detail | Nearest hero prop (well, box, lantern) |


### Layer C — Vision checklist (agent procedure)

After screenshot, agent answers **in the session report** (yes/no + evidence):

| # | Question | Fail if |
|---|----------|---------|
| V1 | Any obvious grey/brown **axis-aligned boxes** visible? | Primitive placeholder |
| V2 | Palette muted coastal (fog grey, weathered wood) — not candy/sunny anime? | `ART_DIRECTION.md` §1 |
| V3 | Single toon/NPR read — not glossy PBR skin or HDRI sky? | `RENDERING_GUIDE.md` |
| V4 | Japanese coastal motifs — no European castle/medieval read? | `ART_DIRECTION.md` §9 |
| V5 | Hero silhouette readable at gameplay distance? | `CHARACTER_BIBLE.md` |
| V6 | UI: no pink font boxes, no clipped dialogue? | `UI_UX_FLOW.md` |

**If any V1–V6 fails → task is FAIL** even if Godot Output is clean. Replace assets; re-screenshot.

**On FAIL:** `python3 tools/qa_remediation_brief.py --jury <path>.jury.json --log-attempt` — see `docs/ops/qa/QA_REMEDIATION_LOOP.md`.
