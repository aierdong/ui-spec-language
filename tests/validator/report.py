"""Report aggregation and pretty printing for the conformance validator."""

from dataclasses import dataclass, field


@dataclass
class RuleResult:
    rule_id: str
    group: str
    severity: str
    description: str
    passed: bool
    detail: str = ""

    def __str__(self) -> str:
        mark = "PASS" if self.passed else "FAIL"
        head = f"  [{mark}] {self.rule_id} ({self.group}, {self.severity})"
        if self.passed:
            return head
        tail = f"  -> {self.description}"
        if self.detail:
            tail += f"\n     detail: {self.detail}"
        return f"{head}\n{tail}"


@dataclass
class ScenarioReport:
    scenario: str
    results: list[RuleResult] = field(default_factory=list)

    def add(self, r: RuleResult) -> None:
        self.results.append(r)

    @property
    def passed(self) -> bool:
        return all(r.passed or r.severity != "error" for r in self.results)

    @property
    def failures(self) -> list[RuleResult]:
        return [r for r in self.results if not r.passed and r.severity == "error"]

    @property
    def warnings(self) -> list[RuleResult]:
        return [r for r in self.results if not r.passed and r.severity != "error"]

    def render(self) -> str:
        lines = [f"==== {self.scenario} ===="]
        for r in self.results:
            lines.append(str(r))
        n_fail = len(self.failures)
        n_warn = len(self.warnings)
        status = "PASS" if self.passed else "FAIL"
        lines.append(f"  -> {status} ({n_fail} error, {n_warn} warning)")
        return "\n".join(lines)
