# THE ARCHITECT — HSPD Research Site with Integrated Arbiter Lab (v0.3)

**Deployment target:** https://thearchitect-hspd.github.io/The-Architect-Hybrid-Sovereign-Research/

This package replaces the existing GitHub Pages site content. It is a site source package, not a GitHub deployment. Upload its contents to the **root of the public repository** and commit to `main`, preserving the directory structure.

## Included

- `index.html`: existing v0.2 homepage and 21-agent presentation, with prominent **Open Arbiter Lab** buttons.
- `arbiter/index.html`: integrated, responsive, gold/dark themed research workbench.
- `arbiter/knowledge.js`: complete author-supplied manuscript paragraphs, 7,087 searchable passages from both books and addendum.
- `arbiter/app.js`, `arbiter/agent_registry.js`: source search, 24 candidate capability cards, principle quotations, deterministic evidence gate, and 20-role synthetic report intake.
- `arbiter/CHAPTER_INVENTORY.csv`, `arbiter/CAPABILITY_REGISTRY.csv`, `arbiter/SOURCE_CONCORDANCE.csv`: traceable research provenance.
- `sandbox/`: existing separate deterministic HSPD network experiment (6 scenarios, 3 comparison policies).

## Scope and scientific limitations

This works in GitHub Pages **without a backend or API keys**. It is a read-only source browser plus deterministic evaluation software. It **does not deploy 21 independent LLM agents**, authenticate evidence origins, continually learn, call web APIs or reliably determine universal truth. The **24 proposed capabilities and automatic passage matches are candidates**, not validated skills or approved doctrinal rules. The evidence gate's two-independent-root threshold is **experimental**, not doctrine law. All decision traces explicitly prohibit consequential action without human authority.

## PUBLICATION AND RIGHTS — PLEASE READ

The complete text of both books and the adversarial addendum is embedded in `arbiter/knowledge.js` and will be **publicly downloadable** when uploaded to a public GitHub repository. The source DOCX originals are not distributed in this website package, but the extracted paragraphs are nearly all included. Publishing a book on Amazon does not necessarily grant unlimited rights to distribute full text elsewhere if a publisher/Kindle Select agreement applies. You, as author, must confirm that releasing the full text is intentional and compatible with your distribution agreement. If not, use a separately prepared redacted/citation-only corpus instead of uploading this package.

## Upload to GitHub

1. Extract this ZIP to a folder on your Windows computer.
2. Open your existing GitHub repository. Use **Add file → Upload files** and drag the **contents** of the extracted folder (not the enclosing folder) onto the root upload area. Ensure GitHub displays paths `index.html`, `arbiter/index.html`, `arbiter/knowledge.js`, `sandbox/index.html` before committing. GitHub's web interface may require dragging folders individually or using GitHub Desktop to preserve structure.
3. Commit to branch `main`, replacing the old root `index.html`. If the browser won't accept a folder drag, use GitHub Desktop or Git command line: copy the contents into your local checkout, commit, push.
4. After Pages deploys, open the homepage, then `/arbiter/` and `/sandbox/`. Refresh with Ctrl+F5 if cached.

**Do not paste API keys, passwords, private credentials or personal evidence records into this published repo.** The browser workbench runs locally in the visitor's browser and does not send entered case text to a server.

## Local testing

To try the full system without publishing, extract the ZIP, then double-click `index.html` and follow **Open Arbiter Lab**. The links and scripts are all relative.

## Next engineering stage

A separately hosted, authenticated backend could run independent LLM processes, provide controlled source provenance tools, isolate agent contexts and allow pre-registered blinded adversarial evaluations. Do not embed secret model API keys in the GitHub Pages JavaScript.
