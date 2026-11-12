"""HSPD TRIAL002 isolated Narethyl (agent-05) timing and failure diagnostic.

One paid model call, explicitly authorised. No trial result modification.
Never print private prompts, provider response bodies, API keys, or exception messages.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results" / "trial002" / "inputs" / "HSPD-TRIAL002-02.json"
DEST = ROOT / "results" / "trial002" / "diagnostics"

def safe_usage(obj):
    """Permit only a defined, bounded telemetry schema."""
    if not isinstance(obj, dict):
        return {}
    ret = {}
    for field in ("requested_max_output_tokens", "provider_output_tokens",
                  "provider_reasoning_tokens"):
        value = obj.get(field)
        if type(value) is int and 0 <= value <= 10_000_000:
            ret[field] = value
    for field in ("final_text_present", "reasoning_output_item_present"):
        if type(obj.get(field)) is bool:
            ret[field] = obj[field]
    return ret


def worker():
    """Executed only by the guarded parent process."""
    sys.path.insert(0, str(ROOT))
    from agent_server import find_agent, llm_assessment
    event = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert event.get("scenario_id") == "HSPD-TRIAL002-02"
    start = time.perf_counter()
    try:
        receipt = llm_assessment(find_agent("agent-05"), event)
        print(json.dumps({
            "status": "COMPLETED",
            "elapsed_seconds": round(time.perf_counter() - start, 3),
            "mode": receipt.get("mode"),
            "assessment_status": receipt.get("status"),
            "proposed_action": receipt.get("proposed_action"),
            "reasoning_characters": len(receipt.get("reasoning", "")),
            "alternative_characters": len(receipt.get("alternative_explanation", "")),
        }))
    except Exception as exc:
        safe = safe_usage(getattr(exc, "diagnostics", None))
        if not safe:
            safe = safe_usage(getattr(exc, "safe_generation_diagnostics", None))
        print(json.dumps({
            "status": "ERROR",
            "elapsed_seconds": round(time.perf_counter() - start, 3),
            "exception_class": type(exc).__name__,
            "safe_generation_diagnostics": safe,
        }))
    # Avoid printing worker subprocess traceback, provider response or prompt.

def main():
    ap = argparse.ArgumentParser(description="Single-call Narethyl timed diagnostic")
    ap.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--watchdog-seconds", type=int, default=240)
    args = ap.parse_args()
    if args.worker:
        try:
            worker()
        except Exception as exc:
            frames = traceback.extract_tb(exc.__traceback__)
            safe_frames = [
                "%s:%d:%s" % (Path(f.filename).name, f.lineno, f.name)
                for f in frames[-4:]
            ]
            # Never emit exception strings, arguments, provider payloads or stderr.
            print(json.dumps({
                "status": "WORKER_FAILURE",
                "exception_class": type(exc).__name__,
                "safe_error_frames": safe_frames
            }))
        return
    if not 190 <= args.watchdog_seconds <= 600:
        ap.error("Watchdog must be between 190 and 600 seconds")
    if not SOURCE.is_file():
        ap.error("Case 02 scenario input not found; first prepare TRIAL002")
    if not (ROOT / "agent_server.py").is_file():
        ap.error("Local agent server not found")
    model = os.environ.get("HSPD_MODEL_AGENT_05", "")
    if not model.startswith("adaption/"):
        ap.error("Agent 05 must be assigned a native Adaption model")
    if not os.environ.get("ADAPTION_API_KEY"):
        ap.error("Adaption API credential is missing from this PowerShell session")
    budget_str = os.environ.get("HSPD_MAX_OUTPUT_TOKENS_AGENT_05", "1000")
    try:
        budget = int(budget_str)
    except ValueError:
        ap.error("Invalid Adaption output budget")
    if budget < 64 or budget > 8192:
        ap.error("Adaption output budget must be 64..8192")
    print("NARETHYL ISOLATED TIMING DIAGNOSTIC")
    print("Model role: agent-05 | output budget:", budget, "| watchdog seconds:", args.watchdog_seconds)
    print("One live hosted model call may incur provider charges.")
    print("Doctrine grounding required. No action on real-world systems.")
    print("No result files will be overwritten. Provider content and secrets never printed.")
    if input("Type TIME05 to authorise one live call: ").strip() != "TIME05":
        raise SystemExit("Cancelled before making provider calls")
    env = os.environ.copy()
    env["HSPD_MODEL"] = model
    env["HSPD_DOCTRINE_MODE"] = "required"
    env["HSPD_STRICT_DOCTRINE"] = "1"
    env["HSPD_ALLOW_DOCTRINE_CLOUD"] = "1"
    env.pop("HSPD_TRIAL002_BASELINE", None)
    env["HSPD_ADAPTION_MAX_OUTPUT_TOKENS"] = str(budget)
    env.pop("HSPD_MODEL_API_BASE", None)
    env["PYTHONIOENCODING"] = "utf-8"
    started_at = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    cmd = [sys.executable, str(Path(__file__).resolve()), "--worker"]
    try:
        cp = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True,
                            text=True, timeout=args.watchdog_seconds)
        wall = round(time.perf_counter() - start, 3)
        try:
            result = json.loads(cp.stdout.strip())
            if not isinstance(result, dict) or result.get("status") not in ("ERROR", "COMPLETED"):
                raise ValueError("Invalid worker output")
        except (ValueError, TypeError):
            result = {"status": "WORKER_FAILURE", "exit_code": cp.returncode}
        if cp.returncode != 0:
            result = {"status": "WORKER_FAILURE", "exit_code": cp.returncode}
    except subprocess.TimeoutExpired:
        wall = round(time.perf_counter() - start, 3)
        result = {"status": "WATCHDOG_TIMEOUT",
                  "interpretation": "No worker result before outer watchdog; not proof of provider-origin timeout"}
    record = {
        "diagnostic": "HSPD-TRIAL002-02-agent-05-timing",
        "started_at_utc": started_at,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "trial_result_modified": False,
        "separate_diagnostic_call": True,
        "provider_call_authorised": True,
        "agent": "agent-05",
        "scenario_id": "HSPD-TRIAL002-02",
        "arm": "hspd",
        "output_token_budget": budget,
        "watchdog_seconds": args.watchdog_seconds,
        "wall_elapsed_seconds": wall,
        "worker_result": result,
        "limitations": ["Model/server SDK timeouts may occur internally and are not identifiable from the exception class alone.",
                        "This is a diagnostic run, not a preregistered first-attempt comparison."]
    }
    DEST.mkdir(parents=True, exist_ok=True)
    for n in range(1, 1000):
        target = DEST / ("agent05_timing_%03d.json" % n)
        try:
            with target.open("x", encoding="utf-8") as f:
                json.dump(record, f, indent=2)
                f.write("\n")
            break
        except FileExistsError:
            pass
    else:
        raise SystemExit("No free diagnostic report filename")
    print("Elapsed wall time:", wall, "seconds")
    print("Result:", result.get("status"))
    if result.get("exception_class"):
        print("Exception class:", result["exception_class"])
    if result.get("safe_error_frames"):
        print("Safe frames:", " -> ".join(result["safe_error_frames"]))
    if result.get("elapsed_seconds") is not None:
        print("Worker elapsed:", result["elapsed_seconds"], "seconds")
    if result.get("safe_generation_diagnostics"):
        print("Safe token diagnostics:", json.dumps(result["safe_generation_diagnostics"]))
    if result.get("assessment_status"):
        print("Assessment:", result["assessment_status"], "| proposed action:", result.get("proposed_action"))
    print("Saved:", target)
    print("TRIAL002 original reports unchanged.")

if __name__ == "__main__":
    main()
