"""Offline validation of public navigation and interactive lab wiring."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("lab.html", "shield21.html", "research.html", "architecture.html",
         "arbiter.html", "evidence.html", "about.html")

class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs: self.ids.add(attrs["id"])
        for k in ("href", "src"):
            if k in attrs: self.links.append((tag, attrs[k]))

def check():
    errors = []
    parsed = {}
    for filename in PAGES:
        page = ROOT / filename
        if not page.is_file():
            errors.append("Missing page: "+filename)
            continue
        p = Collector()
        p.feed(page.read_text(encoding="utf-8"))
        parsed[filename] = p
    for filename, page in parsed.items():
        for tag, value in page.links:
            dest = urlsplit(value)
            if dest.scheme or dest.netloc or value.startswith(("mailto:", "tel:", "data:")):
                continue
            target = unquote(dest.path)
            if not target or target == "." or target == "./":
                resolved = ROOT / filename
            elif target.startswith("/"):
                # Project Pages uses a repository subpath; avoid root-relative URLs.
                errors.append(f"{filename}: root-relative link {value}")
                continue
            else:
                resolved = (ROOT / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{filename}: link escapes repository: {value}")
                continue
            if not resolved.exists():
                errors.append(f"{filename}: missing target: {value}")
                continue
            if dest.fragment and resolved.name in parsed:
                if dest.fragment not in parsed[resolved.name].ids:
                    errors.append(f"{filename}: missing anchor: {value}")
    lab = (ROOT / "lab.html").read_text(encoding="utf-8")
    for control in ("lab-scenario","lab-run","lab-batch","lab-export","custom-add",
                    "custom-run","lab-trace","lab-file","lab-import-output"):
        if f'id="{control}"' not in lab:
            errors.append("Missing lab control: "+control)
    for name in ("assets/app.js","assets/lab.js","assets/lab.css",
                 "assets/emblem.svg","dataset.js","engine_browser.js"):
        if not (ROOT / name).is_file():
            errors.append("Missing required asset: "+name)
    if errors:
        for err in errors: print("FAIL:",err)
        raise SystemExit(1)
    print(f"PASS: {len(parsed)} public pages, local navigation, anchors, and lab controls checked")
    print("NOTE: external links, remote deployment, and live LLM inference not verified.")

if __name__ == "__main__":
    check()
