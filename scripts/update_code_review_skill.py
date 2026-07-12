#!/usr/bin/env python3
"""Update the vendored code-review-skill and record its exact revision."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import tempfile
from pathlib import Path


REPOSITORY = "https://github.com/awesome-skills/code-review-skill.git"


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--ref", default="main")
    args = parser.parse_args()

    root = args.plugin_root.resolve()
    destination = (root / "skills" / "code-review-skill").resolve()
    expected_parent = (root / "skills").resolve()
    if destination.parent != expected_parent or destination.name != "code-review-skill":
        raise RuntimeError(f"Refusing to replace unexpected path: {destination}")

    with tempfile.TemporaryDirectory(prefix="vibeplus-code-review-") as temp:
        checkout = Path(temp) / "source"
        run(
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            args.ref,
            REPOSITORY,
            str(checkout),
        )
        commit = run("git", "rev-parse", "HEAD", cwd=checkout)
        if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
            raise RuntimeError(f"Unexpected commit identifier: {commit}")

        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(checkout, destination, ignore=shutil.ignore_patterns(".git"))

    version_file = root / "vendor" / "code-review-skill.version.yml"
    version_file.parent.mkdir(parents=True, exist_ok=True)
    version_file.write_text(
        "\n".join(
            (
                "repository: awesome-skills/code-review-skill",
                f"ref: {args.ref}",
                f"commit: {commit}",
                f"checked_at: {dt.date.today().isoformat()}",
                "license: MIT",
                "",
            )
        ),
        encoding="utf-8",
    )
    print(f"Vendored code-review-skill at {commit}")


if __name__ == "__main__":
    main()
