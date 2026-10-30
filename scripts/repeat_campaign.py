"""Sequential, staged and independently published repeat experiment campaign."""
import argparse
import asyncio
import ctypes
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from repeat_common import *
import repeat_publish as pub
from audit_experiment import audit
from analyze_comparisons import compare
from finalize_failed_episodes import finalize
from repeat_runner import execute

RUNTIME=ROOT/'runtime'/CAMPAIGN
STATE=RUNTIME/'state.json'
LOCK=threading.RLock()
STOP=threading.Event()
NO_WINDOW=getattr(subprocess,'CREATE_NO_WINDOW',0)
SHELL=shutil.which('pwsh') or str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')

def state(phase,message,**extra):
    with LOCK:
        old=read(STATE) if STATE.exists() else {}
        old.update(pid=os.getpid(),phase=phase,message=message,updated_at=now(),**extra);save(STATE,old)
    print(now(),phase,message,flush=True)
def command(args,filename):
    env=os.environ.copy();env['PYTHONIOENCODING']='utf-8';env['PYTHONUNBUFFERED']='1'
    with (RUNTIME/filename).open('ab',buffering=0) as log:
        log.write(('\n'+now()+' '+repr(list(map(str,args)))+'\n').encode())
        p=subprocess.Popen(list(map(str,args)),cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,env=env,creationflags=NO_WINDOW)
        state(read(STATE)['phase'],read(STATE)['message'],child_pid=p.pid)
        code=p.wait();state(read(STATE)['phase'],read(STATE)['message'],child_pid=None)
    if code:raise RuntimeError(f'{filename}: subprocess exited {code}; evidence retained')
def ps(name,*args):command([SHELL,'-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'scripts'/name,*args],name+'.log')
def json_get(url):
    with urllib.request.urlopen(url,timeout=5) as r:return json.load(r)
def model(role):
    other='judge' if role=='actor' else 'actor'
    ps('stop-local-model.ps1','-Role',other)
    ps('start-local-model.ps1' if role=='actor' else 'start-judge.ps1')
    port=8081 if role=='actor' else 8082
    for i in range(120):
        try:
            if json_get(f'http://127.0.0.1:{port}/health').get('status')=='ok':break
        except Exception:pass
        time.sleep(1)
    else:raise RuntimeError('Model not ready')
    props=json_get(f'http://127.0.0.1:{port}/props');models=json_get(f'http://127.0.0.1:{port}/v1/models')
    expected=16384 if role=='actor' else 24576;alias='qwen3-4b' if role=='actor' else 'qwen2.5-7b-judge'
    if props['default_generation_settings']['n_ctx']!=expected or props.get('build_info')!='b11900-74b104c9b' or alias not in [m['id'] for m in models['data']]:raise RuntimeError('Runtime differs from frozen protocol')
    save(ROOT/'artifacts'/CAMPAIGN/(role+'-runtime.json'),{'recorded_at':now(),'properties':props,'models':models})
def verified_status():
    with LOCK:
        s=read(STATE);pub.status(s['phase'],s['message'])
        return pub.publish('Update repeat experiment progress '+now())
def heartbeat():
    while not STOP.wait(900):
        try:verified_status()
        except Exception as e:save(RUNTIME/'progress-publication-error.json',{'at':now(),'error':str(e)})
def preserve_old():
    pre=read(ROOT/'artifacts'/CAMPAIGN/'preflight.json')
    for name,expected in pre['raw_evidence_hashes'].items():
        if sha(ROOT/name)!=expected:raise RuntimeError('Original evidence changed: '+name)
def scored_report(folder,ordinal):
    view=metrics(folder);save(ROOT/'artifacts'/CAMPAIGN/(folder.name+'-metrics.json'),view)
    labels={'no_update':'No update','full_rewrite':'Full rewrite','selective_patch':'Selective patch'}
    lines=[f'# Round {ordinal}: independent results','',f'Collected: {now()}. Source: `runs/{folder.name}`.','',
        f"Saved {view['status']['found']}/162; scored {view['status']['scored']}/162; execution exceptions {view['status']['failures']}. All failures retained.",'',
        '| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS |','|---|---:|---:|---:|---:|']
    for x in view['strategies']:lines.append('| '+labels[x['strategy']]+' | '+' | '.join(f"{x['stages'][v]['tf']:.2f} / {x['stages'][v]['pe']:.2f}" for v in VERS)+f" | {x['ecs']:.3f} |")
    lines+=['','## Cost','', '| Policy | Phase | Calls | Token | Request seconds | Local API USD |','|---|---|---:|---:|---:|---:|']
    for x in view['strategies']:
        for k,c in x['costs'].items():lines.append(f"| {labels[x['strategy']]} | {k} | {c['calls']} | {c['tokens']} | {c['request_seconds']:.2f} | {c['api_usd']:.2f} |")
    full=next(x for x in view['strategies'] if x['strategy']=='full_rewrite');sel=next(x for x in view['strategies'] if x['strategy']=='selective_patch');den=full['costs']['update']['tokens']
    lines+=['',f"Selective-patch update-token savings vs full rewrite: {100*(1-sel['costs']['update']['tokens']/den):.1f}%. Update stage only; agent/judge usage is separate. Zero local API billing excludes electricity and hardware." if den else 'Zero update-token denominator; savings undefined.','',
        '## Recovery and retention','', '| Policy | Version | Cohort | n | TF | Delta vs own Early | Delta vs same-round no update |','|---|---|---|---:|---:|---:|---:|']
    for x in view['strategies']:
        for c in x['cohorts']:lines.append(f"| {labels[x['strategy']]} | {c['version']} | {c['cohort']} | {c['n']} | {c['tf']:.2f} | {c['delta_own_early']:+.2f} | {c['delta_same_version_no_update']:+.2f} |")
    checks=[]
    for rp in sorted(folder.glob('repeat-*/*/*/*/result.json')):
        r=read(rp)
        if r['idx'] in [28,113,117]:checks.append({'source':rp.relative_to(ROOT).as_posix(),'task':r['idx'],'strategy':r['strategy'],'version':r['version'],
            'score':r['eval_result']['aggregate'],'files':r.get('artifact_changes',{}),'execution_status':r.get('execution_status'),
            'review_status':'Automatic file/trace index; requires review and does not prove correct completion.'})
    save(ROOT/'artifacts'/CAMPAIGN/(folder.name+'-case-index.json'),checks)
    c=round_compatibility(ROOT/'runs/final-v1',folder);save(ROOT/'artifacts'/CAMPAIGN/(folder.name+'-compatibility.json'),c)
    lines+=['','## Limits and evidence','',f"Overall comparability with R1: {c['compatible']}. Actual per-record resource lists are checked in addition to manifests. Runtime/tool/model checks: artifacts/repeats-20261029.",'',
        'If resource lists differ, report incompatible rounds separately without pooling them. Windows path visibility is an input difference, not an isolated causal explanation for score changes.', '',
        'Fixed seed and temperature=0 do not establish significance. Repetition does not remove task 113/117 judge blind spots. Automatic case indexes locate files/traces, not correct contents. Retain original scores.',
        '','The latest report integrates all rounds; the original report/figures remain historical. The dependency variant remains a single auxiliary experiment. See [task 117](../CASE_117_JUDGE_REVIEW.md).', '',
        'See [task 113](../CASE_113_REVIEW.md) and [task 28](../CASE_28_REVIEW.md) for under-/over-updating evidence. Task 28 is associative, not sentence-level causation.']
    (pub.PUBLIC/f'ROUND_{ordinal}_RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return c
def aggregate_views(ordinal):
    folders=[ROOT/'runs'/n for n in NAMES[:ordinal]]
    if any(not round_compatibility(folders[0],p)['compatible'] for p in folders[1:]):
        save(ROOT/'artifacts'/CAMPAIGN/f'{ordinal}-round-combination-refused.json',{'collected_at':now(),'reason':'Actual resource listings differ or compatibility is unverified; original and added rounds must be reported separately.','rounds':[p.name for p in folders]})
        return
    combined=merge_views(folders);save(ROOT/'artifacts'/CAMPAIGN/f'{ordinal}-round-comparison.json',combined)
    # Paired differences retain each original identity, path, manifest and hash.
    paired=[];provenance=[]
    for folder in folders:
        provenance.append({'round':folder.name,'manifest':str((folder/'manifest.json').relative_to(ROOT)).replace('\\','/'),'manifest_sha256':sha(folder/'manifest.json')})
        for version in VERS:
            for idx in read(folder/'manifest.json')['task_ids']:
                rs={p:read(folder/f'repeat-0/{p}/{version}/{idx}/result.json') for p in POLS}
                for p in POLS:
                    path=folder/f'repeat-0/{p}/{version}/{idx}/result.json';r=rs[p]
                    paired.append({'round':folder.name,'strategy':p,'version':version,'idx':idx,'source':path.relative_to(ROOT).as_posix(),'sha256':sha(path),
                        'tf':r['eval_result']['aggregate']['task_fulfillment_mean'],'pe':r['eval_result']['aggregate']['planning_and_efficiency_mean'],
                        'tf_delta_no_update':r['eval_result']['aggregate']['task_fulfillment_mean']-rs['no_update']['eval_result']['aggregate']['task_fulfillment_mean']})
    save(ROOT/'artifacts'/CAMPAIGN/f'{ordinal}-round-paired-evidence.json',{'sources':provenance,'records':paired})
    lines=[f'# Comparable summary across {ordinal} rounds','',f"Collected {now()}; {combined['total_records']} scored observations, 18 distinct tasks, {ordinal} observations per combination.",'',
        '| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS mean ± sample SD of round means |','|---|---:|---:|---:|---:|']
    for s in combined['strategies']:lines.append('| '+s['strategy']+' | '+' | '.join(f"{s['stages'][v]['tf']:.2f} / {s['stages'][v]['pe']:.2f}" for v in VERS)+f" | {s['ecs_mean']:.3f} ± {s['ecs_sample_sd']:.3f} |")
    lines+=['','Complete round metrics, recovery/retention, phased costs, and sample SDs of TF/PE round means: '+f'[`{ordinal}-round-comparison.json`](../../artifacts/{CAMPAIGN}/{ordinal}-round-comparison.json)。',
        '',f'Per-record provenance and same-task/version paired differences: [`{ordinal}-round-paired-evidence.json`](../../artifacts/{CAMPAIGN}/{ordinal}-round-paired-evidence.json)。',
        '','Fixed-setting stability repetitions. SD uses round means, not individual tasks, and establishes neither significance nor universal superiority. Judge blind spots, the 18-task subset, and the single auxiliary variant remain limitations.']
    (pub.PUBLIC/f'ROUND_{ordinal}_SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def run_round(index,resume=False):
    name=NAMES[index];folder=ROOT/'runs'/name;ordinal=index+1
    if index==2:
        plan=read(ROOT/'artifacts'/CAMPAIGN/'second-new-round-plan.json')
        if plan['output_name']!=name or not read(ROOT/'artifacts'/CAMPAIGN/'second-new-round-path-validation.json')['passed']:raise RuntimeError('Second new round directory predeclaration not verified')
        if plan['config_sha256']!=sha(ROOT/'configs/experiment.json'):raise RuntimeError('Second new round configuration changed after predeclaration')
    state('loading_actor',f'Preparing round {ordinal} (additional round {index})',round=name);model('actor')
    state('executing',f'Executing round {ordinal}; saving each result',round=name)
    args=[sys.executable,ROOT/'scripts/repeat_runner.py',folder]
    if resume and folder.exists():args.append('--resume')
    command(args,name+'-execution.log')
    finalize(folder,apply=True)
    a=audit(folder);save(folder/'analysis/execution-audit.json',a)
    if not a['recorded_invariants_pass'] or a['found']!=162:raise RuntimeError('Execution incomplete or unscoreable failure: '+str(a['issues']))
    state('loading_judge',f'Round {ordinal} execution records complete; loading judge');model('judge')
    state('scoring',f'Scoring round {ordinal}; preserving existing scores and execution evidence')
    command([sys.executable,ROOT/'scripts/judge_with_capacity.py',folder],name+'-scoring.log')
    state('verifying',f'Auditing round {ordinal} completeness, sources, and statistics')
    a=audit(folder);save(folder/'analysis/invariant-audit.json',a)
    if not a['complete_and_evaluated'] or not inspect(folder)['complete']:raise RuntimeError('Scored round did not pass strict 162-row audit')
    command([sys.executable,'-m','tool_adapt','analyze',folder],name+'-summary.log')
    compare(folder);preserve_old()
    c=scored_report(folder,ordinal);aggregate_views(ordinal)
    if read(folder/'analysis/judge-capacity.json')!=read(ROOT/'runs/final-v1/analysis/judge-capacity.json'):raise RuntimeError('Judge receipt differs from original')
    with LOCK:
        state('publishing',f'Round {ordinal} scoring audit passed; publishing evidence; next-round gate not yet passed')
        receipt=verified_status();released=pub.release(folder,receipt['commit'])
        with (pub.PUBLIC/f'ROUND_{ordinal}_RESULTS.md').open('a',encoding='utf-8') as f:f.write('\n\nPublic evidence: '+released['release']['url']+'\n\nAnonymous download verified; SHA-256: `'+released['sha256']+'`。\n')
        state('round_published',f'Round {ordinal} scored, published, and remotely verified')
        final_receipt=verified_status()
        save(RUNTIME/(name+'-gate.json'),{'completed_at':now(),'scored':162,'release_verified':released,'publish_verified':final_receipt,'compatible':c['compatible']})

def acquire():
    folder=ROOT/'runtime/dashboard';folder.mkdir(parents=True,exist_ok=True);guard=(folder/'control.lock').open('a+b');guard.seek(0);guard.write(b'0');guard.flush();guard.seek(0)
    import msvcrt
    msvcrt.locking(guard.fileno(),msvcrt.LK_NBLCK,1)
    # Existing terminal experiments must finish before any model switch.
    text=subprocess.check_output([SHELL,'-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'python' } | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],text=True,encoding='utf-8',creationflags=NO_WINDOW)
    rows=json.loads(text) if text.strip() else [];rows=[rows] if isinstance(rows,dict) else rows
    patterns=['-m tool_adapt run','-m tool_adapt judge','repeat_runner.py','judge_with_capacity.py','run_full_pipeline.py','resume_scoring.py','verify_final_workflow.py']
    if any(r['ProcessId']!=os.getpid() and any(p in (r.get('CommandLine') or '') for p in patterns) for r in rows):guard.close();raise RuntimeError('Another experiment is active')
    return guard
def main():
    p=argparse.ArgumentParser();p.add_argument('--resume',action='store_true');a=p.parse_args();RUNTIME.mkdir(parents=True,exist_ok=True)
    guard=acquire();awake=False
    try:
        if not read(ROOT/'artifacts'/CAMPAIGN/'preflight.json')['compatible_preconditions']:raise RuntimeError('Preflight not passed')
        if not read(ROOT/'artifacts'/CAMPAIGN/'runtime-dependency-verification.json')['passed']:raise RuntimeError('Actual runtime dependencies not verified')
        smoke=read(ROOT/'artifacts'/CAMPAIGN/'smoke-verification.json')
        if not smoke.get('actual_resume_skip_verified') or not smoke['audit']['complete_and_evaluated']:raise RuntimeError('Actual development path verification required')
        awake=bool(ctypes.windll.kernel32.SetThreadExecutionState(0x80000001))
        if not awake:raise RuntimeError('Could not request process-lifetime sleep prevention')
        state('prepared','Preparation status published; starting staged execution',awake_request=True,controller_started_at=now())
        verified_status();threading.Thread(target=heartbeat,daemon=True).start()
        for index in [1,2]:
            gate=RUNTIME/(NAMES[index]+'-gate.json')
            if gate.exists():
                g=read(gate)
                if g.get('scored')!=162 or not inspect(ROOT/'runs'/NAMES[index])['complete']:raise RuntimeError('Prior gate no longer valid')
                continue
            if index==2:
                prior=RUNTIME/(NAMES[1]+'-gate.json')
                if not prior.is_file():raise RuntimeError('First new round publication gate missing')
                if now()>='2026-10-29T12:00:00+08:00':
                    state('waiting_team','R2 published; the 12:00 target has passed; R3 has not started and requires a team decision');verified_status();return
            run_round(index,a.resume)
        state('completed','Both additional rounds scored, verified, and published; pool only compatible rounds');verified_status()
    except Exception as e:
        state('blocked',str(e)+'; R3 cannot bypass an unmet publication gate')
        try:verified_status()
        except Exception as publication_error:save(RUNTIME/'blocked-publication-error.json',{'at':now(),'error':str(publication_error)})
        raise
    finally:
        STOP.set()
        if awake:ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        guard.close()
if __name__=='__main__':main()
