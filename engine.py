"""HSPD sandbox v0.1: deliberately non-LLM, deterministic simulation.

This is a toy evidence lineage test harness. It makes NO real-world decisions.
Do not interpret its outcomes as demonstrating feasibility of the HSPD doctrine.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENTS = json.loads((ROOT / 'agents.json').read_text(encoding='utf-8'))
SCENARIOS = json.loads((ROOT / 'scenarios.json').read_text(encoding='utf-8'))
MODES = ('majority', 'confidence', 'arbiter')


def positive_count(evidence):
    return sum(1 for e in evidence if e['supports_claim'])


def base_majority(evidence):
    yes = positive_count(evidence)
    no = len(evidence)-yes
    return {
        'recommendation': 'REQUEST_HUMAN_REVIEW' if yes > no else 'HOLD_UNCERTAINTY',
        'explanation': f'Raw majority: {yes} supporting, {no} opposing. No lineage check.',
        'eligible_roots': None,
        'alerts': ['Baseline counts copied evidence as separate votes.'],
        'confidence_score': round(yes / len(evidence), 3) if evidence else None,
    }


def confidence_monitor(evidence):
    support = sum(e['confidence'] for e in evidence if e['supports_claim'])
    oppose = sum(e['confidence'] for e in evidence if not e['supports_claim'])
    score = support/(support+oppose) if support+oppose else 0
    return {
        'recommendation': 'REQUEST_HUMAN_REVIEW' if score >= 0.7 else 'HOLD_UNCERTAINTY',
        'explanation': f'Confidence-weighted support is {score:.2f}; threshold 0.70. Ignores lineage.',
        'eligible_roots': None,
        'alerts': ['Confidence is a synthetic input, not calibrated probability.'],
        'confidence_score': round(score, 3),
    }


def arbiter_policy(evidence):
    """Proposed *engineering demonstration*, not a quote of doctrine or an ML agent.

    Disallows intervention-derived evidence. Deduplicates observed roots.
    Each root casts at most one vote, and roots with internal contradictions abstain.
    Detecting intentionally falsified provenance is OUT OF SCOPE (tested as failure).
    """
    roots = defaultdict(list)
    excluded = []
    for e in evidence:
        if e['intervention_generated']:
            excluded.append(e['id'])
        else:
            roots[e['observed_root']].append(e)
    root_votes = {}
    conflicted = []
    for root, group in sorted(roots.items()):
        values = set(bool(e['supports_claim']) for e in group)
        if len(values) != 1:
            conflicted.append(root)
        else:
            root_votes[root] = values.pop()
    yes_roots = sum(root_votes.values())
    no_roots = len(root_votes) - yes_roots
    eligible = yes_roots + no_roots
    fraction = yes_roots/eligible if eligible else 0.0
    # Conservative *candidate threshold*, must be evaluated rather than presumed correct.
    affirmative = yes_roots >= 2 and fraction >= 0.67
    alerts = []
    if excluded:
        alerts.append(f'Excluded intervention-generated evidence: {", ".join(excluded)}')
    if conflicted:
        alerts.append(f'Conflicting observations under same root: {", ".join(conflicted)}')
    if len(roots) < len(evidence)-len(excluded):
        alerts.append('Shared upstream roots detected: raw agreement is not independent confirmation.')
    if no_roots:
        alerts.append('Independent contradictory source(s) preserved for human review.')
    if not affirmative:
        alerts.append('Insufficient independent evidence: preserve unknown/other hypothesis.')
    alerts.append('Observed source labels may be spoofed; lineage authenticity is not verified.')
    return {
        'recommendation': 'REQUEST_HUMAN_REVIEW' if affirmative else 'HOLD_UNCERTAINTY',
        'explanation': (f'Observed independent roots: {yes_roots} supporting / {no_roots} opposing; '
                        f'{len(conflicted)} internally conflicted, {len(excluded)} excluded. '
                        'Candidate rule: >=2 supporting roots and >=0.67 support share.'),
        'eligible_roots': root_votes,
        'alerts': alerts,
        'confidence_score': round(fraction, 3),
    }


def run_case(scenario_id='copied_false_consensus', seed=1, mode='arbiter'):
    if mode not in MODES:
        raise ValueError(f'Unknown mode {mode!r}')
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 10_000_000:
        raise ValueError('Seed must be an integer from 0 to 10,000,000.')
    if scenario_id not in SCENARIOS:
        raise ValueError(f'Unknown scenario {scenario_id!r}')
    sc = copy.deepcopy(SCENARIOS[scenario_id])
    # Do not give the policy the evaluator-only actual origin of a forged source.
    evaluator_actual_roots = {e['id']: e['actual_root_for_scoring'] for e in sc['evidence']}
    ev = [{k: v for k, v in e.items() if k != 'actual_root_for_scoring'} for e in sc['evidence']]
    random.Random(seed).shuffle(ev)
    trace = []

    def record(name, role, message, phase='simulated_policy'):
        trace.append({'seq': len(trace)+1, 'agent': name, 'role': role, 'phase': phase, 'message': message})

    domain_agents = AGENTS[:8]
    for a in domain_agents:
        context = sc['domain_context'].get(a['domain'], 'No domain-specific event in this toy case')
        record(a['name'], a['role'], f'Context only: {context}. No external action or domain model.', 'context_stub')

    votes = [e['supports_claim'] for e in ev]
    record('Solvyr', 'Independent analyst A', f'Blind synthetic first-pass: {sum(votes)} supporting / {len(votes)-sum(votes)} opposing. Sources not independently verified.')
    record('Elyrion', 'Independent analyst B', f'Independent policy pass (same input records): weighted confidence {confidence_monitor(ev)["confidence_score"]:.2f}. Not an independent model instance.')
    record('Thornev', 'Independent challenge', 'Preserve contradictory observations; challenge consensus and source reuse.' if len(set(votes)) > 1 else 'No contradictory observation present; still require independent verification.')
    unique_roots = sorted(set(e['observed_root'] for e in ev))
    record('Orivane', 'Provenance auditing', f'{len(ev)} records identify {len(unique_roots)} observed upstream roots. Root identifiers may be falsified.')
    record('Kaelrix', 'Causal and falsification review', 'Keep claim true / claim false / unknown open; synthetic causal mechanisms are not verified.')
    record('Varrun', 'Defensive-cost review', f'Synthetic evidence-processing cost: {len(ev)} units; real computation costs not measured.')
    record('Farreth', 'Priority and tail-risk review', f'Scenario priority label: {sc["severity"]}; no actual triage undertaken.')
    record('Elyndra', 'Civilian burden review', 'Human impacts remain simulated; no population consequences are enacted.')
    record('Oathryn', 'Constitutional review', 'All outcomes advisory only; consequential actions require external human authority.')
    record('Synthera', 'System orchestration', f'Run mode {mode}; seed {seed}; data order randomized but no network messaging.')
    record('Scarveth', 'Audit, replay and versioning', 'Exact inputs, role labels and outputs included in downloadable trace.')
    record('Umbrakar', 'Independent red-team', sc['attack_description'])
    if mode == 'arbiter':
        decision = arbiter_policy(ev)
        record('The Arbiter', 'Evidence-integrity oversight', decision['explanation'] + ' Advisory only.', 'active_policy')
    else:
        decision = base_majority(ev) if mode == 'majority' else confidence_monitor(ev)
        record('The Arbiter', 'Evidence-integrity oversight', 'Disabled in this ablation condition.', 'disabled')
    expected = sc['ground_truth']
    # 'request review' ≠ approve/act. For the score, it is a *positive classification* only.
    predicted_positive = decision['recommendation'] == 'REQUEST_HUMAN_REVIEW'
    result = {
        'schema_version': '0.1', 'experiment_type': 'synthetic_deterministic_policy_test',
        'not_a_live_ai_swarm': True, 'scenario_id': scenario_id, 'scenario_title': sc['title'],
        'claim': sc['claim'], 'seed': seed, 'mode': mode,
        'agent_registry_count': len(AGENTS), 'implemented_independent_llm_agents': 0,
        'evidence': ev, 'ground_truth': expected,
        'evaluator_actual_roots': evaluator_actual_roots,
        'labels_withheld_from_candidate_policy': True,
        'labels_not_security_isolated': True,
        'recommendation': decision['recommendation'],
        'positive_classification': predicted_positive,
        'correct_classification': None if expected is None else predicted_positive == expected,
        'confidence_score': decision['confidence_score'],
        'explanation': decision['explanation'], 'alerts': decision['alerts'],
        'observed_root_votes': decision['eligible_roots'],
        'trace': trace,
        'limitations': [
            'Every role is a deterministic stub/policy in one Python process; none is an independent LLM.',
            'No operating-system sandbox or security boundary is implemented.',
            'Ground truth and source provenance are invented for controlled experiments.',
            'Decisions are advisory labels, never permission to act in the world.',
            'Apparent source independence can be spoofed; the candidate Arbiter policy fails on that case.',
        ],
    }
    # Digest excludes itself and only commits to deterministic, serialized results.
    encoded = json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    result['sha256'] = hashlib.sha256(encoded.encode('utf-8')).hexdigest()
    return result


def batch(n=30, scenario_ids=None):
    if n < 1 or n > 500:
        raise ValueError('Use between 1 and 500 seeds')
    ids = scenario_ids or list(SCENARIOS)
    rows = []
    for sid in ids:
        for mode in MODES:
            for seed in range(n):
                result = run_case(sid, seed, mode)
                rows.append({
                    'scenario': sid, 'mode': mode, 'seed': seed,
                    'ground_truth': str(result['ground_truth']),
                    'recommendation': result['recommendation'],
                    'correct_classification': str(result['correct_classification']),
                    'sha256': result['sha256'],
                })
    return rows


def csv_text(rows):
    import io
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=['scenario', 'mode', 'seed', 'ground_truth', 'recommendation', 'correct_classification', 'sha256'])
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()
