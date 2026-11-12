"""Patch local native OpenAI doctrine gate for an explicitly marked synthetic TRIAL002 baseline.

Creates agent_server.py.trial002-original.bak and refuses unknown source layouts.
Only the baseline gate is excepted; underlying models, regular safety checks,
provider authentication, real-world-action prohibitions, and default strict
doctrine behaviour remain unchanged.
"""
from __future__ import annotations
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/"agent_server.py"
backup=ROOT/"agent_server.py.trial002-original.bak"
old="""        if (os.environ.get('HSPD_DOCTRINE_MODE') != 'required' or
                os.environ.get('HSPD_ALLOW_DOCTRINE_CLOUD') != '1' or
                os.environ.get('HSPD_DOCTRINE_PUBLIC_SUMMARY_ONLY') == '1'):
            raise ValueError('OpenAI Sol requires authorised full pinned doctrine')"""
new="""        # Research-only paired ablation exception. No doctrine text is provided
        # to models in the baseline; the same synthetic safety gate still runs.
        trial002_baseline = (
            os.environ.get('HSPD_TRIAL002_BASELINE') == '1'
            and os.environ.get('HSPD_DOCTRINE_MODE') == 'off'
            and os.environ.get('HSPD_ALLOW_DOCTRINE_CLOUD') == '0'
            and os.environ.get('HSPD_STRICT_DOCTRINE') != '1'
            and os.environ.get('HSPD_DOCTRINE_PUBLIC_SUMMARY_ONLY') != '1'
        )
        if not trial002_baseline and (
                os.environ.get('HSPD_DOCTRINE_MODE') != 'required' or
                os.environ.get('HSPD_ALLOW_DOCTRINE_CLOUD') != '1' or
                os.environ.get('HSPD_DOCTRINE_PUBLIC_SUMMARY_ONLY') == '1'):
            raise ValueError('OpenAI Sol requires authorised full pinned doctrine')"""
if not target.is_file():
    raise SystemExit("agent_server.py not found; no changes")
content=target.read_text(encoding="utf-8")
if new in content:
    print("ALREADY PATCHED; no changes")
    sys.exit(0)
if content.count(old)!=1:
    raise SystemExit("Expected guard not found exactly once; source may differ; NO CHANGE")
if backup.exists():
    raise SystemExit("Backup path already exists; refusing to replace or change source")
shutil.copy2(target,backup)
patched=content.replace(old,new,1)
try:
    compile(patched,str(target),"exec")
except SyntaxError:
    raise SystemExit("Patched source failed syntax check; original remains unchanged")
target.write_text(patched,encoding="utf-8")
print("PATCH INSTALLED: research-only synthetic baseline exception")
print("Backup:",backup)
print("OpenAI default doctrine requirement remains enforced outside TRIAL002 baseline.")
