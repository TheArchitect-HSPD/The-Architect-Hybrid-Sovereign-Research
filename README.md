# The Architect — GitHub Pages navigation repair v0.5

## What this fixes
The earlier releases expected nested `agents/`, `arbiter/` and `sandbox/` folders to be deployed intact. Missing or misplaced folders produced 404 responses from an older `404.html` that also had a broken relative return link.

This **self-contained root `index.html` embeds all three existing research tools in full**: their HTML, CSS, scripts, full 7,087-passage doctrine corpus, 20-agent profiles, evidence-gate demo and synthetic sandbox. Internal links use root hash navigation; the research tools do not require any extra files or folders.

The included `404.html` redirects old directory URLs to the corresponding embedded workspace on the homepage, and uses an absolute project-root return path.

## Installation — ONLY TWO FILES NEEDED
1. Open your GitHub repository at `https://github.com/TheArchitect-HSPD/The-Architect-Hybrid-Sovereign-Research/`.
2. In the repository file list, use **Add file → Upload files**.
3. Drag in `index.html` and `404.html` from this repair package, **not the ZIP itself**. Confirm they appear at the same level as the existing README, not inside another folder.
4. Commit changes to `main`. Wait for the Pages deployment shown in **Actions** or **Settings → Pages**.
5. Open `https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/` and use links to the three workbenches.
6. Hard refresh with Ctrl+F5 to avoid cached old navigation. Existing old folders may remain; the repaired homepage no longer needs them.

## Single-file deep links
- `/#agent-library` — 20 Agent Doctrine Library
- `/#arbiter-lab` — Arbiter research workbench
- `/#arbiter-gate` — evidence gate tab
- `/#experimental-sandbox` — synthetic testbed

Full public URL must include the repository name before the hash.

## Limitations
This is a static GitHub Pages implementation, not running independent AI models. Source-authenticity, real-world evidence and model verdicts are not independently verified. User-supplied doctrine manuscripts are embedded in the single file, meaning they are publicly readable if deployed.

## Compatibility
No external JavaScript, stylesheets or fonts. Tested using local Chromium with GitHub Pages-style subpath hosting. The iframe workbenches are embedded via srcdoc and scripts are inlined; no network calls are used.
