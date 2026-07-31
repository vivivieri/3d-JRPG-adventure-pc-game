---
id: commands-refs
type: how-to
phase: [1, 6]
audience: [qa, release, builder]
status: active
authority: qa
tokens_est: 278
summary: "bash tools/run_perf_review_checks.sh"
---
# Perf — Procedure & Evidence — Commands + related

**Hub:** [`procedure_evidence.md`](../procedure_evidence.md)

## 11. Commands

```bash
# Validate baseline + thresholds catalogs (L2 — any environment)
bash tools/run_perf_review_checks.sh

# After capture — manual check of evidence file
python3 -m json.tool artifacts/perf_reviews/ruined_village_abc1234.json
```

---



## 12. Related docs

| Doc | Contents |
|-----|----------|
| `docs/ops/qa/PLATFORM_SUPPORT.md` | **Linux + Windows ship policy; cloud dev parity** |
| `docs/design/art/RENDERING_GUIDE.md` §10 | Low / Medium / High presets |
| `docs/design/world/ENVIRONMENT_KITS.md` §9 | LOD + material batching |
| `docs/ops/cheat-sheets/RR_CHEATSHEET.md` | Performance review workflow |
| `docs/ops/qa/QA_AND_BUG_PROCESS.md` §6 | Post-fix regression |
| `steam/STORE_PAGE.md` | Public system requirements |
| `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md` | M6 hardware smoke |
