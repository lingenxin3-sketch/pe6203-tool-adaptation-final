# Round 2: independent results

Collected 2026-10-29T05:35:39+08:00 from `runs/repeat-r2-20261029`. Saved and scored: 162/162. Execution exceptions: 5, all retained.

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS |
|---|---:|---:|---:|---:|
| No update | 7.28 / 7.89 | 6.94 / 7.00 | 6.72 / 6.22 | 5.983 |
| Full rewrite | 6.72 / 6.56 | 6.61 / 7.28 | 6.89 / 7.11 | 5.611 |
| Selective patch | 7.17 / 7.39 | 6.28 / 6.33 | 5.78 / 7.17 | 4.597 |

## Cost

| Policy | Phase | Calls | Token | Request seconds | Local API USD |
|---|---|---:|---:|---:|---:|
| No update | update | 0 | 0 | 0.00 | 0.00 |
| No update | agent | 420 | 3088764 | 4497.17 | 0.00 |
| No update | judge | 54 | 424142 | 1610.91 | 0.00 |
| Full rewrite | update | 36 | 104413 | 304.55 | 0.00 |
| Full rewrite | agent | 403 | 2563956 | 3553.74 | 0.00 |
| Full rewrite | judge | 54 | 394719 | 1539.77 | 0.00 |
| Selective patch | update | 19 | 36449 | 113.19 | 0.00 |
| Selective patch | agent | 404 | 2873558 | 4169.57 | 0.00 |
| Selective patch | judge | 54 | 411512 | 1603.49 | 0.00 |

Selective patch uses 65.1% fewer update tokens than full rewrite. This is the update stage only. Local API charges exclude hardware and electricity; request seconds are cumulative request time, not full wall-clock runtime. Unreturned calls have unknown usage.

## Recovery and retention

| Policy | Version | Cohort | n | TF | Delta vs own Early | Delta vs same-round no update |
|---|---|---|---:|---:|---:|---:|
| No update | iter3 | changed | 9 | 7.00 | -0.56 | +0.00 |
| No update | iter3 | unaffected | 9 | 6.89 | -0.11 | +0.00 |
| No update | iter5 | changed | 10 | 6.80 | -1.00 | +0.00 |
| No update | iter5 | unaffected | 8 | 6.62 | +0.00 | +0.00 |
| Full rewrite | iter3 | changed | 9 | 6.67 | -0.89 | -0.33 |
| Full rewrite | iter3 | unaffected | 9 | 6.56 | +0.67 | -0.33 |
| Full rewrite | iter5 | changed | 10 | 8.10 | +0.30 | +1.30 |
| Full rewrite | iter5 | unaffected | 8 | 5.38 | +0.00 | -1.25 |
| Selective patch | iter3 | changed | 9 | 7.89 | +0.89 | +0.89 |
| Selective patch | iter3 | unaffected | 9 | 4.67 | -2.67 | -2.22 |
| Selective patch | iter5 | changed | 10 | 7.50 | +0.20 | +0.70 |
| Selective patch | iter5 | unaffected | 8 | 3.62 | -3.38 | -3.00 |

## Interpretation and evidence

R2 is not strictly comparable with R1: 123 of 162 actual resource lists differ, and all 54 within-round cross-policy input groups differ. Windows path visibility is an input confound; its causal contribution to scores has not been isolated. Keep this round separate. Selective patch has the lowest ECS here; do not extend the original round's ranking to R2.

Update tokens are 104,413 for full rewrite and 36,449 for selective patch. Three-stage totals are 3,063,088 and 3,321,519 respectively: selective patch uses 8.4% more recorded tokens. Neither metric establishes a causal policy effect under input confounding.

The publication gate passed at 05:37:57, commit `e7186eaed5f8206a813ec317381026fbddafae3a`; R3 actor execution started only after verification at 05:38:09. See [archive verification](../../artifacts/repeats-20261029/r2-independent-archive-verification.json) and [remote verification](../../artifacts/repeats-20261029/r2-independent-remote-verification.json).

All 27 task 28/113/117 cases were checked against pre-score execution originals without changing bytes or scores. Task 117/full rewrite/Late ended with an exception, empty answer, no task storage or successful history search, yet scored TF=10/PE=10. Task 113/no update/Late failed all seven planning validations and scored 1/4. Preserve both; neither automatic full marks nor a blanket rejection of the judge follows. See [R2 case review](ROUND_2_CASE_REVIEW.md).

[Frozen R2 evidence release](https://github.com/lingenxin3-sketch/pe6203-enterprise-tool-adaptation/releases/tag/project-evidence-20261029). ZIP SHA-256: `9c2c963d0b8fa02267a87034a398672442a10424f22dae81a4298587f137fceb`.

Fixed seed and temperature=0 repetitions are descriptive, not significance tests. Original task 113/117 judge disagreements remain. File existence does not establish correct contents or implementation. Reviews used AI assistance, not independent human annotation. The latest full report integrates all rounds; old PDF/figures remain historical. The dependency-expansion variant was not repeated. See [task 113](../CASE_113_REVIEW.md), [task 28](../CASE_28_REVIEW.md), and [task 117](../CASE_117_JUDGE_REVIEW.md).
