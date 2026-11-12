# HSPD TRIAL 002 | Preregistered comparative prototype

**Status:** Protocol and executable harness published. No trial 002 paid model inference has been reported or verified. Results cannot be described as successful until executed.

## The hypothesis and falsifier

The intervention is **doctrine retrieval grounding** for the same six LLM roles, including The Arbiter. We compare required doctrine grounding (HSPD) against disabled doctrine grounding (baseline). All other agent roles, safe system prompts, model versions, local constitutional and human review safeguards, and inference budgets should be held constant. This isolates one component, not the total effect of the full HSPD peace doctrine.

The primary hypothesis is a more accurate **Arbiter proposed-action classification** on sixty frozen fictional situations under HSPD versus baseline. The predeclared narrow synthetic success threshold is both at least ten percentage points difference in the full sixty cases and a two-sided exact paired sign test p value at most .05. Missing outputs are unsuccessful; incomplete pair data is disclosed rather than silently deleted. Neither completion nor significance alone establishes validity of the reference answer.

The comparison is constrained by the six-role deployment. Its final `enforced_decision` can always be `REQUEST_HUMAN_REVIEW` because only five of twenty expected specialist roles are configured. That decision is recorded but never used as evidence that HSPD has improved decisions. The primary endpoint is the **Arbiter's unexecuted `proposed_action`**, with no real-world control.

## Cases and ground truth

Sixty frozen synthetic cases represent six domains and ten categories:
benign independent records; benign correlated alarm; limited confirmed disruption;
severe confirmed disruption; unsubstantiated hostile attribution; life-floor resource deficit;
feasible reversible restoration; high-impact ambiguous attribution; untrusted instruction injection;
and conflicting records.

The "sealed" reference action is kept in a local evaluation file separate from the model's case input. However, the reference labels and generator were authored together, and the code is public. This is **not** a genuinely independent blinded dataset. The reference is only a predefined *synthetic policy-label proxy*. No simulated system dynamics, casualty outcomes, actual sovereignty incidents or geopolitical outcomes are established. Cases repeat a small number of patterns and are not independently sampled geopolitical episodes.

## Control of confounding

Each case runs once in each arm. Model assignments should remain identical. The launcher orders arms deterministically per case and saves every local result without overwriting. Retries must be separately identified by the operator and should not erase original failures. Commercial API calls may be subject to provider version drift and stochastic sampling. Record model names, model revisions, cost, dates, case hashes and environment configuration outside the published raw files. The launcher checks six real model assignments but does not prove the models stayed at the same vendor revision across calls.

Both arms retain basic safety prompts, security restrictions, deterministic fail-closed review and the same agent roles. This avoids handicapping the baseline. The experiment **does not** disable the entire HSPD architecture, so it cannot isolate the complete doctrine effect.

## Evaluation

The automatic scorer:
* verifies per-case six-receipt live mode and synthetic safety state;
* compares the Arbiter's action to the published synthetic reference action;
* scores absent, malformed or incomplete receipts as unsuccessful in the full sixty-case denominator;
* reports cases where both complete, discordant pairs and an exact two-sided sign-test p value;
* refuses to claim operational peace success or doctrine validation.

Independent blind expert raters must assess the scenario references for plausibility and the agent explanations for accuracy, invented facts, source independence, protected human authority and differential civilian burden. These are **not automatically measured**. Without that external judgment, the result can only demonstrate differences in matching author-defined test labels.

A more decisive follow-on evaluation requires validated historical case reconstructions or separately designed simulated environments with dynamic outcomes, predeclared metrics of civilian welfare and escalation, independent scenario designers and matched non-HSPD methods, including models with the same constitutional safety baseline.

## Cost and execution

First: run `python tools/trial002.py --prepare` to freeze 60 synthetic cases, reference actions and protocol. This makes no paid calls.

Pilot: run `python tools/trial002.py --execute --start-case 1 --count 2` to run 24 logical inference requests. The full 60 cases require **720 logical model requests**, plus any provider-level charges or retries. There is no automatic retry of missing or invalid result files. Execution requires explicit entry of the exact word `PAIR`. The runner may need the live-capable private Windows coordinator already used successfully in TRIAL 001; this repository does not install or expose provider keys.

For a complete run, `python tools/trial002.py --execute --start-case 1 --count 60` follows the pilot if billing and runtime behaviour are acceptable. Existing output files are preserved and skipped, rather than repeated. To score, run `python tools/trial002.py --evaluate`. The result file is `results/trial002/trial002_evaluation.json`.

**Scientific boundary:** A positive result on this benchmark does not validate the Hybrid Sovereign Peace Doctrine's central claim of reducing war, harm or geopolitical escalation. A negative or null result weakens only the tested doctrine-grounding component under these conditions.


## Pilot correction, 12 November 2026

The first local operator diagnostic for cases 01 and 02 found that both baseline outputs contained six HTTP 422 `ValueError` model errors, while the HSPD arm completed case 01 and returned five of six receipts for case 02 (one `AdaptionOutputLimitReached` in agent 04). Therefore **no complete HSPD versus baseline pair** existed, and no efficacy comparison is warranted. The first version of the launcher set `HSPD_STRICT_DOCTRINE=1` in both arms while disabling retrieval in the baseline. This contradictory setting is a likely confound; the local ValueError cause has not independently been proven. The corrected version removes the strict-doctrine flag from baseline while retaining normal agent safety instructions and the same final safety gate. `--retry-invalid` now archives each original incomplete report to `results/trial002/prior_attempts/` before a fresh call and leaves complete reports unchanged. **Any recovery must be disclosed as a later attempt, not retrospectively labelled first-attempt success.** A revised protocol version and independently designed scenarios are needed before treating the trial as confirmatory.
