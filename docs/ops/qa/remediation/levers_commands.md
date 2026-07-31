---
id: levers-commands
type: how-to
audience: [qa, builder, visual]
status: active
authority: qa
tokens_est: 465
summary: "Lever taxonomy + commands"
---
# QA Remediation Loop — Lever taxonomy + commands

**Hub:** [`QA_REMEDIATION_LOOP.md`](../QA_REMEDIATION_LOOP.md)

## 3. Lever taxonomy (change one per attempt)

| Lever class | Examples | When to use |
|-------------|----------|-------------|
| `prompt` | Meshy/Tripo/ACE-Step text, negative prompts, reference image | Style/silhouette/mood wrong; jury M2/M6 or audio A3 fail |
| `tool_tier` | Meshy → Tripo → Rodin; procedural → ACE-Step | Same prompt failed twice |
| `mesh_ops` | Blender decimate ratio, subdiv, manual edge loop | Technical tris fail; M5 detail fail |
| `texture` | ComfyUI workflow, Material Maker, `palette_remap.py` zone | Muted palette fail; untextured kit |
| `shader_scene` | Toon ramp, emission, fog, light angle | In-scene visual fail but turntable PASS |
| `placement_camera` | GDAI reposition, gameplay camera screenshot | V5 silhouette in-scene only |
| `mastering` | ffmpeg `loudnorm`, loop points, trim tail | A2 LUFS/peak fail |

**Forbidden:** “Run jury again” without rebuilding. “Tweak jury min-pass.” “Mark WARN as PASS.”

---


## 4. Commands

```bash
# After vision jury FAIL
python3 tools/qa_remediation_brief.py \
  --jury artifacts/visual_reviews/phase1_ruined_village_gameplay.jury.json \
  --log-attempt

# After model jury FAIL
python3 tools/qa_remediation_brief.py \
  --jury artifacts/model_reviews/urashima.jury.json \
  --log-attempt

# After audio jury FAIL
python3 tools/qa_remediation_brief.py \
  --jury artifacts/audio_reviews/bgm_village.jury.json \
  --log-attempt

# After technical lint FAIL (no jury yet)
python3 tools/qa_remediation_brief.py --technical-model urashima
python3 tools/qa_remediation_brief.py --technical-audio bgm_village
```

---
