# Final results and evidence verification

[Latest full report PDF](../../output/pdf/PE6203_Project4_Final_Report.pdf) · [Report source](../REPORT.md) · [Team responsibilities](../../README.md#team-responsibilities).

All three rounds are executed and scored. Values come from records completed on 2026-10-29. This English documentation edition does not rerun experiments, change scores, or replace evidence archives.

## Completion

| Round | Scored / planned | Execution exceptions | ECS: no update / full rewrite / selective patch |
|---|---:|---:|---|
| R1: final-v1 | 162 / 162 | 4 | 6.280 / 5.239 / 6.332 |
| R2: repeat-r2-20261029 | 162 / 162 | 5 | 5.983 / 5.611 / 4.597 |
| R3: final-r3 | 162 / 162 | 5 | 4.929 / 5.340 / 6.152 |

All exceptions remain in the 486 scored observations. A valid score is not actual task success.

## Supported interpretation

R2 has 123 cross-round resource-list mismatches and 54 mismatched cross-policy input groups. It is preserved separately, not pooled as a third comparable repetition. R1/R3 match all 162 resource lists and 54 fairness groups each. Under the comparison criteria declared before R3 scoring, they form a 324-observation descriptive comparison: 18 distinct tasks, twice per combination.

| Comparable R1 + R3 | No update | Full rewrite | Selective patch |
|---|---:|---:|---:|
| Mean ECS ± sample SD of two round means | 5.605 ± 0.956 | 5.289 ± 0.071 | 6.242 ± 0.127 |
| Update tokens | 0 | 208,898 | 72,898 |
| Recorded tokens: update + agent + judge | 6,816,584 | 6,342,924 | 6,699,203 |

Selective patch uses 65.1% fewer update tokens than full rewrite but 5.6% more total recorded tokens. It has the higher comparable mean ECS; TF/PE, recovery, and retention remain mixed. R2 gives selective patch the lowest ECS, which must remain visible; input confounding prevents isolating its cause.

The SD uses n=2 round means, not a confidence interval. Fixed seed=6203 and temperature=0 repetitions describe stability, not more independent tasks, significance, or universal superiority. Early score differences occur before updates and cannot all be attributed to the method.

## Results, cases, and original evidence

The [evidence index](../EVIDENCE.md) provides byte-preserving archive copies in this repository with original release provenance.

- [R2 independent results](ROUND_2_RESULTS.md) and [R3 independent results](ROUND_3_RESULTS.md).
- [R1 + R3 TF/PE/ECS, cost, recovery, and retention](COMPARABLE_R1_R3.md).
- [R2 cases](ROUND_2_CASE_REVIEW.md) and [R3: 27 selected cases plus all five exceptions](ROUND_3_CASE_REVIEW.md).
- [Complete comparison JSON](../../artifacts/repeats-20261029/original-r3-comparison.json) and [162 pairs with source hashes](../../artifacts/repeats-20261029/original-r3-paired-evidence.json).

| Frozen release | Contents | ZIP SHA-256 |
|---|---|---|
| [R1 v1.0.0](https://github.com/lingenxin3-sketch/pe6203-enterprise-tool-adaptation/releases/tag/project-evidence-20261029) | Original round, original auxiliary/development validation, original report and documents | `f0df5bdecbfc840cfd8b58555733ad5a4bfe99ad742fdedbd6b1f500dbc19fad` |
| [R2](https://github.com/lingenxin3-sketch/pe6203-enterprise-tool-adaptation/releases/tag/project-evidence-20261029) | 162 results, traces, outputs, failures | `9c2c963d0b8fa02267a87034a398672442a10424f22dae81a4298587f137fceb` |
| [R3](https://github.com/lingenxin3-sketch/pe6203-enterprise-tool-adaptation/releases/tag/project-evidence-20261029) | 162 results/agent copies/events, five original failures, closed logs; 909 manifest entries | `402d9a8005bc5848890fc60919dac4eef531ccf2a96a750e6b5c67f920f34c8c` |

Both additional ZIPs were anonymously downloaded and checked for sizes, SHA values, and CRCs. Frozen ZIPs are unchanged. Paired analysis and post-score case tables were added as branch files after release, not retroactively placed inside the ZIPs. See the [original acceptance archive](../archive/ACCEPTANCE_CHECKLIST_ORIGINAL.md).

## Historical verification index

These 21 receipts refer to the original experiment-delivery snapshots and commits. They do not verify every later documentation edit. In particular, preservation of main describes the experiment-completion point; later authorized documentation cleanup changed main and the submission branch without modifying raw experiment data, tags, or releases.

<details>
<summary>Original experiment-delivery checks</summary>

| Historical check | Status at experiment delivery | Receipt |
|---|---|---|
| Complete unique 18-task / 3-policy / 3-version matrix | Verified at that time | [preflight.json](../../artifacts/repeats-20261029/preflight.json)、[repeat-r2-20261029-metrics.json](../../artifacts/repeats-20261029/repeat-r2-20261029-metrics.json)、[final-r3-metrics.json](../../artifacts/repeats-20261029/final-r3-metrics.json) |
| At most two additional rounds; development and auxiliary variants excluded | Verified at that time | [smoke-verification.json](../../artifacts/repeats-20261029/smoke-verification.json)、[3-round-combination-refused.json](../../artifacts/repeats-20261029/3-round-combination-refused.json) |
| Original configuration, models, code, and dependencies frozen before execution | Verified at that time | [preflight.json](../../artifacts/repeats-20261029/preflight.json)、[runtime-dependency-verification.json](../../artifacts/repeats-20261029/runtime-dependency-verification.json)、[final-preservation-verification.json](../../artifacts/repeats-20261029/final-preservation-verification.json) |
| Preparation page published and read back before formal execution | Verified at that time | [final-independent-statistics-and-order-verification.json](../../artifacts/repeats-20261029/final-independent-statistics-and-order-verification.json) |
| Model-free tests, real development workflow, and resume-skip verification | Verified at that time | [test-receipt.json](../../artifacts/repeats-20261029/test-receipt.json)、[smoke-verification.json](../../artifacts/repeats-20261029/smoke-verification.json) |
| Timestamped progress including the pre-08:00 snapshot | Verified at that time | [first-automatic-progress-verification.json](../../archive/progress/repeats-20261029/first-automatic-progress-verification.json)、[before-0800-progress-verification.json](../../archive/progress/repeats-20261029/before-0800-progress-verification.json) |
| R2: all scores, failures, evidence publication, and remote verification | Verified at that time | [r2-independent-archive-verification.json](../../artifacts/repeats-20261029/r2-independent-archive-verification.json)、[r2-independent-remote-verification.json](../../artifacts/repeats-20261029/r2-independent-remote-verification.json) |
| R3 started only after the R2 publication gate | Verified at that time | [publication-gates/repeat-r2-20261029-gate.json](../../artifacts/repeats-20261029/publication-gates/repeat-r2-20261029-gate.json)、[r3-actor-runtime-preservation.json](../../artifacts/repeats-20261029/r3-actor-runtime-preservation.json) |
| R3: all scores, audit, evidence publication, and remote verification | Verified at that time | [r3-independent-archive-verification.json](../../artifacts/repeats-20261029/r3-independent-archive-verification.json)、[r3-independent-remote-verification.json](../../artifacts/repeats-20261029/r3-independent-remote-verification.json)、[publication-gates/final-r3-gate.json](../../artifacts/repeats-20261029/publication-gates/final-r3-gate.json) |
| Actual per-record inputs and same-task/version cross-policy fairness | Verified at that time | [r3-input-compatibility-final-execution.json](../../artifacts/repeats-20261029/r3-input-compatibility-final-execution.json)、[within-round-input-fairness-final.json](../../artifacts/repeats-20261029/within-round-input-fairness-final.json) |
| Historical client guard and serialization differences disclosed | Verified at that time | [original-effective-context-verification.json](../../artifacts/repeats-20261029/original-effective-context-verification.json)、[original-public-evidence-verification.json](../../artifacts/repeats-20261029/original-public-evidence-verification.json)、[original-local-serialization-provenance.json](../../artifacts/repeats-20261029/original-local-serialization-provenance.json) |
| R2 separate; only R1 + R3 in the 324-observation descriptive comparison | Verified at that time | [original-r3-comparison.json](../../artifacts/repeats-20261029/original-r3-comparison.json)、[original-r3-paired-evidence.json](../../artifacts/repeats-20261029/original-r3-paired-evidence.json)、[3-round-combination-refused.json](../../artifacts/repeats-20261029/3-round-combination-refused.json) |
| TF/PE/ECS, recovery/retention, paired differences, task denominator, and round-mean SD | Verified at that time | [original-r3-comparison.json](../../artifacts/repeats-20261029/original-r3-comparison.json)、[final-independent-statistics-and-order-verification.json](../../artifacts/repeats-20261029/final-independent-statistics-and-order-verification.json) |
| Update, agent, and judge costs separated; no total-cost claim from update savings | Verified at that time | [repeat-r2-20261029-metrics.json](../../artifacts/repeats-20261029/repeat-r2-20261029-metrics.json)、[final-r3-metrics.json](../../artifacts/repeats-20261029/final-r3-metrics.json)、[original-r3-comparison.json](../../artifacts/repeats-20261029/original-r3-comparison.json) |
| All 162 execution copies/events and original failures preserved during judging | Verified at that time | [r3-execution-freeze.json](../../artifacts/repeats-20261029/r3-execution-freeze.json)、[original-r3-comparison.json](../../artifacts/repeats-20261029/original-r3-comparison.json)、[r3-independent-archive-verification.json](../../artifacts/repeats-20261029/r3-independent-archive-verification.json) |
| All failures retained; 27 selected cases and five exceptions reviewed | Verified at that time | [r3-case-postscore-review.json](../../artifacts/repeats-20261029/r3-case-postscore-review.json)、[r3-failures-postscore-review.json](../../artifacts/repeats-20261029/r3-failures-postscore-review.json)、[r3-failure-preservation-verification.json](../../artifacts/repeats-20261029/r3-failure-preservation-verification.json) |
| Under-/over-updating cases retained without claiming independent human review | Verified at that time | [r3-case-execution-review-receipt.json](../../artifacts/repeats-20261029/r3-case-execution-review-receipt.json)、[r3-case-postscore-review.json](../../artifacts/repeats-20261029/r3-case-postscore-review.json) |
| At experiment completion: 491 originals, main, old tag, and release preserved | Verified at that time | [final-preservation-verification.json](../../artifacts/repeats-20261029/final-preservation-verification.json)、[r3-independent-remote-verification.json](../../artifacts/repeats-20261029/r3-independent-remote-verification.json) |
| New ZIPs anonymously downloaded; manifest SHA/CRC and provenance verified | Verified at that time | [r2-independent-archive-verification.json](../../artifacts/repeats-20261029/r2-independent-archive-verification.json)、[r3-independent-archive-verification.json](../../artifacts/repeats-20261029/r3-independent-archive-verification.json) |
| Analysis/validation source, report, and final state remotely checked | Verified at that time | [Final publication receipt](../../artifacts/repeats-20261029/final-publication-verification.json) |
| Single-round/auxiliary scope and AI-assisted review disclosed | Verified at that time | [r3-case-postscore-review.json](../../artifacts/repeats-20261029/r3-case-postscore-review.json) |

</details>

Original supplementary-file verification corresponds to [commit 5d85029](https://github.com/lingenxin3-sketch/pe6203-tool-harness-adaptation/commit/5d85029220f0f617e234d59dae37c2ae92631e2a) and its [publication receipt](../../artifacts/repeats-20261029/final-publication-verification.json). Later documentation edits are tracked in Git history. Ten intermediate snapshots are in the [progress archive](../../archive/progress/repeats-20261029/README.md); two early development files are in the [development archive](../../archive/development/README.md). Historical receipt paths are not rewritten.

## Limits

- Tasks 113/117 include failed actions with high scores and saved plans with low scores. Retain original scores and inspect calls, responses, and files. Task 28 over-updating evidence is associative, not sentence-level causation.
- The first 39 original client guards were 16384; later/new calls use 24576. The server was always 24576; all first-39 reservations fit and all 162 original judge calls dropped zero messages. One original public/local JSON differs in serialization but not values/types. Disclose both rather than claim identical code or bytes: [context audit](../../artifacts/repeats-20261029/original-effective-context-verification.json), [source audit](../../artifacts/repeats-20261029/original-public-evidence-verification.json).
- Recorded costs cover calls with returned usage only. Interrupted, non-returning calls have unknown cost. Zero API billing excludes electricity, hardware, and development; request seconds are not full runtime.
- The latest report integrates all rounds. The [old PDF](../../output/pdf/PE6203_Project4_Report.pdf), [old result tables](../../artifacts/final-result-tables.md), and [old figures](../../artifacts/figures/README.md) cover R1 only. The six-observation component variant remains a single auxiliary experiment.
- Development, documents, and evidence review used AI assistance; local automatic scores and AI-assisted review do not replace independent human evaluation.
