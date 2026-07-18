"""Phase 6 semantic assertions — must-contain / must-not-contain.

Each expectations/*.expect.yaml:
    scenario: login
    must-contain:
      - capability.id == authentication
      - input.kind == credential
      - action.intent == submit
      - state.id in [processing, authenticated, auth-failed]
    must-not-contain:
      - concept.label == "Shopping Cart"
      - any.id contains "cart"

The matcher goes through every Concept in the spec and tries to satisfy each
assertion. must-contain passes if at least one concept matches; must-not-contain
passes if NO concept matches.
"""

from __future__ import annotations

import re

from .report import RuleResult, ScenarioReport
from .spec_index import index_spec

# assertion grammar we support (kept tiny — feel free to extend)
# forms:
#   <type>.<field> == <value>            # exact match
#   <type>.<field> == <value> (case-insensitive)
#   <type>.<field> in [<v1>, <v2>, ...]
#   <type>.<field> contains <substring>
#   any.<field> contains <substring>      # any concept type
#   any.id contains <regex>
_EQ = re.compile(r"^\s*(?P<type>[\w-]+)\.(?P<field>[\w-]+)\s+(?P<op>==|in|contains)\s+(?P<rest>.+?)\s*(?:\((?P<flag>case-insensitive)\))?\s*$")


def run_assertions(spec: dict, expectations: dict, scenario: str) -> ScenarioReport:
    idx = index_spec(spec)
    rep = ScenarioReport(scenario=scenario)

    for must in expectations.get("must-contain", []) or []:
        _check_must(idx, must, rep, positive=True)
    for must_not in expectations.get("must-not-contain", []) or []:
        _check_must(idx, must_not, rep, positive=False)

    return rep


def _check_must(idx, raw: str, rep: ScenarioReport, positive: bool) -> None:
    m = _EQ.match(raw)
    if not m:
        rep.add(RuleResult(
            rule_id="CT-ASSERT-PARSE", group="assertions", severity="error",
            description=f"could not parse assertion: {raw!r}",
            passed=False,
        ))
        return
    ctype, field, op, rest, flag = (m.group("type"), m.group("field"),
                                    m.group("op"), m.group("rest"), m.group("flag"))
    ci = flag == "case-insensitive"
    candidates = idx.concepts if ctype == "any" else idx.of_type(ctype)
    matched = False
    for c in candidates:
        val = c.node.get(field)
        if val is None:
            continue
        if _match(val, op, rest, ci):
            matched = True
            break

    if positive:
        rule_id = "MUST-CONTAIN"
        desc = f"must contain concept matching: {raw}"
        passed = matched
        detail = "" if matched else f"no {ctype} concept matched"
    else:
        rule_id = "MUST-NOT-CONTAIN"
        desc = f"must NOT contain any concept matching: {raw}"
        passed = not matched
        detail = "" if passed else f"a concept matched the forbidden pattern"

    rep.add(RuleResult(
        rule_id=rule_id, group="assertions",
        severity="error" if positive else "error",
        description=desc, passed=passed, detail=detail,
    ))


def _match(val, op: str, rest: str, ci: bool) -> bool:
    if op == "==":
        expected = _parse_scalar(rest)
        # list field: == means "list contains scalar" (membership)
        if isinstance(val, list):
            if ci:
                return (str(expected).lower() in [str(x).lower() for x in val]
                        or str(_quote_strip(rest)).lower() in [str(x).lower() for x in val])
            return expected in val or str(_quote_strip(rest)) in val
        if ci:
            return str(val).lower() == str(expected).lower()
        return val == expected or str(val) == str(_quote_strip(rest))
    if op == "in":
        items = _parse_list(rest)
        if ci:
            vals = [str(x).lower() for x in items]
            return str(val).lower() in vals
        return val in items or str(val) in [str(x) for x in items]
    if op == "contains":
        # list field: contains = membership; string field: contains = substring
        if isinstance(val, list):
            needle = _parse_scalar(rest)
            if ci:
                return (str(needle).lower() in [str(x).lower() for x in val]
                        or str(_quote_strip(rest)).lower() in [str(x).lower() for x in val])
            return needle in val or str(_quote_strip(rest)) in val
        needle = _parse_scalar(rest)
        if ci:
            return str(needle).lower() in str(val).lower()
        return str(needle) in str(val)
    return False


def _parse_scalar(rest: str):
    s = rest.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def _parse_list(rest: str):
    s = rest.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    items = []
    for part in _split_top_commas(s):
        part = part.strip()
        if (part.startswith('"') and part.endswith('"')) or (part.startswith("'") and part.endswith("'")):
            items.append(part[1:-1])
        else:
            items.append(part)
    return items


def _split_top_commas(s: str):
    out = []
    buf = ""
    depth = 0
    for ch in s:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(buf)
            buf = ""
            continue
        buf += ch
    if buf.strip():
        out.append(buf)
    return out


def _quote_strip(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s
