"""Regenerate current numeric tables without altering frozen evidence."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def main():
    d=json.loads((ROOT/'artifacts/rerun-r2-20261030/corrected-three-round-comparison.json').read_text(encoding='utf-8'))
    assert d['total_records']==486
    source=ROOT/'docs/REPORT.md'
    text=source.read_text(encoding='utf-8')
    labels={'no_update':'No update','full_rewrite':'Full rewrite','selective_patch':'Selective patch'}
    rows=['| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS mean +/- SD |','| --- | ---: | ---: | ---: | ---: |']
    for s in d['strategies']:
        rows.append('| '+labels[s['strategy']]+' | '+' | '.join(f"{s['stages'][v]['tf']:.2f} / {s['stages'][v]['pe']:.2f}" for v in ['original','iter3','iter5'])+f" | {s['ecs_mean']:.3f} +/- {s['ecs_sample_sd']:.3f} |")
    table='\n'.join(rows)
    import re
    pattern=r'(### 5.2 Current three-round comparison\n\n)(?:\|.*\n)+'
    updated,count=re.subn(pattern,lambda m:m.group(1)+table+'\n',text)
    if count!=1:raise RuntimeError('Expected current report table not found; refusing historical fallback')
    source.write_text(updated,encoding='utf-8')
    print('Current three-round table regenerated; scientific narrative and original scores preserved.')
if __name__=='__main__':main()
