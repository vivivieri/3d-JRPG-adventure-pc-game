---
id: smoke-workflow
type: how-to
phase: [1, 5]
audience: [audio, qa]
status: active
authority: audio
tokens_est: 537
summary: "L2 smoke, agent workflow, report template"
---
# Audio QA — L2 smoke, agent workflow, report template

**Hub:** [`AUDIO_QA.md`](../AUDIO_QA.md)

## When to read

Use **Audio QA — L2 smoke, agent workflow, report template** (roles: audio, qa) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [3. L2 smoke integration](#3-l2-smoke-integration)
- [4. Agent workflow](#4-agent-workflow)
- [BGM](#bgm)
- [P0 VO](#p0-vo)
- [5. Agent report template](#5-agent-report-template)


## 3. L2 smoke integration

```bash
bash tools/run_audio_smoke_checks.sh
```

| State | Behavior |
|-------|----------|
| No `bgm_village.ogg` | **WARN** — BGM smoke skip (Phase 1 not ready) |
| No P0 VO `en` clip | **WARN** — VO smoke skip until ElevenLabs batch |
| Placeholder + dev mode | **WARN** — replace with ACE-Step before M5 |
| Placeholder + `--ship` | **FAIL** |
| ACE-Step export wrong LUFS | **FAIL** |
| Hero BGM jury, no API keys | **WARN** — manual packet |
| P0 VO jury, no API keys | **WARN** — manual packet |

Wired into `bash tools/run_playtest_smoke.sh`.

---


## 4. Agent workflow

### BGM

```
1. bash tools/generate_ai_bgm.sh --track bgm_village --api
2. Loudness normalize toward −16 LUFS in DAW/ffmpeg if needed
3. python3 tools/register_asset.py add --path <path> ...
4. python3 tools/check_audio_catalog.py --phase 1
5. python3 tools/check_audio_technical.py --track bgm_village
6. python3 tools/review_audio_vision.py --track bgm_village  (hero tracks)
7. GDAI MCP — wire in editor, F5 zone test
```

### P0 VO

```
1. bash tools/generate_ai_vo.sh --clip sc00_urashima_01 --locale en --locale ja --locale zh
2. python3 tools/check_audio_vo.py --clip sc00_urashima_01 --locale en
3. python3 tools/review_vo_vision.py --clip sc00_urashima_01 --locale en
4. Repeat technical for all locales; jury gate on en only
5. GDAI MCP — F5 scene with subtitles + duck_bgm_db
```

---


## 5. Agent report template

```
[AUDIO QA] track=bgm_village
  catalog phase1: PASS
  technical: PASS (I=-16.2 LUFS, peak=-2.1 dBTP)
  placeholder: NO (ACE-Step)
  jury: PASS (2/2) — artifacts/audio_reviews/bgm_village.jury.json
  result: PASS
```

---
