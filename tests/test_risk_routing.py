from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "vibeplus" / "scripts" / "classify_risk.py"


def classify(*signals: str, override: str | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT)]
    for signal in signals:
        command.extend(("--signal", signal))
    if override:
        command.extend(("--override", override))
    return subprocess.run(command, text=True, capture_output=True)


class RiskRoutingTests(unittest.TestCase):
    def test_cosmetic_change_is_fast(self) -> None:
        result = classify("cosmetic_only")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["mode"], "fast")

    def test_cross_module_change_is_standard(self) -> None:
        result = classify("multiple_modules")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["mode"], "standard")

    def test_auth_boundary_forces_critical_despite_negative_score(self) -> None:
        result = classify("auth_boundary", "cosmetic_only")
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["mode"], "critical")
        self.assertEqual(output["forced_by"], ["auth_boundary"])

    def test_automatic_override_cannot_lower_risk(self) -> None:
        result = classify("auth_boundary", override="standard")
        self.assertNotEqual(result.returncode, 0)

    def test_evidence_signal_is_required(self) -> None:
        result = classify()
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
