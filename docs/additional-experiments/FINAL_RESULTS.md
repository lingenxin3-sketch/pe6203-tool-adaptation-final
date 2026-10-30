# Current results and evidence

The active comparison contains 486 scored observations over 18 distinct tasks and three comparable rounds. Selective patch uses 65.1% fewer update tokens than full rewrite, but 5.5% more recorded total tokens. ECS means are 5.498 / 5.354 / 5.913 for no update / full rewrite / selective patch. All 10 execution exceptions remain included. The superseded input-incompatible round and one uncommitted interrupted attempt are preserved separately.

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS mean +/- SD |
| --- | ---: | ---: | ---: | ---: |
| No update | 6.69 / 6.96 | 6.80 / 7.20 | 7.33 / 7.41 | 5.498 +/- 0.701 |
| Full rewrite | 6.54 / 7.20 | 6.67 / 7.30 | 7.41 / 7.91 | 5.354 +/- 0.123 |
| Selective patch | 7.28 / 7.54 | 7.15 / 7.31 | 6.63 / 7.17 | 5.913 +/- 0.577 |

Corrected R2 is included using predeclared input criteria; all 162 actual resource lists match R1 and 54 cross-policy groups agree. Its selective ECS is below both baselines. All 10 active-grid execution exceptions remain scored. The 156 records committed before the monitoring interruption remain preserved, and the unfinished attempt is archived.

- [Three-round comparison](COMPARABLE_THREE_ROUNDS.md).
- [Corrected second-round results](ROUND_2_RESULTS.md) and [cases](ROUND_2_CASE_REVIEW.md).
- [Completion receipt](../../artifacts/rerun-r2-20261030/completion.json).
- [Evidence index](../EVIDENCE.md).
- [Full report](../REPORT.md).

The seven returned calls from the interrupted attempt add 75,652 known tokens outside the completed-grid totals. Costs for unreturned calls remain unknown. Do not claim statistical significance, lower total token use or universal method superiority.
