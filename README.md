# Enterprise AI Tool Adaptation

PE6203 Group Project 4 compares no update, full rewrite and selective patching when MCP tool names, parameters or usage descriptions change. The system updates tool contracts and usage notes without retraining the base model. Models run locally without paid APIs.

## Assembly status

Part E, assigned to **LIN GENXIN**, has been imported from the corrected 30 October package. The other five modules are pending. This is currently a partial project repository; execution code, full metrics and the integrated report arrive with the remaining modules.

The active experiment selection is R1, corrected R2 (`final-r2`) and R3: 486 scored observations on 18 distinct tasks. The superseded input-incompatible second round remains historical. Saved files and tool responses are checked separately from automatic scores; original scores and negative results are retained.

## Available evidence

- [Corrected R2 case review](docs/additional-experiments/ROUND_2_CASE_REVIEW.md)
- [Corrected R2 record and output hashes](artifacts/rerun-r2-20261030/case-review.json)
- [R3 case review](docs/additional-experiments/ROUND_3_CASE_REVIEW.md)
- [Task 113 parameter failures](docs/CASE_113_REVIEW.md)
- [Task 28 unnecessary-update cases](docs/CASE_28_REVIEW.md)
- [Task 117 score disagreements](docs/CASE_117_JUDGE_REVIEW.md)

## Repository structure

| Directory | Current contents |
| --- | --- |
| `docs/` | Case studies, output checks and task review guidance |
| `artifacts/` | Incident logs, case indexes and evidence-preservation receipts |
| `scripts/` | Saved-output checks, error inspection, evidence replay and failure preservation |
| `tests/` | Failure-accounting checks |

Historical dated receipts retain their original scope and source paths. Links to modules or archives owned by other members become available after those modules are imported.

## Team responsibilities

| Part | Member | Responsibility | Import status |
| --- | --- | --- | --- |
| A | SU YANG | Agent execution and tool calls | Pending |
| B | LIU ZHEYUAN | Tool knowledge and selective adaptation | Pending |
| C | HE YUJIE | Experiment execution and reproduction | Pending |
| D | SHISHUYI | Metrics, recovery, retention and cost | Pending |
| E | LIN GENXIN | Saved outputs, failure cases and score checks | Imported |
| F | PAN JUNKUN | Report, repository documentation and delivery | Pending |

The final shared structure will also contain `tool_adapt/`, `configs/` and the integrated report. Upload paths are assigned across members; members do not create separate member-named folders in this repository. Documentation and evidence review used AI assistance.
