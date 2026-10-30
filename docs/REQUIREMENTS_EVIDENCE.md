# Requirements evidence

The active comparison contains 486 scored observations over 18 distinct tasks and three comparable rounds. Selective patch uses 65.1% fewer update tokens than full rewrite, but 5.5% more recorded total tokens. ECS means are 5.498 / 5.354 / 5.913 for no update / full rewrite / selective patch. All 10 execution exceptions remain included. The superseded input-incompatible round and one uncommitted interrupted attempt are preserved separately.

| Course requirement | Project evidence |
| --- | --- |
| Compare no update, full rewrite and selective adaptation | [Policies and shared execution loop](REPORT.md) |
| Tool, parameter and description changes | [Official tool inventories](../artifacts/inventory/original.json) and [coverage](../artifacts/coverage.json) |
| Consistent tasks, models, settings and judge | [Frozen configuration](../configs/experiment.json) and [corrected input checks](../artifacts/rerun-r2-20261030/final-input-compatibility.json) |
| Prefer three repetitions | Three compatible 162-episode grids; [486 scored sources](../artifacts/rerun-r2-20261030/corrected-three-round-paired-evidence.json) |
| Report ECS, task fulfillment, efficiency and costs | [Current result tables](../artifacts/final-result-tables.md), including paired recovery and retention |
| Show under-update and over-update failures | [Task 113](CASE_113_REVIEW.md), [task 28](CASE_28_REVIEW.md), and [corrected-R2 counterexamples](additional-experiments/ROUND_2_CASE_REVIEW.md) |
| Preserve evidence and avoid fine-tuning | [Raw archive and hashes](EVIDENCE.md); unchanged model weights and frozen method |
| Present clearly within ten minutes | Six responsibility areas are listed in the README; the presentation is a separate delivery artifact |

- [Current round selection](../artifacts/current-round-selection.json).
- [Frozen protocol](EXPERIMENT_PROTOCOL.md).
- [Current comparison and costs](additional-experiments/COMPARABLE_THREE_ROUNDS.md).
- [Corrected R2 cases](additional-experiments/ROUND_2_CASE_REVIEW.md).
- [R3 failure and score checks](additional-experiments/ROUND_3_CASE_REVIEW.md).
- [Evidence and hashes](EVIDENCE.md).

Execution and score completeness, actual inputs, raw evidence preservation and known cost limitations have been checked. Automated scores are not verified task success. The fixed 18-task subset and single supplementary component comparison remain limitations. No new model training or human scoring was performed.
