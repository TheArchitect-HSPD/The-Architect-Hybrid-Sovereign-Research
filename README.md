# The Architect / Hybrid Sovereign Research

The public GitHub Pages site documents the Hybrid Sovereign Peace Doctrine (HSPD), the proposed twenty-one-role architecture, the Arbiter, historical synthetic research, and the November 2026 HSPD SHIELD 21 hosted LLM assessment pilot.

**Current live research status (10 November 2026):** Four hosted LLM model pools cover twenty specialist roles, with a separate LLM Arbiter. Operator-shared console output documents the first complete-cohort live run as PASS_ALL_REQUIRED_LIVE: 20 accepted specialist LLM assessments and one separate Arbiter response, with zero failed agents, REQUEST_HUMAN_REVIEW enforced and real-world actuation disabled. The full private JSON report has not been independently audited or published.

The original, very large `index.html` embeds the October 2026 browser research workbenches and a doctrine corpus. Those browser workbenches remain deterministic demonstrations. They do not connect directly to the private HSPD SHIELD 21 Windows sandbox.

## Start here

1. [Homepage](https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/#home) displays the latest research announcement above the preserved historical workbenches.
2. [HSPD SHIELD 21 update](https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/shield21.html) explains four model pools, live successes and failures, corrections, the Arbiter and remaining experimental limits.
3. [Architecture](https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/architecture.html) describes all twenty roles and the Arbiter.
4. [Research](https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/research.html) distinguishes the historical synthetic exercises from hosted LLM research.
5. [Evidence ledger](https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/evidence.html) identifies source types and evidentiary limits.

## November 2026 work

The experimental SHIELD 21 federation uses four specialist model pools of five worker roles each: OpenAI GPT 4.1 Mini, Anthropic Claude Haiku 5.5, Gemma 4 31B via Adaption, and Gemma 4 26B via Adaption. The Arbiter is separate and was evaluated with OpenAI GPT 6.1 Sol in the reported trials. Two of the models use the same family and inference gateway, so their outputs are not independent corroboration. Agents use local isolated processes with scoped doctrine retrieval, not separately trained weights.

An expanded pilot exposed real output-budget failures. Anthropic truncation was resolved with larger output ceilings for agents 06 and 10. DeepSeek V4 Flash used its entire reasoning-token allowance without final text on agents 08 and 12; Qwen 3.8 27B also returned an incomplete assessment. Gemma 4 26B then passed all five fourth-pool roles individually at a 4,096-token budget. The reported local offline suite passed 339 tests.

The 21/21 live outcome demonstrates that the software can complete the full model assessment pipeline on one synthetic scenario. It does not demonstrate inference accuracy, a validated prediction of geopolitical events, institutional endorsement, operational control, or achievement of the doctrine's peace KPIs.

## Privacy and safety

The public website contains no API keys, local federation result JSON, private runtime configuration or new unpublished doctrine document uploads. The original October 2026 homepage already includes embedded doctrine passages, so repository publication settings and intellectual property implications require the author's review.

The LLM federation is restricted to explicitly synthetic scenarios, has no real-world actuation and enforces human review through a deterministic gate. The Arbiter is an epistemic reviewer, not an authority over political truth, public belief, justice or ideology.

## Legacy documentation

The previous website release was a self-contained homepage navigation repair. The root HTML embeds earlier doctrine library, Arbiter Lab and toy sandbox tools. The original deep links remain:

* `/#agent-library` for the historical doctrine library
* `/#arbiter-lab` for the deterministic Arbiter workbench
* `/#arbiter-gate` for its evidence-gate tab
* `/#experimental-sandbox` for the synthetic browser sandbox

The large `index.html` is updated by the guarded `tools/refresh_shield21_home.py` script and its GitHub Actions workflow, which insert a short status announcement without replacing the embedded research material.

See [Research limitations](RESEARCH_LIMITATIONS.md), [research protocol](RESEARCH_PROTOCOL.md), and [citation metadata](CITATION.cff).

© The Architect. Publishing this website does not grant an open-source licence to the underlying doctrine or manuscripts.
