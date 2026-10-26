"""Researcher command-line interface for the HSPD synthetic sandbox. Stdlib only."""
import argparse
import json
from pathlib import Path
from engine import run_case, batch, csv_text, SCENARIOS, MODES


def main():
    parser=argparse.ArgumentParser(description='HSPD deterministic policy sandbox (not a live multi-agent system).')
    parser.add_argument('--scenario', choices=list(SCENARIOS), default='copied_false_consensus')
    parser.add_argument('--mode', choices=MODES, default='arbiter')
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--batch', type=int, metavar='N', help='Run all scenarios and modes for N seeds each; CSV output')
    parser.add_argument('--output', type=Path, help='Write JSON or CSV to this path, otherwise print to console')
    args=parser.parse_args()
    if args.batch:
        data=csv_text(batch(args.batch))
    else:
        data=json.dumps(run_case(args.scenario,args.seed,args.mode),indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding='utf-8')
        print(f'Wrote {args.output}')
    else:
        print(data)


if __name__=='__main__':
    main()
