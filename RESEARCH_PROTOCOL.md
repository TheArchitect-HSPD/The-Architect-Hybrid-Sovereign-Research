# HSPD Sandbox v0.1 — Pre-registration draft (engineering proposal)

**Status:** not peer reviewed; not pre-registered externally; no claims of independently validated efficacy.

## Primary research question

In a controlled synthetic multi-agent-like evidence environment, does **observed-source deduplication and feedback-contamination filtering** reduce unsupported positive alerts compared with a raw majority or confidence-only monitor? What false negatives and attacks remain?

This is a *first component test*, not a test of HSPD's ability to produce peace or of a genuine 21-model swarm.

## Hypotheses (candidate only)

- H1: In the copied-source false-consensus fixture, the candidate Arbiter policy will withhold the alert while the raw-vote baseline will not.
- H2: When multiple independent roots truly support an event, the candidate policy will permit a **human-review alert**.
- H3: With provenance labels forged to simulate independent origins, the candidate policy will fail; this demonstrates that lineage metadata alone is insufficient.
- H4: A single genuine source may not satisfy the candidate threshold, causing false negatives. This demonstrates a precision/recall tradeoff.

These hypotheses are **specified with knowledge of the fixtures** (they are regression checks), so confirmation is not an unbiased empirical estimate. A future dataset must contain withheld randomly generated and independently authored cases.

## Fixtures, controls and intervention

Six labeled cases in `scenarios.json`, each with an explicit claim, severity, observed root, true root (for *scoring only*), simulated confidence, evidence that supports/opposes, and intervention-generated flag.

Each case is evaluated in 3 ablation conditions using identical evidence. The candidate policy receives a filtered view without `actual_root_for_scoring` or `ground_truth`. This is logical separation, **not** security isolation: all fixtures live in one process. Fixture roots are supplied by the scenario author and can be forged. All runs are advisory/no-act.

**No honest claim of truly independent AI agents:** A/B analyses are simulated policy functions using the same record set, without independent model weights or data collection. All roles execute inside one program. A hardened sandbox has not yet been built.

## Measured fields

- Positive alert (`REQUEST_HUMAN_REVIEW`) / hold (`HOLD_UNCERTAINTY`).
- Toy binary label agreement for known true/false fixture worlds; **do not interpret as real-world classification accuracy**.
- Number of raw records and distinct *observed* source roots; intervention data excluded.
- Recorded dissent, source conflicts and unresolved alternatives.
- Replay checksum and complete synthetic role trace.

**Future independent experiments must measure:** false-alarm and missed-alert rates across held-out scenarios, calibration, ambiguity/abstention coverage, costs and latency, propagation of wrong claims through actual isolated model instances, ability of compromised agents to tamper with logs, treatment of vulnerable population outcomes, and security escape attempts.

## Deliberately included failure cases

- `spoofed_source_origins`: provenance IDs lie; candidate Arbiter mistakenly recommends review of a false claim.
- `single_source_true`: legitimate urgent claim with only one supporting independent origin; candidate Arbiter withholds.

These cases must be retained in future presentations to avoid selective reporting.

## Required next steps before a scientific validation claim

1. Version and freeze a research protocol and source dataset before held-out tests.
2. Replace individual role stubs with separate processes / isolated memory and real LLM backends, where safe.
3. Secure the environment (no default access to network, credentials, files, or real-world tools).
4. Increase fixture diversity with independent adversarial case authors; verify genuine ground truth.
5. Run blinded scoring and compare raw majority, simple monitor, provenance guard, diversity interventions, and no-guard ablation.
6. Repeat across model families, random seeds affecting **behaviour**, varied model temperatures / population sizes, and diverse causal assumptions.
7. Measure false positives, false negatives, abstention, calibration, burden distribution and computational costs; include confidence intervals and limitations.
8. Invite external reviewers to attempt spoofed provenance, correlated reasoning, privilege escalation and constitutional constraint violations.

## Safety / dual-use

Only fictional medical-supply claims are represented. There is no command interface to real hospitals, emergency communications, sanctions, weapons or public information feeds. The existence of a tool for detecting corrupted sources may itself be susceptible to evasion: forged roots demonstrate one way a monitor can be misled. Details of real system access or offensive sabotage are outside this prototype. All real decisions remain human-controlled.

## Relation to Apart Research sprint

Primary Track 1: reproducible synthetic testbed. Secondary Track 4: monitor/forensics prototype. This is a **starting artifact** requiring model integration, domain realism and independent evaluation before being a competitive research submission.
