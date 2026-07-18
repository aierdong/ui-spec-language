from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validator.spec_rules import run_structural


BASE_SPEC = {
    "spec": {
        "constraints": [
            {
                "id": "email-format",
                "condition": "invalid email",
                "effect": "validity",
                "severity": "error",
            }
        ],
        "data": [
            {"id": "user-session", "source": "context"}
        ],
        "navigations": [
            {"id": "go-home", "target": "page.home", "method": "replace"}
        ],
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
                                        "maps-to": "data.user-session",
                                    }
                                ],
                                "provides": [
                                    {
                                        "id": "submit",
                                        "intent": "submit",
                                        "triggers": ["processing"],
                                        "may-lead-to": ["auth-outcome"],
                                    }
                                ],
                                "produces": [
                                    {"id": "processing"},
                                    {"id": "authenticated"},
                                ],
                                "communicates": [
                                    {"id": "auth-error", "kind": "error-message"}
                                ],
                                "explains": [
                                    {
                                        "id": "auth-outcome",
                                        "intent": "determine result",
                                        "evaluates": ["authenticated"],
                                        "branches": [
                                            {
                                                "condition": "authenticated is active",
                                                "resolves-to": "navigation.go-home",
                                            }
                                        ],
                                        "default-branch": {"resolves-to": "state.processing"},
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }
}


def broken(mutator):
    spec = copy.deepcopy(BASE_SPEC)
    mutator(spec)
    return run_structural(spec)


class SpecRuleTests(unittest.TestCase):
    def assert_rule_failed(self, report, rule_id: str) -> None:
        self.assertIn(rule_id, {r.rule_id for r in report.failures})

    def test_base_spec_passes_without_errors(self) -> None:
        self.assertTrue(run_structural(BASE_SPEC).passed)

    def test_required_properties_fail(self) -> None:
        report = broken(lambda spec: spec["spec"]["pages"][0]["sections"][0]["capabilities"][0].pop("intent"))

        self.assert_rule_failed(report, "RP-002")

    def test_capability_contains_is_forbidden(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["contains"] = []

        self.assert_rule_failed(broken(mutate), "FR-002")

    def test_action_handler_is_forbidden(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["provides"][0]["handler"] = "submitLogin"

        self.assert_rule_failed(broken(mutate), "FR-009")

    def test_page_cannot_directly_contain_capability(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["capabilities"] = [{"id": "bad", "intent": "bad"}]

        self.assert_rule_failed(broken(mutate), "FR-001")

    def test_constraint_cannot_resolve(self) -> None:
        def mutate(spec):
            spec["spec"]["constraints"][0]["resolves-to"] = "state.processing"

        report = broken(mutate)
        self.assert_rule_failed(report, "FR-005")
        self.assert_rule_failed(report, "FR-006")

    def test_state_cannot_communicate_feedback(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["produces"][0]["communicates"] = ["auth-error"]

        self.assert_rule_failed(broken(mutate), "FR-007")

    def test_navigation_source_cannot_be_external(self) -> None:
        report = broken(lambda spec: spec["spec"]["navigations"][0].update({"source": "external"}))

        self.assert_rule_failed(report, "FR-008")

    def test_internal_navigation_target_cannot_be_route(self) -> None:
        report = broken(lambda spec: spec["spec"]["navigations"][0].update({"target": "/home"}))

        self.assert_rule_failed(report, "FR-010")
        self.assert_rule_failed(report, "SI-004")

    def test_navigation_target_must_be_single_string(self) -> None:
        report = broken(lambda spec: spec["spec"]["navigations"][0].update({"target": ["page.home"]}))

        self.assert_rule_failed(report, "CA-002")

    def test_input_maps_to_must_be_single_string(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["requires"][0]["maps-to"] = ["data.user-session"]

        self.assert_rule_failed(broken(mutate), "CA-004")

    def test_unresolved_reference_fails(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["provides"][0]["triggers"] = ["missing"]

        self.assert_rule_failed(broken(mutate), "RI-001")

    def test_typed_reference_must_match_target_type(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["explains"][0]["branches"][0]["resolves-to"] = "feedback.authenticated"

        self.assert_rule_failed(broken(mutate), "RI-004")

    def test_typed_reference_can_disambiguate_duplicate_ids(self) -> None:
        def mutate(spec):
            spec["spec"]["navigations"].append({"id": "submit", "target": "page.submit", "method": "push"})
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["provides"][0]["navigates-to"] = "navigation.submit"

        self.assertTrue(broken(mutate).passed)

    def test_capability_string_references_resolve(self) -> None:
        def mutate(spec):
            cap = spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]
            spec["spec"]["inputs"] = [{"id": "shared-email", "kind": "credential", "label": "Email"}]
            spec["spec"]["actions"] = [{"id": "shared-submit", "intent": "submit"}]
            spec["spec"]["states"] = [{"id": "shared-processing"}]
            spec["spec"]["feedbacks"] = [{"id": "shared-error", "kind": "error-message"}]
            spec["spec"]["decisions"] = [
                {
                    "id": "shared-outcome",
                    "intent": "determine shared result",
                    "branches": [{"resolves-to": "state.shared-processing"}],
                }
            ]
            cap["requires"] = ["input.shared-email"]
            cap["provides"] = ["action.shared-submit"]
            cap["produces"] = ["state.shared-processing"]
            cap["communicates"] = ["feedback.shared-error"]
            cap["explains"] = ["decision.shared-outcome"]
            cap["consumes"] = ["data.user-session"]
            cap["obeys"] = ["constraint.email-format"]

        report = broken(mutate)
        self.assertTrue(report.passed)

    def test_capability_string_reference_must_resolve(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["requires"] = ["input.missing"]

        self.assert_rule_failed(broken(mutate), "RI-001")

    def test_capability_string_reference_must_match_expected_type(self) -> None:
        def mutate(spec):
            spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["requires"] = ["action.submit"]

        self.assert_rule_failed(broken(mutate), "RI-004")

    def test_constraint_and_decision_rules_fail(self) -> None:
        def mutate(spec):
            spec["spec"]["constraints"][0]["effect"] = "navigation"
            spec["spec"]["constraints"][0]["severity"] = "fatal"
            decision = spec["spec"]["pages"][0]["sections"][0]["capabilities"][0]["explains"][0]
            decision["branches"] = []
            decision["default-branch"] = {"condition": "always", "resolves-to": "state.processing"}

        report = broken(mutate)
        for rule_id in ("CT-001", "CT-002", "CA-005", "DE-002"):
            self.assert_rule_failed(report, rule_id)


if __name__ == "__main__":
    unittest.main()
