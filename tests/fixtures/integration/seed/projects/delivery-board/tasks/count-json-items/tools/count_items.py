"""Synthetic standard-library report for the isolated Vault task-tools pilot."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description="Count items in a JSON array.")
parser.add_argument("--input", required=True, type=Path)
parser.add_argument("--output", required=True, type=Path)
parser.add_argument("--active-only", action="store_true", help="Count only objects whose active field is true.")
args = parser.parse_args()
items = json.loads(args.input.read_text(encoding="utf-8"))
if not isinstance(items, list):
    parser.error("input must be a JSON array")
count = sum(isinstance(item, dict) and item.get("active") is True for item in items) if args.active_only else len(items)
report = {"input_count": len(items), "count": count, "mode": "active-only" if args.active_only else "all"}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
