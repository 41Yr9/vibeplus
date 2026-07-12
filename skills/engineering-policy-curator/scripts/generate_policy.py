#!/usr/bin/env python3
"""Create a non-destructive engineering policy workspace draft."""

from __future__ import annotations

import argparse
from pathlib import Path


FILES = {
    "AGENTS.md": """# Project agent instructions

<!-- DRAFT: Human approval required before treating these rules as authoritative. -->

## Required workflow

- Read the relevant documents under `docs/engineering/` before planning.
- Record acceptance criteria, tests, risks, and explicit non-goals in each implementation plan.
- Follow approved ADRs and create an ADR for decisions matching `docs/engineering/decisions.md`.
- Do not weaken security, data integrity, or verification requirements without human approval.
""",
    "docs/engineering/index.md": """# Engineering handbook

Status: draft, human approval required.

- [Principles](principles.md)
- [Planning](planning.md)
- [Testing](testing.md)
- [Code review](code-review.md)
- [Security](security.md)
- [Reliability](reliability.md)
- [Delivery](delivery.md)
- [Decisions](decisions.md)
- [Sources](sources.md)
""",
    "docs/engineering/principles.md": "# Engineering principles\n\n<!-- Add approved project-specific principles. -->\n",
    "docs/engineering/planning.md": "# Planning\n\n<!-- Define acceptance criteria, non-goals, risks, and human approval gates. -->\n",
    "docs/engineering/testing.md": "# Testing\n\n<!-- Define test layers, required checks, and handling of unavailable tests. -->\n",
    "docs/engineering/code-review.md": "# Code review\n\n<!-- Define review scope, severity, change size, and merge conditions. -->\n",
    "docs/engineering/security.md": "# Security\n\n<!-- Define trust boundaries, secret handling, and security review triggers. -->\n",
    "docs/engineering/reliability.md": "# Reliability\n\n<!-- Define observability, failure behavior, SLOs, and incident expectations when applicable. -->\n",
    "docs/engineering/delivery.md": "# Delivery\n\n<!-- Define CI/CD, migration, rollout, and rollback requirements. -->\n",
    "docs/engineering/decisions.md": """# Architecture decisions

Create an ADR for changes to public contracts, data models, security boundaries, infrastructure dependencies, or decisions that are costly to reverse.
""",
    "docs/engineering/sources.md": """# Policy sources

Record each adopted policy ID, source repository, path, pinned commit, license, approver, and approval date.
""",
    "docs/engineering/adr/template.md": """# ADR-NNNN: Decision title

- Status: proposed
- Date: YYYY-MM-DD
- Decision owners:

## Context

## Decision

## Alternatives considered

## Consequences

## Revisit when
""",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()
    if not root.is_dir():
        raise RuntimeError(f"Project root does not exist: {root}")

    created = []
    skipped = []
    for relative, content in FILES.items():
        destination = root / relative
        if destination.exists():
            skipped.append(relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8", newline="\n")
        created.append(relative)

    print("Created:")
    for path in created:
        print(f"  {path}")
    print("Preserved existing:")
    for path in skipped:
        print(f"  {path}")


if __name__ == "__main__":
    main()
