"""Add a compact, evidence-bounded SHIELD 21 research banner to the giant homepage.

The October 2026 homepage is a large, self-contained academic workbench whose
inline corpus and scripts must remain unchanged. This program inserts or updates
one recognisable banner immediately after the opening <body> element.

No source manuscripts or private sandbox artefacts are imported. It is safe
to re-run and does not contact any provider or alter the embedded workbenches.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
START = "<!-- SHIELD21_PUBLIC_STATUS_START -->"
END = "<!-- SHIELD21_PUBLIC_STATUS_END -->"

BANNER = """<!-- SHIELD21_PUBLIC_STATUS_START -->
<section aria-labelledby="shield21-site-banner" style="position:relative;z-index:9999;background:linear-gradient(110deg,#112839,#133d3b);color:#edf9fc;border-bottom:2px solid #65cbbd;padding:18px 22px;font-family:system-ui,Arial,sans-serif">
  <div style="max-width:1150px;margin:auto;display:flex;align-items:center;gap:18px;justify-content:space-between;flex-wrap:wrap">
    <div style="flex:1 1 420px;min-width:250px">
      <span style="font-size:11px;color:#98f0df;text-transform:uppercase;font-weight:800;letter-spacing:.13em">Research update | 10 November 2026</span>
      <h2 id="shield21-site-banner" style="font:600 clamp(17px,2.2vw,23px)/1.25 system-ui,Arial,sans-serif;margin:6px 0 5px;color:#f4fcff">HSPD SHIELD 21: full live 21-agent federation test PASSED</h2>
      <p style="margin:0;font:14px/1.6 system-ui,Arial,sans-serif;color:#d0e3eb">The full HSPD SHIELD 21 federation has now returned 21/21 accepted real LLM assessments in one coordinated synthetic test: twenty specialists and a separate Arbiter, zero failed agents, and deterministic REQUEST_HUMAN_REVIEW enforcement with no real-world actions. This is verified from the operator-shared console summary; the complete local JSON report remains unpublished and independently unaudited. The embedded browser labs below remain historical deterministic demonstrations.</p>
    </div>
    <a href="shield21.html" style="display:inline-block;background:#89e3d4;color:#0d202d;padding:12px 17px;border-radius:9px;font:800 13px/1.3 system-ui,Arial,sans-serif;text-decoration:none;white-space:nowrap">Read the November 2026 update</a>
  </div>
</section>
<!-- SHIELD21_PUBLIC_STATUS_END -->"""


def inject(source: str) -> str:
    if source.count(START) > 1 or source.count(END) > 1:
        raise ValueError("Duplicated banner markers; refusing to modify")
    if START in source or END in source:
        if START not in source or END not in source:
            raise ValueError("Unmatched banner markers; refusing to modify")
        start, end = source.index(START), source.index(END) + len(END)
        if end <= start:
            raise ValueError("Invalid marker order")
        return source[:start] + BANNER + source[end:]
    match = re.search(r"<body\b[^>]*>", source, flags=re.IGNORECASE)
    if match is None:
        raise ValueError("Homepage has no opening body element")
    return source[:match.end()] + "\n" + BANNER + source[match.end():]


def main() -> None:
    original = INDEX.read_text(encoding="utf-8")
    revised = inject(original)
    if original == revised:
        print("Homepage status banner already current")
        return
    INDEX.write_text(revised, encoding="utf-8")
    print("Homepage status banner inserted without changing inline research corpus")


if __name__ == "__main__":
    main()
