# Additional experiments: frozen protocol and failure handling

Historical protocol and amendment record. The active comparison now uses R1, corrected R2 final-r2 and R3 (486 observations); see [current results](FINAL_RESULTS.md). Earlier selection decisions below retain their original historical scope.

This is an English reading edition of the 2026-10-29 protocol and declarations made before R3 scoring. Both additional rounds are complete. Historical references to 12:00 and waiting for the team describe the original execution boundary, not pending work. Frozen receipts retain their original text, paths, timestamps, and hashes. See [final results](FINAL_RESULTS.md) and the [progress archive](../../archive/progress/repeats-20261029/README.md).

## Provenance and comparability

R1 is `runs/final-v1`; R2 is `runs/repeat-r2-20261029`; R3 is `runs/final-r3`. Before it was ever executed, R3 was renamed from the planned `repeat-r3-20261029` to an eight-character directory matching the R1 directory length to restore resource visibility. Each configuration uses repeats=1 and executes 162 observations. Do not rewrite R1 manifests, runs, failures, or scores. A comparison is an analysis view with round, source path, and SHA-256; original repeat numbers remain unchanged.

Require the same configuration, 18 tasks, three policies, versions, tool inventories and source, base models, decoding settings, step limit, and judging protocol. Actor/updater: original Qwen3 4B, temperature=0, seed=6203, 12 decision rounds, context 16384. Judge: original Qwen2.5 7B, capacity revision 24576, original rubric and judge-only adapter. Preflight dependency and source checks are in `artifacts/repeats-20261029/preflight.json`; also inspect actual manifests, model runtime receipts, and judge calls. Report incompatible rounds separately; do not add a third new round.

Fixed settings describe execution stability. Output paths enter prompts, and generated IDs, caches, and hardware state can vary. Timing is descriptive; do not attribute hardware differences to adaptation or assume significance.

During execution, Windows long-path behavior hid some PDF filenames from resource listings under the new directory even when file bytes matched. Compare actual per-record resource lists. A mismatch prevents strict pooling; possible nonuse of a PDF is not evidence of equal inputs. Preserve completed runs rather than rerun them to repair directory names. The list difference is not proven to cause score changes.

R2 also has visibility differences across policy directory lengths, confounding within-round comparisons. Before R3, 27 model-free filesystem checks covered one-, two-, and three-digit task IDs, all policies, and all versions under an equal-length directory. Visible filenames matched R1; temporary test directories were cleaned separately without modifying source or formal evidence. Actual R3 prompts still required verification. Never include incompatible R2 records in a 486-observation comparable result.

## Orchestration and recovery

New scripts manage outer orchestration, status, resumption, and publication; frozen `tool_adapt` code remains unchanged. Initial execution calls the original function. Explicit resumption uses a checked AST adapter to replace only the existing-output-directory guard and load saved episode results/knowledge at episode boundaries, skipping completed execution. Model and method instructions do not change. Preserve original/new script hashes and tests.

After input mismatches were found, `repeat_supervise_existing.py` attached sleep prevention, retained the live actor handle, and replaced only the obsolete controller. It waited for that same actor to finish before explicitly resuming the corrected controller. Completed requests were not sent again. Keep takeover receipts, process IDs, and tests; stop on takeover errors without clearing data.

Never automatically rerun saved episodes. An existing workspace without a completely committed result.json blocks resumption and requires investigation; do not erase it. Preserve model/tool errors as real failures. Failure recovery assembles existing events for judging while preserving failure-record.json and event hashes. Missing or inconsistent traces stop recovery.

Use the original `judge_with_capacity.py`. Skip valid existing scores and handle only awaiting_judge records. Never silently rescore judge_failed records. If a connection interruption prevents saving a score, preserve the agent record and interruption log, confirm the old process has terminated, and explicitly decide whether to resume unscored records. Retain the official limited malformed-JSON format retries uniformly. Do not alter scores, select favorable retries, or remove failures.

## Publication gates used in the completed campaign

Before execution, publish and read back a status page. During execution, aim for timestamped snapshots every 15 minutes from atomically saved result.json files. Times are UTC+8. Windows SetThreadExecutionState prevents idle sleep while the process lives without changing the power plan; lid closing, power loss, reboot, and network failures can still interrupt it.

Each round requires execution, failure evidence, judging, the unique 162-cell matrix audit, protocol checks, and an independent statistics check. Before R3 starts, R2 must also have a committed result, a new evidence release, anonymous archive download/SHA-256 verification, and remote readback of the final status. A failed gate stops R3. Do not overwrite v1.0.0, force-push, merge main, or submit to the course platform automatically.

12:00 was a target: if R3 had not started, the controller was to wait for the team. Preserve the current run and report actual progress rather than delete or fabricate data.

## Statistics and public evidence

Report TF, PE, ECS, recovery, retention, update/agent/judge tokens, request seconds, and local API charges separately. Comparable summaries use complete round statistics and sample SD of round means. Preserve the denominator of 18 distinct tasks; repetitions are not new independent tasks. Include paired policy differences for the same task/version. The original dependency-expansion variant remains a single auxiliary experiment.

Preserve original task 113/117 score disagreements. Automated case indexes for tasks 28/113/117 locate traces and files; they are not independent human confirmation. File existence is not content correctness. Distinguish under-updating, over-updating, model behavior, and tool failures.

Evidence archives contain manifests, calls, trajectories, scores, failures, actual created/modified files, and verification receipts. Exclude model weights, credentials, environment variables, unrelated workspace content, and unchanged duplicate resources. Scan credential patterns and path boundaries, then anonymously download each new release to verify its checksum. Code, documentation, and reviews used AI assistance; packaging is not proof of independent authorship.

Include closed logs for execution, judging, and aggregation subprocesses, plus failure-case tool stderr. Do not treat a still-growing global model-server log as a completed attachment. Synthetic ZIP inclusion tests are separate from formal observations.

## Text hashes and raw bytes

Git can normalize CRLF to LF. Verify branch files against bytes of the corresponding commit's Git blobs. ZIP PACKAGE_MANIFEST.json hashes cover original local bytes; the attachment .sha256 covers the entire ZIP. These are different objects.

For r2-actor-start-runtime.json, the local raw SHA starts with `9b0d42`, while the commit text SHA starts with `d6b245`; the difference is CRLF-to-LF normalization. Verify original-byte runtime hashes in the ZIP and branch hashes against Git blobs. Do not rewrite evidence to force hash equality.

## R3 comparison declared before judging

Before R3 scoring, the stated rule allowed a separately named R1 `final-v1` + R3 `final-r3` descriptive comparison only if R3 completed scoring and matched actual inputs and runtime/judging conditions. That view has 324 observations, 18 distinct tasks, and two observations per combination. R2 stays separate because its input difference was discovered before scoring, not because of its scores. If R3 failed comparability, report all rounds separately without another new round.

## Original release serialization exception

The anonymously downloaded v1.0.0 PE6203_Project4_Submission.zip has SHA-256 `f0df5bdecbfc840cfd8b58555733ad5a4bfe99ad742fdedbd6b1f500dbc19fad`. Of 491 original evidence files, 490 match local frozen bytes. Task 113/no_update/Late/result.json differs in JSON serialization; this is not byte equality and is not merely a newline difference.

Its public raw SHA begins `b16ad344`; the local frozen SHA begins `72272795`. Canonical sorted-key compact UTF-8 JSON matches completely, including scores, requests, traces, values, and types. The campaign did not rewrite the local file, replace the old ZIP, or change scores. R1 statistics use the initial frozen local version. Both raw hashes and the canonical content hash are in [source verification](../../artifacts/repeats-20261029/original-public-evidence-verification.json).

An exact binary copy of that local original is described in [serialization provenance](../../artifacts/repeats-20261029/original-local-serialization-provenance.json) and included in the R3 evidence ZIP. Its raw SHA is `7227279529b71bbe8c95cac2d43c7935b20faeca3e56b3d89170e43205cc4335`. It is not another observation. Branch downloads may undergo LF normalization; use the ZIP for exact bytes. Never rewrite release history to hide this distinction.

## Historical judge client guard

Read-only checks at 08:15 covered the original release, startup logs, two recovery receipts, and all 162 original judge calls. The first 39 calls used the original 16384 client guard without a context_limit field; the later 123 used the 24576 adapter. The server was already 24576 before the first call, as shown by startup and recovery records.

The largest first-39 prompt plus response/safety reservation was 15505, below 16384; all 162 calls have dropped_messages=0. The first-39 source hashes match the incident archive. Thus the guard difference did not change retained judge inputs, but client implementations were not identical. See [context verification](../../artifacts/repeats-20261029/original-effective-context-verification.json). Disclose this and inspect actual R3 requests/runtime receipts rather than equate matching configuration with matching conditions. Costs of interrupted, non-returning original judge requests remain unknown and must not be fabricated as zero.
