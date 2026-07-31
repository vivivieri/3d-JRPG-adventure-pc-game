---
id: m3-jury
type: how-to
audience: [visual, qa]
status: active
authority: art
tokens_est: 525
summary: "python3 tools/render_model_turntable.py --model urashima"
---
# Model QA — Defense Layers — M3 turntable + jury

**Hub:** [`defense_layers.md`](../defense_layers.md)

### M3 — Turntable render (Blender)

```bash
python3 tools/render_model_turntable.py --model urashima
# → artifacts/model_reviews/urashima/{front,side,back,three_quarter}.png
```

Requires **Blender** (`install_extended_toolchain.sh`). Neutral grey studio + 4 orthographic-style views.


### M3b — Multi-LLM vision jury (hero + set-pieces)

```bash
python3 tools/review_model_vision.py --model urashima --min-pass 2
```

Sends **4 turntable PNGs** to vision models with `CHARACTER_BIBLE` / catalog brief.

**Hero jury scope** (`qa_catalog.json` → `hero_jury`): Urashima, Yuzu, Roku, torii, palace gate, lacquer box, Shore Wraith, Tide Keeper.

**Criteria (M1–M6):**

| # | Question |
|---|----------|
| M1 | Obvious **axis-aligned block** or untextured primitive? |
| M2 | **Stylized Japanese coastal** — not European castle / generic fantasy? |
| M3 | **Adult 1:5 proportions** — not chibi? |
| M4 | **Readable silhouette** at game distance (3/4 view)? |
| M5 | **Sufficient detail** for high-detail NPR target — not low-poly kitbash? |
| M6 | Matches model brief (coat, box, torii, etc.)? |
| M7 | **Emotional mood matches** generation brief (`docs/briefs/<id>.md`)? |
| M8 | **No forbidden tone** (comedy cheer, horror gore, bright Ghibli swagger)? |

**Pass:** ≥2 models `acceptance.valid_pass: true` (confidence ≥ 0.65, all M1–M8 met). Jury loads **Emotional intent** from generation brief when present. See `tools/generation_brief_lib.py`. Gate `L2_model_jury`.

**Note:** M7/M8 judge **art-direction emotional register** from stills — not animation feel or player enjoyment (human L6).


### Why turntable + in-game screenshot?

| Layer | Catches |
|-------|---------|
| Turntable jury | Bad mesh **before** Godot import |
| `VISUAL_QA.md` | Wrong material, lighting, zone palette **in context** |

Use **both**.

---
