# Round 3: execution and score evidence review

Source: `runs/final-r3`. All 162 observations are executed, scored, and archived. Review covers 27 task 28/113/117 traces and all five execution exceptions. Pre-score execution observations are compared with original scores below. This is AI-assisted evidence review, not independent human annotation; no original score changes.

Final audits find all 162 resource lists match R1, with matching 54 cross-policy fairness groups within each round. The 54 cross-policy groups in the superseded R2 run (`repeat-r2-20261029`) differed and that run remains excluded. The replacement R2 (`final-r2`) passed its input checks and is included with R1 and R3 in the current 486-observation comparison. See [final input audit](../../artifacts/repeats-20261029/r3-input-compatibility-final-execution.json), [fairness audit](../../artifacts/repeats-20261029/within-round-input-fairness-final.json), and [final results](FINAL_RESULTS.md). Earlier 12-group checks are intermediate snapshots only.

## Task 28: saved tasks and evidence-supported contents

The question asks to compare yesterday's and today's logs, summarize changes, create follow-up tasks for suspected unresolved issues, and save tasks.md in the project. Paths below are relative to each observation's workspace.

| Policy | Version | Tool calls | MCP-flagged errors | Created task file |
|---|---|---:|---:|---|
| No update | Early | 3 | 0 | anotation_path/markdown/tasks.md |
| No update | Middle | 3 | 0 | anotation_path/markdown/tasks.md |
| No update | Late | 3 | 0 | anotation_path/markdown/tasks.md |
| Full rewrite | Early | 3 | 0 | markdown/tasks.md |
| Full rewrite | Middle | 4 | 3 | Not created |
| Full rewrite | Late | 4 | 3 | Not created |
| Selective patch | Early | 3 | 0 | anotation_path/markdown/tasks.md |
| Selective patch | Middle | 3 | 0 | anotation_path/markdown/tasks.md |
| Selective patch | Late | 4 | 1 | txt/tasks.md |

Seven traces create Markdown with three unchecked tasks each. Original result/output hashes and counts are in the [27-case execution receipt](../../artifacts/repeats-20261029/r3-case-execution-review-receipt.json).

Full rewrite/Middle has an empty modified set but rewrites tasks_add, tasks_setup, and read_multiple_files. It then uses invented source_id_1 and initializes two .txt logs as task sources: one missing-source and two unsupported-type errors, no file. Selective patch/Middle preserves notes and saves a file through valid initialization and addition. Full rewrite/Late rewrites all three notes although only read_multiple_files changed, again producing three errors and no file. These are observed associations, not proof that one rewritten sentence caused the failure.

Selective patch/Late updates only reader notes. It reads logs using includeMetadata and separator, fails its first tasks_add without a valid source, then initializes txt/tasks.md, takes the real returned ID, and adds three tasks. Four calls and one error eventually produce a file. Recovery succeeds in this trace, but it costs one failed call beyond the normal three-call flow. Judge process efficiency together with actual calls, tokens, and PE, not file existence alone.

Yesterday's log has disk warnings, a database connection error, and a login entry; today's has service startup and disk warnings. They prove neither unresolved nor resolved database status. No update in all versions, full rewrite/Early, and selective patch/Early/Middle still assert an ongoing unresolved database error without support. Selective patch/Late acknowledges the absence of a new database error and asks to investigate/verify the historical issue. Repeated disk warnings are supported. Full rewrite/Middle additionally claims stable logins without a corresponding entry today. Saving seven files does not validate their content.

## Task 113: required fields, actual plans, and call counts

Early planning requires originalRequest and tasks; Middle adds splitDetails; Late adds priority and tags. A saved dashboard plan is not delivered dashboard code.

| Policy | Version | Tool calls | Planning calls / failures | Root plan tasks | Other task storage |
|---|---|---:|---:|---:|---|
| No update | Early | 3 | 1 / 0 | 5 | Project task store empty |
| No update | Middle | 4 | 2 / 1 | 5 | Project task store empty |
| No update | Late | 8 | 7 / 7 | No root plan | Project task store empty |
| Full rewrite | Early | 3 | 1 / 0 | 5 | Project task store empty |
| Full rewrite | Middle | 6 | 0 / 0 | No root plan | Four pending project tasks |
| Full rewrite | Late | 3 | 1 / 0 | 5 | Project task store empty |
| Selective patch | Early | 3 | 1 / 0 | 5 | Project task store empty |
| Selective patch | Middle | 2 | 1 / 0 | 6 | No new project task store |
| Selective patch | Late | 3 | 1 / 0 | 6 | Project task store empty |

Root workspace/tasks.json stores a requests array with nested tasks. Reading only a top-level tasks field would falsely count zero. The separate `.agentic-tools-mcp/tasks/tasks.json` store must be inspected independently. Full rewrite/Middle saves four pending tasks there despite no root plan.

No update/Middle omits splitDetails once, reads the error, then saves five tasks. It recovers but uses two more calls than selective patch/Middle. The latter plans and queries the next task in two calls without unnecessary project creation from another tool family. Do not confuse prerequisites across tool families.

No update/Late omits splitDetails/priority/tags initially; six later attempts add splitDetails only. All seven planning calls fail. An empty project store exists, but no root plan is registered: JSON existence alone is not successful task storage.

Both updating policies/Late pass all five required fields and save plans; selective patch also passes estimatedDeadline. All stored plan tasks have done=false and approved=false; the four alternate project tasks remain pending. Outputs are plan JSON, with no evidence of dashboard implementation, testing, or human approval. Selective patch/Late saves six tasks in R3. The earlier comparison of five tasks referred to R1 and the superseded R2 (`repeat-r2-20261029`). Corrected R2 (`final-r2`) also saves six tasks; see the [corrected-R2 case review](ROUND_2_CASE_REVIEW.md).

The shared [execution receipt](../../artifacts/repeats-20261029/r3-case-execution-review-receipt.json) covers original bytes, calls, and output hashes for all 27 cases. Do not substitute selected cases for [whole-round metrics](ROUND_3_RESULTS.md).

## Task 117: decomposition, history search, and exceptions

The question asks for traffic-route-optimization analysis, subtasks with completion criteria, sequential validation reasoning, and similar historical tasks.

| Policy | Version | Decision rounds | Tool calls | Saved Shrimp tasks | Search evidence |
|---|---|---:|---:|---:|---|
| No update | Early | 12 | 12 | 0 | Search failed: source1 not found |
| No update | Middle | 12 | 12 | 0 | Search failed: workspace not found |
| No update | Late | 12 | 12 | 5 | Missing source first; valid work.md query later returned empty |
| Full rewrite | Early | 12 | 12 | 0 | Search failed: source1 not found |
| Full rewrite | Middle | 12 | 12 | 0 | Search failed; work.md registered later without another search |
| Full rewrite | Late | 3 | 3 | 0 | Exception; no search call |
| Selective patch | Early | 3 | 3 | 0 | Exception; no search call |
| Selective patch | Middle | 10 | 8 | 6 | Two failed searches using a task ID as a source ID |
| Selective patch | Late | 12 | 22 | 0 | No split or archive search call |

The limit is 12 decision rounds, not 12 tool calls. Selective patch/Late's 22 tool calls include source initialization and thought tools but no task splitting or archive search, and the final answer is empty. A long process is not completion.

No update/Late first fails with most_recent as a source, then performs a valid query against registered work.md and receives an empty array. That source is a benchmark workflow guide, not retrieved historical experience. Not every search call failed, but no reusable history was returned. Full rewrite/Middle registers a similar Markdown source after a failed search and never queries again.

Selective patch/Middle saves six Shrimp tasks but passes a task ID into another tool family as source_id; both searches fail. String type and parameter name checks cannot establish correct ID provenance across tools.

Full rewrite/Middle makes three split_tasks calls whose bodies report tasksRaw JSON control-character errors while isError=false, with no saved Shrimp task file. Flag counters miss these semantic failures.

Full rewrite/Late and selective patch/Early terminate after their third tool call, split_tasks, with an Unterminated string error. Both have empty answers, no tasks, and eight messages reconstructable from existing events. Preserve originals/events; do not rerun or invent actions. The controller later prepared failures and scored them under the original protocol.

Selective patch/Early has adaptation.status=initial, before any environment update. Its exception cannot be attributed to selective adaptation. Only selective patch/Middle has a nonempty final answer among these nine cases; that fact does not replace official scores. Search responses, split errors, and hashes are in the [execution receipt](../../artifacts/repeats-20261029/r3-case-execution-review-receipt.json).

## Complete original selected-case scores

Collected 2026-10-29T11:25:27+08:00. All 27 are scored; this is not a whole-round average or success rate.

| Policy | Version | Task 28 TF / PE | Task 113 TF / PE | Task 117 TF / PE |
|---|---|---:|---:|---:|
| No update | Early | 10 / 10 | 10 / 10 | 4 / 4 |
| No update | Middle | 10 / 10 | 10 / 10 | 7 / 7 |
| No update | Late | 10 / 10 | 10 / 10 | 8 / 8 |
| Full rewrite | Early | 10 / 10 | 10 / 10 | 7 / 4 |
| Full rewrite | Middle | 1 / 4 | 10 / 10 | 10 / 10 |
| Full rewrite | Late | 1 / 4 | 10 / 10 | 8 / 10 |
| Selective patch | Early | 10 / 10 | 10 / 10 | 10 / 10 |
| Selective patch | Middle | 10 / 10 | 4 / 9 | 10 / 10 |
| Selective patch | Late | 10 / 7 | 4 / 10 | 7 / 7 |

Pre-score original/failure hashes, critical execution fields, and actor/update calls match the first review. See [post-score review](../../artifacts/repeats-20261029/r3-case-postscore-review.json).

## Specific disagreements

Task 117/selective patch/Early scores 10/10 despite exception, empty answer, and no task file, before adaptation. Full rewrite/Middle also scores 10/10 despite three malformed split responses and no stored tasks. Full rewrite/Late scores 8/10 here, not its R2 score of 10/10.

Task 113/no update/Late scores 10/10 despite seven rejected planning calls; its R2 counterpart scores 1/4. Those rounds have different trajectories and R2 input confounding, so this is not an isolated judge-randomness experiment. It still demonstrates why high scores cannot stand in for registration recovery. Selective patch/Middle and Late save plans yet retain TF=4; file existence does not prove all requirements were met.

Task 28/full rewrite/Middle and Late score 1/4, detecting missing task files. Selective patch/Late recovers from one error, saves a file, and scores 10/7. Keep content checks and original scores together without declaring the whole judge universally valid or invalid.

## All five execution exceptions

| Policy | Version | Task | Model / tool calls | TF / PE |
|---|---|---:|---:|---:|
| Full rewrite | Late | 117 | 3 / 3 | 8 / 10 |
| No update | Middle | 389 | 2 / 2 | 7 / 4 |
| Selective patch | Late | 416 | 3 / 3 | 7 / 7 |
| Selective patch | Early | 117 | 3 / 3 | 10 / 10 |
| Selective patch | Early | 389 | 2 / 2 | 8 / 4 |

All five final answers are empty; execution snapshots list no added/modified files. Earlier analysis/planning text can be useful but does not prove registration, archive retrieval, or code changes. Keep original scores, exceptions, and complete trajectories; see [failure score review](../../artifacts/repeats-20261029/r3-failures-postscore-review.json). infrastructure_error is a program status; a generic ExceptionGroup does not establish a hardware root cause.

These explanatory tables and supplementary analyses were committed after the evidence ZIP release. They are not represented as files originally in that ZIP. The frozen ZIP already contains all 162 original scores and execution records; neither it nor old releases was overwritten. Reviews are AI-assisted, not independent human annotation.
