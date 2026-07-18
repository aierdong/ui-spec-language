from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validator.assertions import run_assertions


SPEC = {
    "spec": {
        "pages": [
            {
                "id": "login",
                "label": "Sign In",
                "sections": [
                    {
                        "id": "credential-form",
                        "capabilities": [
                            {
                                "id": "authentication",
                                "intent": "verify identity",
                                "requires": [
                                    {
                                        "id": "email",
                                        "kind": "credential",
                                        "label": "Email",
                                        "validation": ["email-format"],
                                    }
                                ],
                                "provides": [
                                    {
                                        "id": "submit",
                                        "intent": "submit",
                                        "label": "Sign In",
                                        "triggers": ["processing"],
                                    }
                                ],
                                "produces": [
                                    {"id": "processing", "label": "Processing"}
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "constraints": [
            {"id": "email-format", "condition": "invalid email", "effect": "validity"}
        ],
    }
}


class AssertionTests(unittest.TestCase):
    def test_supported_matchers_pass(self) -> None:
        expectations = {
            "must-contain": [
                "capability.id == authentication",
                "input.kind in [credential, text]",
                "action.label contains sign (case-insensitive)",
                "action.triggers contains processing",
            ],
            "must-not-contain": [
                "any.id contains cart",
            ],
        }

        report = run_assertions(SPEC, expectations, "assertions")

        self.assertTrue(report.passed)

    def test_parse_failure_is_error(self) -> None:
        report = run_assertions(SPEC, {"must-contain": ["not valid"]}, "assertions")

        self.assertFalse(report.passed)
        self.assertEqual(report.failures[0].rule_id, "CT-ASSERT-PARSE")

    def test_missing_must_contain_fails(self) -> None:
        report = run_assertions(
            SPEC,
            {"must-contain": ["capability.id == shopping-cart"]},
            "assertions",
        )

        self.assertFalse(report.passed)
        self.assertEqual(report.failures[0].rule_id, "MUST-CONTAIN")

    def test_forbidden_match_fails(self) -> None:
        report = run_assertions(
            SPEC,
            {"must-not-contain": ["any.label contains email (case-insensitive)"]},
            "assertions",
        )

        self.assertFalse(report.passed)
        self.assertEqual(report.failures[0].rule_id, "MUST-NOT-CONTAIN")


if __name__ == "__main__":
    unittest.main()
