# Enterprise AI Tool Adaptation and Capability Retention

PE6203 Group Project 4 compares **no update**, **full rewrite**, and **selective patch** when tools in MCPEvol-Bench change. The system updates tool contracts and usage notes; it does not retrain the base model.

An enterprise AI agent can fail when a tool adds a required parameter, changes its interface, or changes its usage rules. We detect changes in public tool contracts, regenerate notes for affected tools and explicit dependencies, and run the same agent on the task. Calls, responses, saved files, failures, scores, and costs support the comparison.

## Assembly status

Parts E (LIN GENXIN) and F (PAN JUNKUN) have been imported in this local integration. Parts A, B, C and D remain pending. Runtime code, configuration, complete metrics and corrected raw evidence are not yet present; links to those modules will resolve after their imports. The reports and dated receipts describe the prepared experiment package and do not certify that this partial checkout is runnable.

## Reports and results

- [Latest full report PDF](output/pdf/PE6203_Project4_Final_Report.pdf) and [report source](docs/REPORT.md).
- [Final results and evidence](docs/additional-experiments/FINAL_RESULTS.md).
- [Three comparable rounds](docs/additional-experiments/COMPARABLE_THREE_ROUNDS.md).
- [Installation and reproduction](docs/REPRODUCTION.md) and [course requirements mapped to evidence](docs/REQUIREMENTS_EVIDENCE.md).

## Repository structure

| Directory | Contents |
|---|---|
| `tool_adapt/` | Shared agent loop, MCP connections, knowledge updates, and result aggregation |
| `scripts/` | Runtime preparation, experiments, scoring, evidence checks, and packaging |
| `configs/` | Frozen experiment configuration and scoring capacity settings |
| `tests/` | Update boundaries, protocol checks, failure preservation, and packaging tests |
| `artifacts/` | Tool inventories, metrics, failure evidence, and verification receipts |
| `docs/` | Method, report, case studies, and reproduction instructions |
| `output/pdf/` | Latest report and explicitly labeled historical report |
| `archive/` | Historical development files and intermediate progress snapshots |

## Method

| Policy | Response to an environment change |
|---|---|
| No update | Keep the Early tool contracts and usage notes |
| Full rewrite | Copy current contracts and regenerate all in-scope usage notes |
| Selective patch | Copy current contracts; regenerate notes only for changed tools and explicit dependencies |

Both updating policies use the same model and validation rules. Parameter schemas come directly from the current public interface. The updater receives no task answers, reference trajectories, mutation labels, or judge scores. Dependency expansion follows explicit tool-name references and can miss implicit operation order and other semantic dependencies.

## Results

The active comparison contains 486 scored observations over 18 distinct tasks and three comparable rounds. Selective patch uses 65.1% fewer update tokens than full rewrite, but 5.5% more recorded total tokens. ECS means are 5.498 / 5.354 / 5.913 for no update / full rewrite / selective patch. All 10 execution exceptions remain included. The superseded input-incompatible round and one uncommitted interrupted attempt are preserved separately.

| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS mean +/- SD |
| --- | ---: | ---: | ---: | ---: |
| No update | 6.69 / 6.96 | 6.80 / 7.20 | 7.33 / 7.41 | 5.498 +/- 0.701 |
| Full rewrite | 6.54 / 7.20 | 6.67 / 7.30 | 7.41 / 7.91 | 5.354 +/- 0.123 |
| Selective patch | 7.28 / 7.54 | 7.15 / 7.31 | 6.63 / 7.17 | 5.913 +/- 0.577 |

The active second round is `final-r2`, replacing the input-incompatible `repeat-r2-20261029`. Its scores were not selected for favorable outcomes. Selective patch has the lowest ECS in corrected R2 and lower pooled Late TF than full rewrite. These are descriptive results, with fixed seed and temperature. Saved outputs and tool responses must be checked alongside judge scores.

## Team responsibilities

| Part | Member | Responsibility | Entry point |
|---|---|---|---|
| A | SU YANG | Agent execution and tool calls | [Agent](tool_adapt/agent.py) |
| B | LIU ZHEYUAN | Tool knowledge and selective adaptation | [Knowledge updater](tool_adapt/knowledge.py) |
| C | HE YUJIE | Experiment design, execution, and reproduction | [Configuration](configs/experiment.json) |
| D | SHISHUYI | Metrics, recovery, retention, and cost | [Report data](artifacts/final-report-data.json) |
| E | LIN GENXIN | Failure cases and score/evidence review | [Task 113 case](docs/CASE_113_REVIEW.md) |
| F | PAN JUNKUN | Report integration and delivery consistency | [Report](docs/REPORT.md) |

The table defines responsibility areas. All parts share one repository structure and one system.

## Reproduction and original evidence

The [evidence index](docs/EVIDENCE.md) identifies the active rounds, corrected R2 archive and historical originals. Historical source-commit links remain as provenance.

The actor/updater uses Qwen3-4B-Instruct-2507 Q4_K_M; the judge uses Qwen2.5-7B-Instruct Q4_K_M. Both run locally through llama.cpp b11900 without a paid API. The benchmark is pinned to `888c779a0fe735f612ca62bdd1fdd7c9e6bf8701`. See the reproduction guide for dependencies and commands.

Model weights and expanded run directories remain outside the source tree. The [evidence index](docs/EVIDENCE.md) links the current corrected-R2 archive in this repository and the byte-preserved R1/R3 releases. The original incompatible R2 archive remains available as historical evidence.

The original single-round PDF, figures, and result tables remain labeled as historical. Fixed seed and temperature=0 repetitions do not establish statistical significance. Costs cover calls with returned, saved usage; zero API billing excludes hardware, electricity, and development costs.

## Sources and language

Official benchmark: [MCPEvol-Bench](https://github.com/Octobrist/MCPEvol-Bench). Code development, documentation, and evidence review used AI assistance. Original results, failures, and scores remain available for inspection.

Project documentation is in English. Frozen benchmark data, tool contracts, model messages, JSON receipts, and original logs retain their original bytes and language. Translating those records would change experimental evidence. Historical receipts can therefore contain earlier document paths; current English paths are used in the documentation.
