#!/usr/bin/env python3
"""Report whether pinned public sources have newer branch revisions."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references" / "source-catalog.json"


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    drifted = False
    for source in catalog["sources"]:
        result = subprocess.run(
            ["git", "ls-remote", source["repository"], f"refs/heads/{source['ref']}"],
            check=True,
            text=True,
            capture_output=True,
        )
        latest = result.stdout.split()[0]
        status = "current" if latest == source["commit"] else "update-available"
        drifted = drifted or status != "current"
        print(f"{source['id']}: {status} pinned={source['commit']} latest={latest}")
    raise SystemExit(2 if drifted else 0)


if __name__ == "__main__":
    main()
