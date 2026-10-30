# Comparable descriptive analysis: R1 + R3

Collected 2026-10-29T11:26:27+08:00. Includes `final-v1` and `final-r3` only: 324 observations, 18 distinct tasks, twice per task/policy/version combination. R2 remains separate because resource-list mismatches were found before scoring. This is not a three-round or 486-observation comparable summary.

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS |
|---|---:|---:|---:|---:|
| No update | 6.44±0.55 / 6.75±0.27 | 7.39±0.16 / 7.28±0.08 | 7.11±0.47 / 7.25±0.90 | 5.605±0.956 |
| Full rewrite | 6.58±0.43 / 7.39±0.16 | 6.83±0.31 / 7.47±0.51 | 7.14±0.59 / 7.58±0.59 | 5.289±0.071 |
| Selective patch | 7.42±0.43 / 7.28±0.08 | 7.33±0.39 / 7.50±0.16 | 6.86±0.43 / 7.28±0.16 | 6.242±0.127 |

The ± values are sample SDs of two round means (n=2), not SDs across 18 tasks, confidence intervals, or significance tests. The population SD inside the original ECS formula remains unchanged.

## Recorded cost across the two comparable rounds

| Policy | Phase | Calls | Token | Request seconds | Local API USD |
|---|---|---:|---:|---:|---:|
| No update | update | 0 | 0 | 0.00 | 0.00 |
| No update | agent | 851 | 5993184 | 32620.29 | 0.00 |
| No update | judge | 108 | 823400 | 3295.60 | 0.00 |
| Full rewrite | update | 72 | 208898 | 660.07 | 0.00 |
| Full rewrite | agent | 804 | 5338700 | 15384.36 | 0.00 |
| Full rewrite | judge | 108 | 795326 | 4712.60 | 0.00 |
| Selective patch | update | 38 | 72898 | 235.25 | 0.00 |
| Selective patch | agent | 810 | 5832127 | 9206.16 | 0.00 |
| Selective patch | judge | 108 | 794178 | 5698.87 | 0.00 |

Selective patch saves 65.1% of update tokens. Full rewrite uses 6,342,924 total recorded tokens across update, agent, and judge; selective patch uses 6,699,203, a +5.6% change. Request seconds are cumulative request durations, not full wall-clock runtime. Local API zero billing excludes electricity, hardware, and development. Unreturned calls, including historical interrupted judge requests, have unknown costs.

## Provenance, denominators, and limits

The [comparison JSON](../../artifacts/repeats-20261029/original-r3-comparison.json) contains complete metrics, separate round values, recovery, and retention. `cohorts.n` and `n_observations` count repeated observations; `distinct_tasks` counts tasks. Each policy/version has 18 tasks and 36 observations.

The [paired index](../../artifacts/repeats-20261029/original-r3-paired-evidence.json) contains 162 same-task/version/policy cross-round pairs and source hashes. One R1 public ZIP JSON differs in serialization from the local frozen copy but has identical values/types. Both raw hashes are retained; see [source verification](../../artifacts/repeats-20261029/original-public-evidence-verification.json). No old records were rewritten.

Eligibility was [declared before R3 judging](FROZEN_PROTOCOL.md). Fixed seed and temperature=0 describe stability under these settings; repetitions are not additional independent tasks. Early differences precede updates and cannot be counted as adaptation effects. No universal superiority or sentence-level causal claim follows.

The first 39 original judge calls used a 16384 client guard; later 123 calls and new rounds use 24576. The server was always 24576. Maximum first-39 reservation was 15505, all 162 original calls have zero dropped messages, and first-39 hashes match the incident archive. Retained judging inputs were unaffected, although client implementations were not identical. See [context verification](../../artifacts/repeats-20261029/original-effective-context-verification.json).

Automatic scores are not actual success rates. Keep known task 113/117 judge blind spots, under-updating, and over-updating evidence: [R2 cases](ROUND_2_CASE_REVIEW.md), [R3 cases](ROUND_3_CASE_REVIEW.md). Reviews used AI assistance and do not replace independent human annotation. The original dependency-expansion variant remains a single auxiliary experiment. The latest report includes this analysis; older PDF/figures cover R1 only.
