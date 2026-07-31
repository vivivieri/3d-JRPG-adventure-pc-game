---
id: gates-plan
type: how-to
phase: [1, 6]
audience: [qa, release, builder]
status: active
authority: qa
tokens_est: 601
summary: "Gates relationship + plan"
---
# Perf — Procedure & Evidence — Gates relationship + plan

**Hub:** [`procedure_evidence.md`](../procedure_evidence.md)

## 9. Relationship to gates

| Gate | What it checks | Baseline needed? |
|------|----------------|------------------|
| `L2_perf_catalog` | `perf_thresholds.json` + `perf_baseline.json` valid | No — runs anywhere |
| `L3_perf_review` | FPS, draw calls, materials after F5 | **Yes** — Linux snapshot and/or Windows PC |
| `L6_human_playtest` | Feel, fun, readability | Human machine noted in report |

---



## 10. Implementation plan

### Phase 1 — P1-00 (bootstrap)

| Task | Owner | Done when |
|------|-------|-----------|
| `game/project.godot` on `game/development` | PM / Architect | CI boot gate runs |
| Medium graphics preset keys in settings | Architect | `graphics_quality` applies `RENDERING_GUIDE.md` §10 |
| Document baseline in PR template | PM | ✅ this doc + `perf_baseline.json` |

### Phase 2 — P1-02 (ruined village)

| Task | Owner | Done when |
|------|-------|-----------|
| First `ruined_village` scene playable | Builder | F5 clean |
| First perf evidence JSON | Builder | `artifacts/perf_reviews/ruined_village_*.json` on reference PC |
| Gate report cites baseline | QA | PR shows `L3_perf_review: PASS` |

### Phase 3 — M5 (art pass)

| Task | Owner | Done when |
|------|-------|-----------|
| Perf evidence per ship zone | Builder + QA | All `perf_thresholds.json` zones have JSON |
| Remediation loop for FAIL | QA | `qa_emit_remediation.sh` perf brief |
| ≤ 8 materials enforced per zone | Builder | snapshot + visual review |

### Phase 4 — M6 (Steam ship)

| Task | Owner | Done when |
|------|-------|-----------|
| Exported `.exe` perf on reference PC | Release + QA | `editor_vs_export: export` in evidence |
| `steam_minimum` spot-check | Human QA | 720p Low ≥ 30 FPS documented |
| `STEAM_RELEASE_CHECKLIST.md` §2.11 | Release | Windows hardware row checked |

### Optional automation (later)

| Item | Notes |
|------|-------|
| `tools/validate_perf_evidence.py` | Lint evidence JSON against schema |
| CI upload of perf artifacts | Store in GitHub Actions artifacts — still not valid for ship PASS |
| Dedicated reference hardware label | GitHub self-hosted runner or QA bench sticker |

---
