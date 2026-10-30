# Course requirements mapped to evidence

Based on the Project 4 brief. Each of three rounds has 162 scored observations. R2 remains separate; only R1 + R3 form a 324-observation descriptive comparison. See [final results](additional-experiments/FINAL_RESULTS.md).

| Requirement | Implementation or result | Evidence |
|---|---|---|
| MCPEvol-Bench | Pinned official revision, 18 tasks, three real environment versions | `configs/experiment.json`, round manifests, `artifacts/server-source-audit.json` |
| A designed selective adaptation method | Compare public tool contracts, expand explicit references, regenerate affected notes | `tool_adapt/knowledge.py`, report method section, update-boundary tests |
| No-update and full-rewrite baselines | Shared agent and model settings; actual inputs audited separately | Round records and final input-fairness audits |
| Early/Middle/Late; tool, parameter, and description changes | All versions and change categories covered; categories can overlap | `artifacts/inventory/`, protocol, cohort analyses |
| TF, PE, ECS | 162 original-protocol scores per round; preserve separate results | [Final results](additional-experiments/FINAL_RESULTS.md) and [comparable analysis](additional-experiments/COMPARABLE_R1_R3.md) |
| Repeated experiments | R1 and two additional rounds completed; R2 excluded from comparable pooling because inputs differ | Input audits and `3-round-combination-refused.json` |
| Recovery and capability retention | Changed and unaffected cohorts; preserve negative results and denominators | Comparison JSON cohorts; Early differences are not adaptation effects |
| Update cost | Separate update, agent, and judge usage | 65.1% fewer update tokens; 5.6% more total recorded tokens in R1 + R3 |
| Under-updating case | Task 113: old notes omit newly required fields; plan registration fails | `docs/CASE_113_REVIEW.md` and R3 case review |
| Over-updating case | Task 28: unchanged notes rewritten; no task file saved in affected traces | `docs/CASE_28_REVIEW.md` and R3 case review; association, not sentence-level causation |
| Effectiveness, failures, difficult changes | Lower update usage but mixed task/recovery results; implicit dependencies, ID confusion, judge blind spots | Report, comparable analysis, case reviews |
| Reproducible code, configuration, original logs | Frozen dependencies, models, traces, artifacts, and failures | `docs/REPRODUCTION.md` and three evidence releases; full runs are not in the source download |
| 10-minute presentation and 5-minute Q&A | Saved evidence can demonstrate mechanisms; replay is labeled as replay | `scripts/demo_evidence.py` and case reviews |
| GitHub or Google Drive delivery | Public repository, report, checksummed evidence archives | Final results page; publication is distinct from submission to the course platform |

## Research limits

1. The 486 records are not 486 independent tasks. The comparable analysis has 18 distinct tasks and two observations per combination. Fixed seed and temperature=0 repetitions do not establish significance or universal superiority.
2. R2 has 123 cross-round resource-list mismatches and 54 within-round cross-policy mismatched input groups. R1 and R3 match on all 162 resource lists and 54 cross-policy groups each. Historical client-limit and one JSON-serialization difference remain disclosed.
3. Execution exceptions are 4, 5, and 5 in R1, R2, and R3; all are retained and scored. A valid score is not proof of completion. Task 113/117 judge disagreements remain unchanged.
4. Update-token savings are not total-token or total-cost savings. Costs of calls with no returned usage are unknown; zero API billing excludes hardware and electricity.
5. Early results differ before adaptation. The dependency-expansion variant remains a single auxiliary experiment. Do not attribute every execution fluctuation, missing resource, or agent mistake to the update method.
6. The latest report and `PE6203_Project4_Final_Report.pdf` integrate all rounds. The old PDF, tables, and figures cover the original single round only.

Responsibilities appear once in the [root README](../README.md#team-responsibilities). Development, documentation, and evidence review used AI assistance; conclusions follow the saved evidence.
