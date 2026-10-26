# The Architect — HSPD Research Site, doctrinally integrated 21-agent reference architecture (v0.4)

**Purpose:** Existing GitHub Pages research website expanded with source-referenced design specifications for the 20 specialist agents and retained Arbiter Lab for Agent XXI.

**Entry points**
- `index.html` — original homepage, 20-agent roster, doctrine and link to Agent Doctrine Library.
- `agents/index.html` — interactive Agent Doctrine Library: 20 profiles, 160 proposed skills, source quotes, falsification scenarios, bounded instructions, case-specific search and export.
- `agents/AGENT_PROFILES.json` — complete 20-agent candidate specifications; includes proposed input/output contracts, limits and source references.
- `agents/CAPABILITY_REGISTRY_20_AGENTS.csv` — candidate skills and one falsification test per skill.
- `agents/DOCTRINAL_SOURCE_LINKS.csv` — exact source passage IDs, book/chapter, text and mapping status.
- `arbiter/index.html` — preserved Agent XXI Arbiter Lab with search, 24 candidate capabilities and deterministic evidence gate.
- `arbiter/knowledge.js` — full shared 7,087-passage doctrine library from the two books and v1.1 addendum.
- `sandbox/index.html` — prior six-case deterministic experimental sandbox.
- `AGENTS.csv` — original roster, retained unchanged.
- `SOURCE_METHOD.md` — sources, method, review obligations and unresolved gaps.
- `VALIDATION_CHECKLIST.md` — steps to turn these role specifications into independent models and real experiments.

**Experimental status:** No real 20-agent model runtime has been deployed; the pages are a browsable doctrinal specification and a limited deterministic testing interface. The heroic names and machine-readable skills are subsequent AI-assisted design proposals, not claims about words literally in the books. Proposed source matches are candidates for the author to approve. This is a research draft, not independently validated performance.

**Publication:** The website embeds the complete extracted manuscript text in `arbiter/knowledge.js`. Confirm you want those complete texts publicly accessible on GitHub and check your Amazon/KDP distribution terms.

**Deploy:** Extract the ZIP; upload the *contents* to the public repository root, retaining `index.html`, `agents/`, `arbiter/`, and `sandbox/`; commit to `main`. If folder uploads are awkward, use GitHub Desktop to copy the folders into a cloned repo before committing. The website works as static files with relative links; no API keys required.

**Research authenticity:** The entire author-supplied 7,087-passage library is referenced from one shared corpus; each specialist role has a source-scoped profile, not a separate trained language model. It would require an isolated runtime, authenticated inputs, human-authority controls, an independent inference backend and external evaluation to substantiate ability. Never put model API keys in a public GitHub Pages site.
