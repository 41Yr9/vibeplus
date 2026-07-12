#!/usr/bin/env python3
"""Validate files and compatibility assumptions used by Vibeplus."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
require(manifest.get("name") == "vibeplus-plugin", "Unexpected plugin name")
require(manifest.get("skills") == "./skills/", "Plugin must expose the skills directory")

marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
require(marketplace.get("name") == "vibeplus", "Unexpected marketplace name")
entries = marketplace.get("plugins", [])
require(len(entries) == 1, "Marketplace must expose exactly one plugin")
require(entries[0].get("name") == manifest.get("name"), "Marketplace and manifest plugin names differ")
require(entries[0].get("source", {}).get("path") == ".", "Marketplace must point at the repository plugin root")

for name in ("vibeplus", "code-review-skill", "engineering-policy-curator"):
    skill_file = ROOT / "skills" / name / "SKILL.md"
    require(skill_file.is_file(), f"Missing {skill_file}")
    content = skill_file.read_text(encoding="utf-8")
    require(content.startswith("---\n"), f"Missing frontmatter in {skill_file}")
    require(re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", content) is not None, f"Wrong skill name: {name}")

vibeplus = (ROOT / "skills" / "vibeplus" / "SKILL.md").read_text(encoding="utf-8")
require("$code-review-skill" in vibeplus, "Vibeplus must invoke code-review-skill")
require("$engineering-policy-curator" in vibeplus, "Vibeplus must invoke engineering-policy-curator")
require("classify_risk.py" in vibeplus, "Vibeplus must use deterministic risk routing")
require((ROOT / "skills" / "vibeplus" / "references" / "risk-routing.json").is_file(), "Missing risk routing rules")

version = (ROOT / "vendor" / "code-review-skill.version.yml").read_text(encoding="utf-8")
require(re.search(r"(?m)^commit: [0-9a-f]{40}$", version) is not None, "Missing pinned commit")
require((ROOT / "skills" / "code-review-skill" / "LICENSE").is_file(), "Missing upstream license")

print("Distribution validation passed")
