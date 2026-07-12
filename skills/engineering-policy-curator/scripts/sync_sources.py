#!/usr/bin/env python3
"""Fetch pinned engineering knowledge sources into a user cache."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG = SKILL_ROOT / "references" / "source-catalog.json"


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def safe_destination(cache: Path, source_id: str) -> Path:
    destination = (cache / source_id).resolve()
    if destination.parent != cache.resolve() or destination.name != source_id:
        raise RuntimeError(f"Unsafe cache destination: {destination}")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, default=Path.home() / ".cache" / "vibeplus" / "sources")
    parser.add_argument("--source", action="append", dest="sources")
    args = parser.parse_args()

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    selected = set(args.sources or [])
    known = {source["id"] for source in catalog["sources"]}
    unknown = selected - known
    if unknown:
        raise RuntimeError(f"Unknown sources: {', '.join(sorted(unknown))}")

    cache = args.cache_dir.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    for source in catalog["sources"]:
        if selected and source["id"] not in selected:
            continue
        destination = safe_destination(cache, source["id"])
        with tempfile.TemporaryDirectory(prefix="vibeplus-policy-") as temp:
            checkout = Path(temp) / "source"
            run("git", "clone", "--filter=blob:none", "--no-checkout", source["repository"], str(checkout))
            run("git", "checkout", "--detach", source["commit"], cwd=checkout)
            actual = run("git", "rev-parse", "HEAD", cwd=checkout)
            if actual != source["commit"]:
                raise RuntimeError(f"Revision mismatch for {source['id']}: {actual}")
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(checkout, destination, ignore=shutil.ignore_patterns(".git"))
        print(f"Synced {source['id']} at {source['commit']} to {destination}")


if __name__ == "__main__":
    main()
