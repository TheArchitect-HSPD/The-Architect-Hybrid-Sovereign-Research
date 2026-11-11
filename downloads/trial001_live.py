"""HSPD TRIAL 001: synthetic six-role live integration pilot.

Run with --execute --authorise-cloud-doctrine --count 1 only after a passing dry run.
This validates six-model receipt completeness and enforced safety, not doctrine efficacy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = Path(__file__).with_name("author_cases.json")
OUTPUT = ROOT / "results" / "trial001_live"
AGENTS = [f"agent-{i:02d}" for i in range(1, 6)] + ["agent-21"]

def load_cases():
    cases = json.loads(CASE_FILE.read_text(encoding="utf-8"))
    assert isinstance(cases, list) and len(cases) == 30, "Expected 30 cases"
    assert len({case["id"] for case in cases}) == 30, "Duplicate case IDs"
    return cases

def event_for(case):
    signals = [
        {
            "id": "OBS-%03d" % (i + 1),
            "domain": case["domain"],
            "description": "Synthetic report %s the fictional corridor incident. Claimed root is unauthenticated." % ("supports" if src["supports"] else "disputes"),
            "source": str(src["root"]),
            "reliability": float(src["confidence"]),
            "severity": 0.75 if src["supports"] else 0.35
        }
        for i, src in enumerate(case["evidence"])
    ]
    return {
        "scenario_id": case["id"],
        "title": "HSPD TRIAL001 synthetic " + case["domain"],
        "classification": "SYNTHETIC TEST DATA ONLY",
        "description": "Author-generated fictional evidence with withheld truth, unverified origins, and mandatory human review. No real-world actions.",
        "research_question": "Identify source correlation, competing explanations, uncertainty, and constitutional constraints; request human review where needed.",
        "signals": signals,
        "research_limitations": {
            "source_authenticity": "NOT_PROVIDED",
            "structured_constitutional_evidence": "NOT_PROVIDED",
            "structured_safeguards": "NOT_PROVIDED",
            "human_review_required": True,
            "real_world_actions_enabled": False
        }
    }

def verify_runtime(python):
    env_models = {f"agent-{i:02d}" for i in range(1, 22) if os.getenv(f"HSPD_MODEL_AGENT_{i:02d}", "").strip()}
    if env_models != set(AGENTS):
        raise RuntimeError("Exactly six agent model assignments required; configured: " + ", ".join(sorted(env_models)))
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ADAPTION_API_KEY"):
        if not os.getenv(key):
            raise RuntimeError("Missing provider credential environment variable: " + key)
    result = subprocess.run([python, str(ROOT/"run_sandbox.py"), "--help"], cwd=ROOT,
                            capture_output=True, text=True, timeout=20)
    for feature in ("--real-only", "--require-live-agent", "--scenario", "--output"):
        if result.returncode != 0 or feature not in result.stdout:
            raise RuntimeError("Local coordinator lacks required live-only feature " + feature + "; no provider calls made.")

def check_report(path, scenario):
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("scenario_id") != scenario or obj.get("real_world_actions_enabled") is not False:
        raise RuntimeError("Invalid scenario or safety receipt")
    if obj.get("enforced_decision") != "REQUEST_HUMAN_REVIEW":
        raise RuntimeError("Missing mandatory human-review decision")
    rows = obj.get("specialists", [])
    valid = {r.get("agent_id") for r in rows if isinstance(r, dict)
             and r.get("status") in ("ASSESSED", "ABSTAIN") and r.get("mode") == "llm"}
    arb = obj.get("arbiter", {})
    if arb.get("status") in ("ASSESSED", "ABSTAIN") and arb.get("mode") == "llm":
        valid.add("agent-21")
    return valid

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true")
    p.add_argument("--authorise-cloud-doctrine", action="store_true")
    p.add_argument("--start-case", type=int, default=1)
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--continue-on-incomplete", action="store_true", help="Preserve failed reports, continue next case without retries")
    a = p.parse_args()
    if a.start_case < 1 or a.count < 1 or a.start_case + a.count > 31:
        p.error("Choose cases within 1 to 30")
    cases = load_cases()
    selected = cases[a.start_case-1:a.start_case-1+a.count]
    print("HSPD TRIAL 001 | Cases:", len(selected), "| Maximum logical calls:", len(selected)*6)
    print("Case file SHA256:", hashlib.sha256(CASE_FILE.read_bytes()).hexdigest())
    print("Synthetic only; withheld answers never sent; no real-world action.")
    if not a.execute:
        print("OFFLINE PREFLIGHT PASS. Zero provider calls.")
        return
    if not a.authorise_cloud_doctrine:
        p.error("--execute requires --authorise-cloud-doctrine")
    verify_runtime(sys.executable)
    if input("Type LIVE to authorize cloud model charges: ").strip() != "LIVE":
        raise SystemExit("Cancelled")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({"HSPD_STRICT_DOCTRINE":"1", "HSPD_DOCTRINE_MODE":"required",
                "HSPD_ALLOW_DOCTRINE_CLOUD":"1"})
    failures = []
    completed = 0
    for case in selected:
        event = event_for(case)
        label = case["id"]
        event_path = OUTPUT/(label+"_input.json")
        report_path = OUTPUT/(label+"_live.json")
        if event_path.exists() or report_path.exists():
            raise SystemExit("Refusing overwrite for "+label)
        event_path.write_text(json.dumps(event, indent=2)+"\n", encoding="utf-8")
        args = [sys.executable, str(ROOT/"run_sandbox.py"), "--scenario", str(event_path),
                "--output", str(report_path), "--real-only", "--parallel", "2"]
        for aid in AGENTS:
            args.extend(["--require-live-agent", aid])
        result = subprocess.run(args, cwd=ROOT, env=env, timeout=1200,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode or not report_path.exists():
            message = "Runner returned nonzero status or no report"
            print(label, "ERROR:", message, flush=True)
            failures.append({"case_id": label, "error": message})
            if not a.continue_on_incomplete:
                raise SystemExit("Incomplete live case. Stopping.")
            continue
        try:
            valid = check_report(report_path, label)
            missing = sorted(set(AGENTS) - valid)
            print(label, "valid live receipts:", len(valid), "/6",
                  "missing:", ", ".join(missing) or "none", flush=True)
        except (ValueError, TypeError, KeyError, RuntimeError, OSError, json.JSONDecodeError) as exc:
            print(label, "INVALID REPORT:", type(exc).__name__, str(exc)[:160], flush=True)
            failures.append({"case_id": label, "error": type(exc).__name__})
            if not a.continue_on_incomplete:
                raise SystemExit("Invalid report. Stopping.")
            continue
        if valid != set(AGENTS):
            failures.append({"case_id": label, "missing_agents": missing})
            if not a.continue_on_incomplete:
                raise SystemExit("Incomplete six-model trial. Stopping.")
        else:
            completed += 1
    print("Batch outcome:", completed, "complete of", len(selected),
          "| incomplete or failed:", len(failures))
    if failures:
        print("Retained incomplete cases:", ", ".join(f["case_id"] for f in failures))
    print("Doctrine effectiveness NOT proven.")


if __name__ == "__main__":
    main()
