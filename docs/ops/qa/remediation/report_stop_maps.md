---
id: report-stop-maps
type: how-to
audience: [qa, builder, visual]
status: active
authority: qa
tokens_est: 601
summary: "Report template, stop rules, medium maps"
---
# QA Remediation Loop — Report template, stop rules, medium maps

**Hub:** [`QA_REMEDIATION_LOOP.md`](../QA_REMEDIATION_LOOP.md)

## 5. Agent report template (after FAIL)

```markdown
[QA REMEDIATION] asset=urashima attempt=2
  failed_criteria: m5_sufficient_detail (2/3 models)
  root_cause_class: mesh_ops + prompt
  lever_changed: tool_tier (Meshy → Tripo) + coat fold keywords in prompt
  do_not_repeat: same Meshy prompt; decimate 0.5 ratio (attempt 1)
  next_qa: check_model_technical.py → render_model_turntable.py → review_model_vision.py
  escalation_if_fail: manual Blender sculpt pass on coat; then human L6
```

---


## 6. Stop rules (prevents never-ending loops)

| Rule | Limit |
|------|-------|
| Same lever class twice | **Block** — must switch lever class or tool tier |
| Total automated attempts per asset | **3** — then escalate to human L6 or different primary tool |
| Same jury failure code 3× | **Escalate** — symptom may be wrong pipeline stage (e.g. blockout treated as beauty) |
| Re-screenshot without mesh change | **Invalid** if V1 primitives failed |

---


## 7. Medium-specific quick maps

### Model FAIL → typical fix order

1. Technical tris/textures → `mesh_ops` / `texture` (not new AI gen)
2. M1 block primitive → **regenerate** with `tool_tier` bump; do not texture a cube
3. M3 chibi → prompt proportions + negative “chibi, big head”
4. M5 low detail → lower decimate **or** higher-quality gen tier
5. Turntable PASS, in-scene FAIL → `shader_scene` + `VISUAL_QA.md` (not re-export GLB)

### Visual FAIL → typical fix order

1. V1 primitives → replace mesh (MODEL_QA path); lint before screenshot
2. V2 palette → `palette_remap.py` + zone fog/sky (`RENDERING_GUIDE.md`)
3. V3 PBR look → toon shader assignment (GDAI), not HDRI swap
4. V4 wrong culture motif → art swap per `ENVIRONMENT_KITS.md`, not lighting
5. V5 silhouette → camera distance or mesh scale, not bloom

### Audio FAIL → typical fix order

1. Placeholder source → ACE-Step (`generate_ai_bgm.sh`); never re-run procedural
2. LUFS/peak → `mastering` ffmpeg; do not re-compose
3. Wrong mood (jury) → `prompt` in `ace_step_prompts.json`; A/B one variable
4. Loop click → edit loop points (human or DAW); technical pass first

---
