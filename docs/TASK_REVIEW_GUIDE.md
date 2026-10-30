# Task review guide

The active comparison contains 486 scored observations over 18 distinct tasks and three comparable rounds. Selective patch uses 65.1% fewer update tokens than full rewrite, but 5.5% more recorded total tokens. ECS means are 5.498 / 5.354 / 5.913 for no update / full rewrite / selective patch. All 10 execution exceptions remain included. The superseded input-incompatible round and one uncommitted interrupted attempt are preserved separately.

- [Current round selection](../artifacts/current-round-selection.json).
- [Frozen protocol](EXPERIMENT_PROTOCOL.md).
- [Current comparison and costs](additional-experiments/COMPARABLE_THREE_ROUNDS.md).
- [Corrected R2 cases](additional-experiments/ROUND_2_CASE_REVIEW.md).
- [R3 failure and score checks](additional-experiments/ROUND_3_CASE_REVIEW.md).
- [Evidence and hashes](EVIDENCE.md).

Execution and score completeness, actual inputs, raw evidence preservation and known cost limitations have been checked. Automated scores are not verified task success. The fixed 18-task subset and single supplementary component comparison remain limitations. No new model training or human scoring was performed.
