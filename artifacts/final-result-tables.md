# Current three-round result tables

The active comparison contains 486 scored observations over 18 distinct tasks and three comparable rounds. Selective patch uses 65.1% fewer update tokens than full rewrite, but 5.5% more recorded total tokens. ECS means are 5.498 / 5.354 / 5.913 for no update / full rewrite / selective patch. All 10 execution exceptions remain included. The superseded input-incompatible round and one uncommitted interrupted attempt are preserved separately.

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS mean +/- SD |
| --- | ---: | ---: | ---: | ---: |
| No update | 6.69 / 6.96 | 6.80 / 7.20 | 7.33 / 7.41 | 5.498 +/- 0.701 |
| Full rewrite | 6.54 / 7.20 | 6.67 / 7.30 | 7.41 / 7.91 | 5.354 +/- 0.123 |
| Selective patch | 7.28 / 7.54 | 7.15 / 7.31 | 6.63 / 7.17 | 5.913 +/- 0.577 |

## Recovery and retention

| Policy | Version | Cohort | Tasks / observations | TF | Recovery or retention |
| --- | --- | --- | ---: | ---: | ---: |
| No update | Middle | changed | 9 / 27 | 7.48 | +0.00 |
| No update | Middle | unaffected | 9 / 27 | 6.11 | -0.37 |
| No update | Late | changed | 10 / 30 | 7.67 | +0.00 |
| No update | Late | unaffected | 8 / 24 | 6.92 | +0.88 |
| Full rewrite | Middle | changed | 9 / 27 | 7.56 | +0.07 |
| Full rewrite | Middle | unaffected | 9 / 27 | 5.78 | +0.04 |
| Full rewrite | Late | changed | 10 / 30 | 7.83 | +0.17 |
| Full rewrite | Late | unaffected | 8 / 24 | 6.88 | +1.67 |
| Selective patch | Middle | changed | 9 / 27 | 7.44 | -0.04 |
| Selective patch | Middle | unaffected | 9 / 27 | 6.85 | -0.37 |
| Selective patch | Late | changed | 10 / 30 | 7.13 | -0.53 |
| Selective patch | Late | unaffected | 8 / 24 | 6.00 | -1.04 |

## Recorded costs

| Policy | Phase | Calls | Tokens | Request seconds |
| --- | --- | ---: | ---: | ---: |
| No update | update | 0 | 0 | 0.00 |
| No update | agent | 1285 | 9,133,062 | 37234.02 |
| No update | judge | 162 | 1,242,483 | 4203.26 |
| Full rewrite | update | 108 | 313,370 | 932.83 |
| Full rewrite | agent | 1214 | 8,199,730 | 19041.92 |
| Full rewrite | judge | 162 | 1,209,904 | 5638.78 |
| Selective patch | update | 57 | 109,347 | 336.24 |
| Selective patch | agent | 1232 | 8,948,412 | 12700.07 |
| Selective patch | judge | 162 | 1,197,677 | 6588.86 |
