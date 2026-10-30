"""Export the current three-round scientific figure and exact plotted values."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / 'artifacts/rerun-r2-20261030/corrected-three-round-comparison.json'
    data = json.loads(source.read_text(encoding='utf-8'))
    assert data['total_records'] == 486
    dest = ROOT / 'artifacts/figures'
    dest.mkdir(parents=True, exist_ok=True)
    labels = {'no_update': 'No update', 'full_rewrite': 'Full rewrite', 'selective_patch': 'Selective patch'}
    colors = ['#555555', '#1c66a6', '#bd5c18']
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.4), sharey=True)
    figure_rows = []
    for axis, metric, title in zip(axes, ['tf', 'pe'], ['Task fulfillment (TF)', 'Planning effectiveness (PE)']):
        for i, policy in enumerate(data['strategies']):
            stages = [policy['stages'][v] for v in ['original', 'iter3', 'iter5']]
            values = [s[metric] for s in stages]
            errors = [s[metric + '_round_sample_sd'] for s in stages]
            axis.errorbar([0, 1, 2], values, yerr=errors, label=labels[policy['strategy']],
                          color=colors[i], marker=['o', 's', '^'][i], linewidth=1.7,
                          markersize=5.2, capsize=4, alpha=.95)
            figure_rows.append({'policy': policy['strategy'], 'metric': metric,
                                'means': values, 'round_mean_sample_sd': errors})
        axis.set_title(title, fontsize=12, pad=12)
        axis.set_xticks([0, 1, 2], ['Early', 'Middle', 'Late'])
        axis.set_ylim(1, 10)
        axis.set_yticks(range(1, 11))
        axis.grid(axis='y', color='#dddddd', linewidth=.65)
        axis.spines[['top', 'right']].set_visible(False)
        axis.tick_params(labelsize=10)
    axes[0].set_ylabel('Original rubric score (1–10)', fontsize=10)
    fig.legend(*axes[0].get_legend_handles_labels(), loc='lower center', ncol=3,
               bbox_to_anchor=(.5, .06), frameon=False, fontsize=10)
    fig.suptitle('R1 + corrected R2 + R3', fontsize=15, y=.99)
    fig.text(.5, .015, '18 distinct tasks · 54 observations per policy/version · bars: SD of 3 round means, not confidence intervals',
             ha='center', fontsize=8.5, color='#555555')
    fig.subplots_adjust(left=.075, right=.98, bottom=.23, top=.86, wspace=.16)
    fig.savefig(dest / 'performance.png', dpi=220)
    fig.savefig(dest / 'performance.svg')
    plt.close(fig)
    (dest / 'figure-data.json').write_text(json.dumps({'source': source.relative_to(ROOT).as_posix(),
        'rounds': ['final-v1', 'final-r2', 'final-r3'], 'distinct_tasks': 18,
        'observations_per_policy_version': 54, 'values': figure_rows,
        'error_definition': 'Sample standard deviation of three round means; not confidence intervals.'}, indent=2), encoding='utf-8')
    print('Current three-round PNG, SVG and exact figure values exported.')


if __name__ == '__main__':
    main()
