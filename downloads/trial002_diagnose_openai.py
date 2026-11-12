"""Two-call controlled diagnostic for TRIAL002 OpenAI baseline failures.

Outputs only exception classes and code-frame locations. Never prints raw
provider error messages, prompts, responses, doctrine excerpts, or API secrets.
No real-world action; explicit paid-call consent required.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "results" / "trial002"
CASES = CASE_DIR / "inputs"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    cid = "HSPD-TRIAL002-%02d" % args.case
    event_path = CASES / (cid + ".json")
    baseline_path = CASE_DIR / (cid + "_baseline.json")
    if not event_path.is_file() or not baseline_path.is_file():
        parser.error("Missing case input or baseline output; run TRIAL002 prepare and pilot first")
    event = json.loads(event_path.read_text(encoding="utf-8"))
    previous = json.loads(baseline_path.read_text(encoding="utf-8"))
    if event.get("scenario_id") != cid or previous.get("scenario_id") != cid:
        parser.error("Scenario mismatch")
    for aid in ("agent-01", "agent-21"):
        if not os.getenv("HSPD_MODEL_" + aid.upper().replace("-", "_")):
            parser.error("Missing model assignment for " + aid)
    if not os.getenv("OPENAI_API_KEY"):
        parser.error("OpenAI API key not configured")
    print("Two OpenAI baseline calls only; provider charges possible.")
    print("No raw exception text, credentials, prompts, responses, or doctrine will be printed.")
    if input("Type DIAGNOSE to authorize up to 2 calls: ").strip() != "DIAGNOSE":
        raise SystemExit("Cancelled")
    sys.path.insert(0, str(ROOT))
    from agent_server import find_agent, llm_assessment
    # Match the baseline arm, excluding doctrine context and strict-mode flags.
    os.environ["HSPD_DOCTRINE_MODE"] = "off"
    os.environ.pop("HSPD_STRICT_DOCTRINE", None)
    os.environ["HSPD_ALLOW_DOCTRINE_CLOUD"] = "0"
    reports = [r for r in previous.get("specialists", [])
               if isinstance(r, dict) and r.get("status") in ("ASSESSED", "ABSTAIN")]
    for aid in ("agent-01", "agent-21"):
        os.environ["HSPD_MODEL"] = os.environ["HSPD_MODEL_" + aid.upper().replace("-", "_")]
        # Do not modify or infer configured budgets. Match runtime defaults.
        payload = event if aid == "agent-01" else {"event": event, "reports": reports}
        try:
            result = llm_assessment(find_agent(aid), payload)
            print(aid, "SUCCESS", "status=" + str(result.get("status")),
                  "proposed_action=" + str(result.get("proposed_action")))
        except Exception as exc:
            frames = traceback.extract_tb(exc.__traceback__)
            # Frame locations only, never provider or model-generated strings.
            clean = []
            for frame in frames[-8:]:
                filename = Path(frame.filename).name
                if filename and filename not in ("<string>", "<stdin>"):
                    clean.append("%s:%d:%s" % (filename, frame.lineno, frame.name))
            print(aid, "ERROR_CLASS", type(exc).__name__)
            print(aid, "ERROR_TRACE", " -> ".join(clean) or "NO_FRAMES")
    print("Diagnostic complete; no trial results modified.")

if __name__ == "__main__":
    main()
