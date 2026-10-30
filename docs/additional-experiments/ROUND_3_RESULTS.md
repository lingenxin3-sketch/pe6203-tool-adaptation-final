# Round 3: results for this round

Collected 2026-10-29T10:52:08+08:00 from `runs/final-r3`. Saved and scored: 162/162. Execution exceptions: 5, all retained.

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS |
|---|---:|---:|---:|---:|
| No update | 6.06 / 6.94 | 7.50 / 7.22 | 6.78 / 6.61 | 4.929 |
| Full rewrite | 6.89 / 7.28 | 6.61 / 7.11 | 7.56 / 8.00 | 5.340 |
| Selective patch | 7.72 / 7.22 | 7.06 / 7.39 | 6.56 / 7.17 | 6.152 |

## Cost

| Policy | Phase | Calls | Token | Request seconds | Local API USD |
|---|---|---:|---:|---:|---:|
| No update | update | 0 | 0 | 0.00 | 0.00 |
| No update | agent | 425 | 2985646 | 5416.09 | 0.00 |
| No update | judge | 54 | 416731 | 1622.19 | 0.00 |
| Full rewrite | update | 36 | 104426 | 300.76 | 0.00 |
| Full rewrite | agent | 401 | 2656393 | 4182.16 | 0.00 |
| Full rewrite | judge | 54 | 397538 | 1570.82 | 0.00 |
| Selective patch | update | 19 | 36449 | 112.17 | 0.00 |
| Selective patch | agent | 405 | 2846206 | 3432.71 | 0.00 |
| Selective patch | judge | 54 | 385204 | 1521.62 | 0.00 |

Selective patch uses 65.1% fewer update tokens than full rewrite. This is the update stage only. Local API charges exclude hardware and electricity; request seconds are cumulative request time, not full wall-clock runtime. Unreturned calls have unknown usage.

## Recovery and retention

| Policy | Version | Cohort | n | TF | Delta vs own Early | Delta vs same-round no update |
|---|---|---|---:|---:|---:|---:|
| No update | iter3 | changed | 9 | 8.33 | +2.22 | +0.00 |
| No update | iter3 | unaffected | 9 | 6.67 | +0.67 | +0.00 |
| No update | iter5 | changed | 10 | 7.30 | +0.80 | +0.00 |
| No update | iter5 | unaffected | 8 | 6.12 | +0.62 | +0.00 |
| Full rewrite | iter3 | changed | 9 | 8.22 | +0.22 | -0.11 |
| Full rewrite | iter3 | unaffected | 9 | 5.00 | -0.78 | -1.67 |
| Full rewrite | iter5 | changed | 10 | 7.40 | -0.80 | +0.10 |
| Full rewrite | iter5 | unaffected | 8 | 7.75 | +2.50 | +1.62 |
| Selective patch | iter3 | changed | 9 | 8.00 | -0.67 | -0.33 |
| Selective patch | iter3 | unaffected | 9 | 6.11 | -0.67 | -0.56 |
| Selective patch | iter5 | changed | 10 | 7.40 | -1.40 | +0.10 |
| Selective patch | iter5 | unaffected | 8 | 5.50 | -0.88 | -0.62 |

## Interpretation and evidence

All 162 R3 resource lists match R1 and its 54 cross-policy groups agree. Its original scores and failure records remain unchanged. R3 is now included with R1 and corrected R2 in the current 486-observation comparison. See [current results](FINAL_RESULTS.md) for this active selection; earlier two-round analyses are historical snapshots. Fixed-setting repeats do not establish statistical significance or universal superiority.

Selective patch has the highest original automatic ECS in R3 (6.152), which is not a task success rate. Update tokens are 104,426 for full rewrite and 36,449 for selective patch, a 65.1% reduction. Three-stage totals are 3,158,357 and 3,267,859: selective patch uses 3.5% more recorded tokens.

The publication gate passed at 10:55:24 and the controller was observed exiting normally. Anonymous archive verification checked all 909 manifest entries, their sizes, SHA values, and CRCs: 162 results, 162 agent copies, 162 event files, five original failures, and closed phase logs. The original local serialization copy also has the expected raw SHA. See [archive verification](../../artifacts/repeats-20261029/r3-independent-archive-verification.json) and [remote verification](../../artifacts/repeats-20261029/r3-independent-remote-verification.json).

[R3 case review](ROUND_3_CASE_REVIEW.md) compares 27 selected cases and all five exceptions with calls/files. Task 117/selective patch/Early and task 113/no update/Late retain misleading 10/10 scores; task 28/full rewrite/Middle and Late received 1/4 that identified failures. Do not claim all scores are correct or all are invalid. Supplementary analysis is available in this final repository's documentation and evidence files; the frozen R3 ZIP retains its original contents.

[Frozen R3 evidence release in the historical mirror](https://github.com/lingenxin3-sketch/pe6203-enterprise-tool-adaptation/releases/tag/project-evidence-20261029). ZIP SHA-256: `402d9a8005bc5848890fc60919dac4eef531ccf2a96a750e6b5c67f920f34c8c`.

Fixed seed and temperature=0 repetitions are descriptive, not significance tests. Original task 113/117 judge disagreements remain. File existence does not establish correct contents or implementation. Reviews used AI assistance, not independent human annotation. The latest full report integrates all rounds; old PDF/figures remain historical. The dependency-expansion variant was not repeated. See [task 113](../CASE_113_REVIEW.md), [task 28](../CASE_28_REVIEW.md), and [task 117](../CASE_117_JUDGE_REVIEW.md).
