#!/usr/bin/env python3
"""Classify a Vibeplus change from explicit, evidence-backed risk signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "references" / "risk-routing.json"
RANK = {"fast": 0, "standard": 1, "critical": 2}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signal", action="append", default=[])
    parser.add_argument("--override", choices=tuple(RANK))
    args = parser.parse_args()

    rules = json.loads(RULES.read_text(encoding="utf-8"))
    if not args.signal:
        raise SystemExit("At least one evidence-backed risk signal is required")
    known = rules["signals"]
    unknown = sorted(set(args.signal) - set(known))
    if unknown:
        raise SystemExit(f"Unknown signals: {', '.join(unknown)}")

    selected = sorted(set(args.signal))
    score = sum(known[name]["score"] for name in selected)
    if score <= rules["thresholds"]["fast_max"]:
        mode = "fast"
    elif score <= rules["thresholds"]["standard_max"]:
        mode = "standard"
    else:
        mode = "critical"

    forced_by = [name for name in selected if known[name].get("force_mode") == "critical"]
    if forced_by:
        mode = "critical"

    original_mode = mode
    if args.override:
        if RANK[args.override] < RANK[mode]:
            raise SystemExit("Risk mode cannot be lowered by an automatic override; human approval is required")
        mode = args.override

    output = {
        "mode": mode,
        "calculated_mode": original_mode,
        "score": score,
        "signals": [
            {"id": name, "score": known[name]["score"], "description": known[name]["description"]}
            for name in selected
        ],
        "forced_by": forced_by,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
