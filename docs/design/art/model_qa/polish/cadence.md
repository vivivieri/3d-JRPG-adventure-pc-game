---
id: cadence
type: how-to
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 661
summary: "“Keep tweaking until it feels right” without a ladder produces infinite retries or random prompt changes."
---
# Model QA — Polish Direction — Polish cadence

**Hub:** [`polish_direction.md`](../polish_direction.md)

## 8. Model polish cadence (structured iteration)

**Problem:** “Keep tweaking until it feels right” without a ladder produces infinite retries or random prompt changes.

**Rule:** Polish is **gate-driven**. Each attempt changes **one lever** (`docs/ops/qa/QA_REMEDIATION_LOOP.md` §3), logs to `revision_log.json`, and re-runs the **full** model layer — not jury-only reruns.

### 8.1 Attempt ladder (default per asset)

| Attempt | Goal | Primary levers | Exit when |
|---------|------|----------------|-----------|
| **0 — Gen** | First shippable candidate | `prompt` + `tool_tier` (Meshy/Tripo/Rodin) | Technical PASS |
| **1 — Read** | On-brand silhouette | `mesh_ops` (Blender sculpt/decimate) or `prompt` if M2/M3/M6 fail | Turntable jury PASS (M1–M6) |
| **2 — Context** | Reads in zone + motion | `texture` + `shader_scene` + GDAI placement | `VISUAL_QA` gameplay screenshot PASS |
| **3 — Feel** | Human enjoyment | Human L6 feedback → brief/doc update → **one** rebuild lever | `PLAYTEST_SCRIPT.md` §7b avg ≥3.5 (≥5 testers) |

After **3 automated attempts** with no PASS → **escalate** (tool tier ↑, manual Blender pass, or human L6 waiver with evidence). Same lever class twice → **blocked** (`QA_REMEDIATION_LOOP.md` §6).

### 8.2 Polish commands (one full pass)

```bash
MODEL=urashima
python3 tools/check_model_technical.py --model "$MODEL" --ship
python3 tools/render_model_turntable.py --model "$MODEL"
python3 tools/review_model_vision.py --model "$MODEL" --min-pass 2
# GDAI: import, zone placement, gameplay screenshot
python3 tools/check_screenshot_palette.py --zone ruined_village --screenshot artifacts/screenshots/phase1_ruined_village_gameplay.png
bash tools/run_model_smoke_checks.sh
```

On FAIL: `bash tools/qa_emit_remediation.sh model-tech|model-jury <args>` — apply **one** action from the brief before the next attempt.

### 8.3 What “polish” is not

| Invalid | Why |
|---------|-----|
| Re-run jury without rebuilding GLB | Symptom unchanged |
| Tweaking `min-pass` or marking WARN as PASS | Gate shopping |
| Agent “looks fine to me” without jury + screenshot | No measurable evidence |
| More than 3 automated loops on same failure code | Escalate per stop rules |
| Builder changes mesh without Architect brief / failed criterion | R&R violation — direction must be traceable |

---
