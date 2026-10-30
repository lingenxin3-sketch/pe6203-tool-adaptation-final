# Corrected second round results

The formal second round is now `final-r2`, completed on 30 October 2026. All 162 records are scored, one execution exception remains included, all 162 resource listings match R1, and all 54 cross-policy input groups agree.

### R2 final-r2

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS |
| --- | ---: | ---: | ---: | ---: |
| No update | 7.17 / 7.39 | 5.61 / 7.06 | 7.78 / 7.72 | 5.285 |
| Full rewrite | 6.44 / 6.83 | 6.33 / 6.94 | 7.94 / 8.56 | 5.484 |
| Selective patch | 7.00 / 8.06 | 6.78 / 6.94 | 6.17 / 6.94 | 5.255 |

Selective patch does not lead this round: ECS 5.255 versus full rewrite 5.484 and no update 5.285. Inclusion was declared on input criteria before scores were observed. A monitoring interruption and one uncommitted attempt restart are retained in [the interruption record](../../artifacts/rerun-r2-20261030/monitor-memory-interruption-20261030.json). The earlier incompatible R2 remains historical, not pooled.

[Raw evidence ZIP](../../artifacts/evidence/final-r2-evidence.zip) · [Current pooled comparison](COMPARABLE_THREE_ROUNDS.md).
