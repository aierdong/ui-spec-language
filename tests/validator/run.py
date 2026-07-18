"""Run Phase 6 conformance tests.

Usage:
    python3 tests/validator/run.py
    python3 tests/validator/run.py login
    python3 tests/validator/run.py --candidate-dir agent-output
    python3 tests/validator/run.py login --candidate agent-output/login.spec.yaml

Exit code:
    0 = all scenarios PASS
    1 = at least one FAIL
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

# allow `from validator import ...` regardless of cwd
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from validator.spec_rules import run_structural  # noqa: E402
from validator.assertions import run_assertions  # noqa: E402
from validator.report import ScenarioReport  # noqa: E402

REPO_ROOT = HERE.parent.parent
SPECS_DIR = HERE.parent / "specs"
EXPECT_DIR = HERE.parent / "expectations"
REPORT_DIR = HERE.parent / "reports"


def _load_yaml(p: Path) -> dict:
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _scenarios() -> list[str]:
    return sorted(f.stem.replace(".spec", "") for f in SPECS_DIR.glob("*.spec.yaml"))


def _spec_path_for(name: str, candidate_dir: Path | None, candidate: Path | None) -> Path:
    if candidate is not None:
        return candidate
    if candidate_dir is not None:
        return candidate_dir / f"{name}.spec.yaml"
    return SPECS_DIR / f"{name}.spec.yaml"


def run_one(name: str, candidate_dir: Path | None = None, candidate: Path | None = None) -> ScenarioReport:
    spec_path = _spec_path_for(name, candidate_dir, candidate)
    expect_path = EXPECT_DIR / f"{name}.expect.yaml"
    if not spec_path.exists():
        print(f"[!] missing spec: {spec_path}", file=sys.stderr)
        sys.exit(2)
    if not expect_path.exists():
        print(f"[!] missing expectations: {expect_path}", file=sys.stderr)
        sys.exit(2)

    spec = _load_yaml(spec_path)
    expectations = _load_yaml(expect_path)

    # 1) structural rules (Phase 4 subset)
    structural = run_structural(spec)
    structural.scenario = f"{name}/structural"
    # 2) semantic assertions (Phase 6)
    semantic = run_assertions(spec, expectations, f"{name}/semantic")

    # Combined report
    combined = ScenarioReport(scenario=name)
    combined.results = structural.results + semantic.results
    return combined


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 6 conformance tests")
    parser.add_argument("scenarios", nargs="*", help="scenario names, defaults to all canonical scenarios")
    parser.add_argument("--candidate-dir", type=Path,
                        help="directory containing <scenario>.spec.yaml Agent outputs")
    parser.add_argument("--candidate", type=Path,
                        help="single Agent output spec; requires exactly one scenario")
    args = parser.parse_args(argv[1:])
    if args.candidate and args.candidate_dir:
        parser.error("--candidate and --candidate-dir are mutually exclusive")
    if args.candidate and len(args.scenarios) != 1:
        parser.error("--candidate requires exactly one scenario name")
    return args


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    names = args.scenarios or _scenarios()

    if not names:
        print("[!] no scenarios found under tests/specs/", file=sys.stderr)
        return 1

    REPORT_DIR.mkdir(exist_ok=True)
    overall_pass = True
    all_lines: list[str] = []
    summary: list[str] = ["", "==== SUMMARY ===="]

    for n in names:
        rep = run_one(n, candidate_dir=args.candidate_dir, candidate=args.candidate)
        all_lines.append(rep.render())
        status = "PASS" if rep.passed else "FAIL"
        summary.append(f"  {status}  {n} ({len(rep.failures)} err, {len(rep.warnings)} warn)")
        overall_pass = overall_pass and rep.passed

        # write per-scenario report file
        out = REPORT_DIR / f"{n}.report.txt"
        out.write_text(rep.render(), encoding="utf-8")

    print("\n".join(all_lines))
    print("\n".join(summary))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
