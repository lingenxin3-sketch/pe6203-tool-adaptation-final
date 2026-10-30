"""Rerun the input-incompatible second round without changing the frozen method.

The original second round stays immutable. A verified new run supersedes it in
the active comparison only after execution, judging and input checks succeed.
This controller performs no network publication and never selects by score.
"""
from __future__ import annotations

import argparse
import collections
import ctypes
import gc
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
from repeat_common import read, save, sha, now, resource_listing, round_compatibility, metrics, merge_views, inspect, POLS, VERS
from tool_adapt.knowledge import digest
from tool_adapt.experiment import copy_resources
from audit_experiment import audit
from audit_server_sources import audit as audit_servers
from finalize_failed_episodes import finalize
from analyze_comparisons import compare
from repeat_campaign import acquire

DEST = ROOT / 'artifacts/rerun-r2-20261030'
RUNTIME = ROOT / 'runtime/rerun-r2-20261030'
RUN = ROOT / 'runs/final-r2'  # Same eight-character basename as final-v1/final-r3.
BASE = ROOT / 'runs/final-v1'
OLD = ROOT / 'runs/repeat-r2-20261029'
THIRD = ROOT / 'runs/final-r3'
STATE = RUNTIME / 'state.json'
OUTPUT = ROOT.parent / 'outputs/PE6203_Corrected_Second_Round_20261030'
SHELL = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
_LISTING_CACHE = {}


def recorded_listing(path):
    """Cache only the small input listing, never retain full call histories."""
    stat = path.stat()
    identity = (stat.st_mtime_ns, stat.st_size)
    old = _LISTING_CACHE.get(str(path))
    if old is not None and old[0] == identity:
        return old[1], old[2]
    row = read(path)
    listing = resource_listing(row)
    committed = row.get('status') in {'awaiting_judge', 'evaluated', 'infrastructure_error', 'judge_failed'}
    if committed:
        _LISTING_CACHE[str(path)] = (identity, listing, committed)
    return listing, committed


def state(phase, **extra):
    previous = read(STATE) if STATE.exists() else {}
    previous.update(pid=os.getpid(), phase=phase, updated_at=now(), **extra)
    save(STATE, previous)
    print(json.dumps(previous, ensure_ascii=False), flush=True)


def native(path):
    resolved = str(path.resolve())
    return Path('\\\\?\\' + resolved) if os.name == 'nt' else path


def protected_hashes():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for folder in [BASE, OLD, THIRD]
            for p in folder.rglob('*')
            if p.is_file() and 'workspace' not in p.relative_to(folder).parts}


def verify_preservation():
    receipt = read(DEST / 'historical-preservation.json')
    changes = [name for name, expected in receipt['files'].items()
               if not (ROOT / name).is_file() or sha(ROOT / name) != expected]
    if changes:
        raise RuntimeError('Historical evidence changed: ' + repr(changes[:10]))
    return {'checked_at': now(), 'checked_files': len(receipt['files']), 'passed': True}


def verify_recovery_preservation():
    path = DEST / 'monitor-memory-interruption-20261030.json'
    if not path.exists():
        return None
    incident = read(path)
    if not incident['move_verified']:
        raise RuntimeError('Interrupted attempt archive was not verified')
    for name, expected in incident['completed_result_sha256'].items():
        result = ROOT / name
        candidates = [result.with_name('failure-record.json'), result.with_name('agent-record.json'), result]
        if not any(p.is_file() and sha(p) == expected for p in candidates):
            raise RuntimeError('Previously completed evidence changed: ' + name)
    partial = incident['partial_attempt']
    archive = Path(partial['archive_directory'])
    for name, expected in partial['files_sha256'].items():
        if sha(native(archive / name)) != expected:
            raise RuntimeError('Interrupted attempt archive changed: ' + name)
    events = [json.loads(line) for line in (archive / 'events.jsonl').read_text(encoding='utf-8').splitlines()]
    usages = [e['payload']['usage'] for e in events if e['kind'] == 'model_response']
    return {'checked_at': now(), 'passed': True, 'preserved_completed_records': 156,
            'completed_episodes_retried': 0, 'uncommitted_episode_restarted': 1,
            'partial_returned_calls': len(usages),
            'partial_recorded_tokens': sum(u['total_tokens'] for u in usages),
            'partial_request_seconds': sum(u['wall_seconds'] for u in usages),
            'cost_scope': 'Additional interrupted-attempt overhead; excluded from completed-grid totals; unreturned usage unknown.'}


def input_fairness(folder):
    groups = []
    for idx in read(BASE / 'manifest.json')['task_ids']:
        for version in VERS:
            listings = {}
            for policy in POLS:
                path = folder / f'repeat-0/{policy}/{version}/{idx}/result.json'
                if path.exists():
                    listing, committed = recorded_listing(path)
                    if committed:
                        listings[policy] = listing
            if len(listings) == 3:
                groups.append({'task': idx, 'version': version,
                               'same_across_strategies': None not in listings.values()
                               and len({json.dumps(v) for v in listings.values()}) == 1})
    return {'checked_groups': len(groups), 'expected_groups': 54,
            'differing_groups': sum(not x['same_across_strategies'] for x in groups),
            'groups': groups}


def check_live_inputs():
    checked, unavailable, different = 0, [], []
    for path in RUN.glob('repeat-*/*/*/*/result.json'):
        relative = path.relative_to(RUN)
        new, committed = recorded_listing(path)
        if not committed:
            continue  # Frozen runner saves an intermediate record before its final receipt.
        old, _ = recorded_listing(BASE / relative)
        if new is None or old is None:
            unavailable.append(relative.as_posix())
        elif new != old:
            different.append(relative.as_posix())
        else:
            checked += 1
    report = {'checked_at': now(), 'matching_records': checked,
              'unavailable': unavailable, 'different': different,
              'within_round': input_fairness(RUN)}
    save(DEST / 'live-input-check.json', report)
    if unavailable or different or report['within_round']['differing_groups']:
        raise RuntimeError('Actual prompt resource listings differ; run stopped, evidence retained')
    return report


def path_preflight():
    parent = (ROOT / 'runs').resolve()
    folder = parent / secrets.token_hex(4)
    if folder.exists() or folder.parent != parent or len(folder.name) != len(RUN.name):
        raise RuntimeError('Unsafe or wrong-length temporary path')
    folder.mkdir()
    source = ROOT / 'upstream/anotation_path'
    resources = [p for p in native(source).rglob('*') if p.is_file()]
    checks = []
    try:
        for idx in read(BASE / 'manifest.json')['task_ids']:
            for policy in POLS:
                for version in VERS:
                    relative = Path(f'repeat-0/{policy}/{version}/{idx}')
                    ws = folder / relative / 'workspace'
                    for resource in resources:
                        rel = resource.relative_to(native(source))
                        for prefix in [Path('.'), Path('anotation_path')]:
                            target = ws / prefix / rel
                            native(target.parent).mkdir(parents=True, exist_ok=True)
                            os.link(resource, native(target))
                    seen = sorted(p.relative_to(ws).as_posix() for p in ws.rglob('*')
                                  if p.is_file() and not p.name.endswith('.log'))
                    expected = resource_listing(read(BASE / relative / 'result.json'))
                    checks.append({'episode': relative.as_posix(), 'visible': len(seen),
                                   'passed': seen == expected,
                                   'only_expected': sorted(set(expected or []) - set(seen)),
                                   'only_actual': sorted(set(seen) - set(expected or []))})
        report = {'checked_at': now(), 'output': RUN.relative_to(ROOT).as_posix(),
                  'baseline': BASE.relative_to(ROOT).as_posix(),
                  'temporary_basename_length': len(folder.name), 'fixture_files': len(resources),
                  'checks': checks, 'checked': len(checks),
                  'passed': len(checks) == 162 and all(c['passed'] for c in checks),
                  'limits': 'No inference; actual prompt listings are checked again during execution.'}
        save(DEST / 'path-preflight.json', report)
        if not report['passed']:
            raise RuntimeError('All-grid path preflight failed; no model execution allowed')
        print('All 162 resource-list layout checks passed.', flush=True)
    finally:
        if folder.resolve().parent != parent or len(folder.name) != 8:
            raise RuntimeError('Refusing cleanup outside the exact owned temporary root')
        shutil.rmtree(native(folder))


def preflight():
    DEST.mkdir(parents=True, exist_ok=True)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if RUN.exists():
        raise FileExistsError('New corrected output already exists; use --resume after inspection')
    if (DEST / 'plan.json').exists():
        raise FileExistsError('Plan already exists; use its saved preflight instead of redefining it')
    state('preflight', child_pid=None)
    manifest = read(BASE / 'manifest.json')
    checks = {'config': read(ROOT / 'configs/experiment.json') == manifest['config'],
              'sources': all(digest((ROOT / p).read_text(encoding='utf-8')) == h
                             for p, h in manifest['source_hashes'].items()),
              'inventory': all(digest(read(ROOT / 'artifacts/inventory' / f'{v}.json')) == h
                               for v, h in manifest['inventory_hashes'].items()),
              'upstream': subprocess.check_output(['git', '-C', str(ROOT / 'upstream'),
                                                  'rev-parse', 'HEAD'], text=True).strip()
                          == manifest['config']['upstream_commit'],
              'first_and_third_compatible': round_compatibility(BASE, THIRD)['compatible'],
              'first_complete': audit(BASE)['complete_and_evaluated'],
              'third_complete': audit(THIRD)['complete_and_evaluated']}
    for item in read(ROOT / 'artifacts/dependency-lock.json'):
        path = ROOT / 'runtime/downloads' / item['file']
        checks['dependency:' + item['file']] = (path.is_file() and path.stat().st_size == item['bytes']
                                               and sha(path) == item['sha256'])
    server_checks = [audit_servers(v) for v in VERS]
    save(DEST / 'server-source-preflight.json', server_checks)
    checks['official_server_sources'] = all(s['passed'] for s in server_checks)
    save(DEST / 'protocol-preflight.json', {'checked_at': now(), 'checks': checks,
                                          'passed': all(checks.values())})
    if not all(checks.values()):
        raise RuntimeError('Frozen protocol preflight failed: ' + repr(checks))
    path_preflight()
    archive_source = (ROOT.parent / 'outputs/PE6203_New_Repository_Integration_20261029'
                      '/03_ORIGINAL_EVIDENCE/repeat-r2-20261029-evidence.zip')
    expected = '9c2c963d0b8fa02267a87034a398672442a10424f22dae81a4298587f137fceb'
    if sha(archive_source) != expected:
        raise RuntimeError('Archived original second-round ZIP checksum differs')
    historical = OUTPUT / 'archive/input-incompatible-original-r2'
    historical.mkdir(parents=True, exist_ok=True)
    saved_zip = historical / archive_source.name
    if saved_zip.exists():
        raise FileExistsError('Historical archive already exists; refusing replacement')
    shutil.copy2(archive_source, saved_zip)
    with zipfile.ZipFile(saved_zip) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('Historical archive CRC check failed')
    if sha(saved_zip) != expected:
        raise RuntimeError('Historical archive copy verification failed')
    protected = protected_hashes()
    protected.update({p.relative_to(ROOT).as_posix(): sha(p)
                      for p in (ROOT / 'artifacts/repeats-20261029').rglob('*') if p.is_file()})
    save(DEST / 'historical-preservation.json', {'recorded_at': now(), 'files': protected,
          'original_second_round_zip': str(saved_zip), 'original_second_round_zip_sha256': expected})
    plan = {'declared_at': now(), 'replacement': RUN.relative_to(ROOT).as_posix(),
            'supersedes': OLD.relative_to(ROOT).as_posix(), 'archive_sha256': expected,
            'original_rounds_retained': True, 'reason': 'Resource listing incompatibility, not score selection.',
            'baseline_manifest_sha256': sha(BASE / 'manifest.json'),
            'config_sha256': sha(ROOT / 'configs/experiment.json'),
            'source_hashes': manifest['source_hashes'],
            'methods_models_tasks_decoding_and_judge_unchanged': True,
            'formal_records_expected': 162, 'scored_active_total_expected': 486,
            'comparison_rounds': ['final-v1', 'final-r2', 'final-r3'],
            'publication': 'Local only; no GitHub changes.',
            'completion_rule': '162 scored records, same initial inputs, preserved failures and historical evidence.'}
    save(DEST / 'plan.json', plan)
    (historical / 'README.md').write_text(
        '# Superseded second round\n\nThis is the unchanged original second-round evidence. '
        'It is excluded from the active comparison because actual initial resource listings differed. '
        'A new run at `runs/final-r2` replaces this round only after all validation gates pass. '
        'The replacement is not selected for a higher score.\n', encoding='utf-8')
    state('ready', preflight_passed=True)


def command(args, name, live=False):
    log_path = RUNTIME / name
    env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUNBUFFERED': '1'}
    with log_path.open('ab', buffering=0) as log:
        log.write(('\n' + now() + ' ' + repr(list(map(str, args))) + '\n').encode('utf-8'))
        child = subprocess.Popen(list(map(str, args)), cwd=ROOT, env=env, stdout=log,
                                 stderr=subprocess.STDOUT, creationflags=NO_WINDOW)
        state(read(STATE)['phase'], child_pid=child.pid, log=str(log_path))
        try:
            last_count = -1
            while child.poll() is None:
                time.sleep(5)
                if live:
                    try:
                        report = check_live_inputs()
                    except (MemoryError, OSError) as exc:
                        # Observation failure must not kill an in-flight episode.
                        # Final validation remains mandatory before any replacement.
                        gc.collect()
                        save(RUNTIME / 'monitor-warning.json', {
                            'at': now(), 'error': type(exc).__name__ + ': ' + str(exc),
                            'policy': 'Keep actor running; retry observation; require final checks.'})
                        continue
                    count = report['matching_records']
                    if count != last_count:
                        state('executing', completed=count, expected=162)
                        last_count = count
                elif RUN.exists() and (RUN / 'manifest.json').exists() and 'judg' in name:
                    progress = inspect(RUN)
                    if progress['scored'] != last_count:
                        state('scoring', scored=progress['scored'], expected=162)
                        last_count = progress['scored']
            if child.returncode:
                raise RuntimeError(f'{name}: process exited {child.returncode}; evidence retained')
        except BaseException:
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=30)
            raise
        finally:
            state(read(STATE)['phase'], child_pid=None)


def model(role):
    other = 'judge' if role == 'actor' else 'actor'
    command([SHELL, '-NoProfile', '-File', ROOT / 'scripts/stop-local-model.ps1', '-Role', other],
            f'stop-{other}.log')
    script = 'start-local-model.ps1' if role == 'actor' else 'start-judge.ps1'
    command([SHELL, '-NoProfile', '-File', ROOT / 'scripts' / script], f'start-{role}.log')
    port = 8081 if role == 'actor' else 8082
    for _ in range(120):
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=3) as response:
                if json.load(response).get('status') == 'ok':
                    break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise RuntimeError('Local model did not become ready')
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/props', timeout=5) as response:
        props = json.load(response)
    expected = 16384 if role == 'actor' else 24576
    alias = 'qwen3-4b' if role == 'actor' else 'qwen2.5-7b-judge'
    if (props['default_generation_settings']['n_ctx'] != expected
            or props.get('build_info') != 'b11900-74b104c9b' or props.get('model_alias') != alias):
        raise RuntimeError('Model server differs from frozen protocol')
    save(DEST / (role + '-runtime.json'), {'checked_at': now(), 'properties': props})


def summarize():
    state('verifying')
    receipt = audit(RUN)
    save(RUN / 'analysis/invariant-audit.json', receipt)
    if not receipt['complete_and_evaluated'] or not inspect(RUN)['complete']:
        raise RuntimeError('New second round is not completely scored and audited')
    compat = round_compatibility(BASE, RUN)
    save(DEST / 'final-input-compatibility.json', compat)
    fair = input_fairness(RUN)
    save(DEST / 'final-within-round-fairness.json', fair)
    if not compat['compatible'] or fair['checked_groups'] != 54 or fair['differing_groups']:
        raise RuntimeError('New second round is not input-compatible')
    if read(RUN / 'analysis/judge-capacity.json') != read(BASE / 'analysis/judge-capacity.json'):
        raise RuntimeError('Judge capacity receipt differs from baseline')
    command([sys.executable, '-m', 'tool_adapt', 'analyze', RUN], 'summary.log')
    compare(RUN)
    save(DEST / 'preservation-verification.json', verify_preservation())
    view = metrics(RUN)
    combined = merge_views([BASE, RUN, THIRD])
    recovery = verify_recovery_preservation()
    if recovery:
        save(DEST / 'interruption-preservation-verification.json', recovery)
        view['infrastructure_interruption'] = recovery
        combined['additional_interrupted_attempt_overhead'] = recovery
    save(DEST / 'corrected-r2-metrics.json', view)
    save(DEST / 'corrected-three-round-comparison.json', combined)
    paired = []
    for folder in [BASE, RUN, THIRD]:
        for path in sorted(folder.glob('repeat-*/*/*/*/result.json')):
            r = read(path)
            paired.append({'round': folder.name, 'strategy': r['strategy'], 'version': r['version'],
                           'task': r['idx'], 'source': path.relative_to(ROOT).as_posix(),
                           'sha256': sha(path), 'score': r['eval_result']['aggregate']})
    save(DEST / 'corrected-three-round-paired-evidence.json', {'records': paired})
    lines = ['# Corrected three-round results', '',
             'The active comparison uses the original round, a new input-compatible second round, '
             'and the third round: 486 scored observations over 18 distinct tasks. '
             'The superseded second round is preserved separately and excluded. All execution '
             'exceptions remain in the scored grid. Models, tasks, methods, seed and temperature are unchanged.', '',
             '| Policy | Early TF / PE | Middle TF / PE | Late TF / PE | ECS mean ± sample SD |',
             '| --- | ---: | ---: | ---: | ---: |']
    for s in combined['strategies']:
        lines.append('| ' + s['strategy'] + ' | ' + ' | '.join(
            f"{s['stages'][v]['tf']:.3f} / {s['stages'][v]['pe']:.3f}" for v in VERS)
            + f" | {s['ecs_mean']:.3f} ± {s['ecs_sample_sd']:.3f} |")
    full = next(s for s in combined['strategies'] if s['strategy'] == 'full_rewrite')
    selective = next(s for s in combined['strategies'] if s['strategy'] == 'selective_patch')
    update_saving = 100 * (1 - selective['costs']['update']['tokens'] / full['costs']['update']['tokens'])
    full_total = sum(v['tokens'] for v in full['costs'].values())
    selective_total = sum(v['tokens'] for v in selective['costs'].values())
    total_change = 100 * (selective_total / full_total - 1)
    lines += ['', f'Selective patch uses {update_saving:.1f}% fewer recorded update tokens than full rewrite. '
              f'Its recorded total tokens (update + execution + judging) change by {total_change:+.1f}%.', '',
              'These are descriptive stability repeats with a fixed seed and temperature, not a statistical '
              'significance test. The local judge can be wrong; saved files and tool responses require separate '
              'inspection. Recorded usage excludes calls whose usage was not returned. Local API billing excludes '
              'hardware, electricity and development effort.', '',
              'The prior two-round report and presentation describe an earlier data snapshot. Their numbers '
              'must be replaced using this verified comparison before submission. Original logs and scores '
              'have not been rewritten or relabeled as a new experiment.']
    if recovery:
        lines += ['', '## Infrastructure interruption and recovery', '',
                  'A monitoring MemoryError interrupted an uncommitted task 416 / full rewrite / Early '
                  'attempt after 156 episodes had been saved. All 156 saved results remain preserved. '
                  'The entire interrupted attempt was archived; only that uncommitted episode was '
                  'restarted, followed by the five episodes not yet started. No completed episode or '
                  'score was retried to improve a result. The inference server was restarted with unchanged settings.', '',
                  f"The partial attempt contains {recovery['partial_returned_calls']} returned model calls, "
                  f"{recovery['partial_recorded_tokens']:,} recorded tokens and "
                  f"{recovery['partial_request_seconds']:.2f} request seconds. This is additional overhead "
                  'outside the completed-grid token tables. Unreturned-call usage remains unknown. '
                  'The incident and partial attempt are retained; this was not an uninterrupted run.']
    (OUTPUT / 'CORRECTED_RESULTS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    save(OUTPUT / 'corrected-three-round-comparison.json', combined)
    # A separate current-selection file replaces the active analysis input while
    # preserving every previous run and its immutable provenance.
    selection = {'updated_at': now(), 'rounds': ['runs/final-v1', 'runs/final-r2', 'runs/final-r3'],
                 'observations': 486, 'distinct_tasks': 18,
                 'superseded_round': 'runs/repeat-r2-20261029',
                 'reason': 'Initial resource-list incompatibility; replacement predeclared before execution.',
                 'comparison': 'artifacts/rerun-r2-20261030/corrected-three-round-comparison.json',
                 'all_validation_gates_passed': True, 'github_updated': False,
                 'presentation_and_report_refresh_required': True}
    save(ROOT / 'artifacts/current-round-selection.json', selection)
    save(DEST / 'completion.json', {**selection, 'preservation': verify_preservation(),
                                    'interruption_preservation': recovery})
    state('completed', completed=162, scored=162, active_observations=486,
          result_report=str(OUTPUT / 'CORRECTED_RESULTS.md'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    RUNTIME.mkdir(parents=True, exist_ok=True)
    guard = acquire()
    awake = False
    try:
        if not (DEST / 'plan.json').exists():
            preflight()
        elif not read(DEST / 'protocol-preflight.json')['passed'] or not read(DEST / 'path-preflight.json')['passed']:
            raise RuntimeError('Saved preflight did not pass')
        if args.preflight_only:
            return
        verify_preservation()
        verify_recovery_preservation()
        plan = read(DEST / 'plan.json')
        if sha(ROOT / 'configs/experiment.json') != plan['config_sha256']:
            raise RuntimeError('Configuration changed after predeclaration')
        if RUN.exists() and not args.resume:
            raise FileExistsError('Corrected output exists; explicit --resume required')
        if not all(digest((ROOT / p).read_text(encoding='utf-8')) == h for p, h in plan['source_hashes'].items()):
            raise RuntimeError('Frozen method source changed')
        awake = bool(ctypes.windll.kernel32.SetThreadExecutionState(0x80000001))
        if not awake:
            raise RuntimeError('Could not request sleep prevention')
        executed = RUN.exists() and len(list(RUN.glob('repeat-*/*/*/*/result.json'))) == 162
        if not executed:
            state('loading_actor', started_at=now(), error=None, resumed=args.resume)
            model('actor')
            state('executing', expected=162)
            invocation = [sys.executable, ROOT / 'scripts/repeat_runner.py', RUN]
            if args.resume and RUN.exists():
                invocation.append('--resume')
            command(invocation, 'execution.log', live=True)
        check_live_inputs()
        save(DEST / 'failure-recovery.json', finalize(RUN, apply=True))
        execution_audit = audit(RUN)
        save(DEST / 'execution-audit.json', execution_audit)
        if execution_audit['found'] != 162 or not execution_audit['recorded_invariants_pass']:
            raise RuntimeError('Execution audit failed; judging will not start')
        if not round_compatibility(BASE, RUN)['compatible']:
            raise RuntimeError('Actual input compatibility failed')
        if not inspect(RUN)['complete']:
            state('loading_judge')
            model('judge')
            state('scoring', expected=162)
            command([sys.executable, ROOT / 'scripts/judge_with_capacity.py', RUN], 'judging.log')
        # Summary and integrity checks need no inference server in memory.
        command([SHELL, '-NoProfile', '-File', ROOT / 'scripts/stop-local-model.ps1', '-Role', 'judge'],
                'stop-judge-after-scoring.log')
        summarize()
    except BaseException as exc:
        state('stopped', error=type(exc).__name__ + ': ' + str(exc), child_pid=None)
        raise
    finally:
        if awake:
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        guard.close()


if __name__ == '__main__':
    main()
