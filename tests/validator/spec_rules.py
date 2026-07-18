"""Phase 4 structural rules — a focused subset sufficient for Phase 6 conformance.

We do NOT reimplement the full schema-rules.yaml engine. We implement enough
to catch the regressions that matter for conformance tests: required fields,
forbidden alias usage, reference integrity, forbidden capability containment,
semantic naming (no component/CSS words). The heavy lifting stays with Phase 4.
"""

from __future__ import annotations

import re

from .report import RuleResult, ScenarioReport
from .spec_index import SpecIndex, index_spec

# Required fields per concept type (from required-property-matrix.yaml / schema-rules RP-*).
REQUIRED_FIELDS: dict[str, list[str]] = {
    "page": ["id", "label"],
    "section": ["id"],
    "capability": ["id", "intent"],
    "input": ["id", "kind", "label"],
    "action": ["id", "intent"],
    "state": ["id"],
    "feedback": ["id", "kind"],
    "decision": ["id", "intent"],
    "navigation": ["id", "target"],
    "data": ["id", "source"],
    "constraint": ["id", "condition"],
}

# Words banned from ids/labels (SI-001: component names; SI-002: CSS tokens).
# Matched as whole, case-sensitive tokens — "Form" (component) is banned,
# but "credential-form" (semantic compound) is fine. CSS words are lowercase.
COMPONENT_WORDS = {
    "Button", "Modal", "Card", "Checkbox", "Radio", "Drawer", "Popover",
    "TextField", "TextArea", "Dropdown", "Navbar", "Sidebar",
}
CSS_WORDS = {"width", "height", "margin", "padding", "position", "background", "border", "font"}
FRAMEWORK_TOKENS = ("react", "flutter", "vue", "html", "dom", "css", "tailwind", "widget", "jsx", "tsx")

VALID_EFFECTS = {"visibility", "availability", "validity"}
VALID_SEVERITIES = {"error", "warning", "info", "success"}
VALID_INTENTS = {
    "submit", "cancel", "delete", "create", "edit", "dismiss", "navigate",
    "download", "search", "sort", "filter", "sign-out", "clone", "expand",
    "copy", "run", "toggle-theme",
}

# canonical reference prefixes → expected concept type for the target.
REF_PREFIX_TO_TYPE = {
    "page.": "page",
    "section.": "section",
    "capability.": "capability",
    "navigation.": "navigation",
    "data.": "data",
    "constraint.": "constraint",
    "input.": "input",
    "action.": "action",
    "state.": "state",
    "feedback.": "feedback",
    "decision.": "decision",
}


def run_structural(spec: dict) -> ScenarioReport:
    idx = index_spec(spec)
    rep = ScenarioReport(scenario="structural")

    _required_properties(idx, rep)
    _forbidden_page_contains_capability(idx, rep)
    _forbidden_capability_contains(idx, rep)
    _forbidden_constraint_resolves(idx, rep)
    _forbidden_state_communicates(idx, rep)
    _forbidden_navigation_source(idx, rep)
    _forbidden_navigation_route_target(idx, rep)
    _forbidden_forbidden_keywords_in_actions(idx, rep)
    _reference_integrity(idx, rep)
    _semantic_naming(idx, rep)
    _constraint_props(idx, rep)
    _decision_rules(idx, rep)
    _cardinality(idx, rep)
    _intent_vocabulary(idx, rep)

    return rep


def _required_properties(idx: SpecIndex, rep: ScenarioReport) -> None:
    rp_map = {"page": "RP-001", "capability": "RP-002", "section": "RP-003",
              "input": "RP-004", "action": "RP-005", "state": "RP-006",
              "feedback": "RP-007", "decision": "RP-008", "navigation": "RP-009",
              "data": "RP-010", "constraint": "RP-011"}
    for c in idx.concepts:
        rule_id = rp_map.get(c.type)
        if not rule_id:
            continue
        missing = [f for f in REQUIRED_FIELDS[c.type] if not c.node.get(f)]
        desc = f"{c.type} must have={REQUIRED_FIELDS[c.type]}"
        rep.add(RuleResult(
            rule_id=rule_id, group="required-properties", severity="error",
            description=desc,
            passed=not missing,
            detail=f"id={c.node.get('id')!r} missing={missing}" if missing else "",
        ))


def _forbidden_page_contains_capability(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("page"):
        direct = c.node.get("capabilities")
        rep.add(RuleResult(
            rule_id="FR-001", group="forbidden-relationships", severity="error",
            description="Page must not directly contain Capability (use sections[].capabilities[])",
            passed=direct is None,
            detail=f"id={c.node.get('id')!r}" if direct is not None else "",
        ))


def _forbidden_capability_contains(idx: SpecIndex, rep: ScenarioReport) -> None:
    # FR-002/003/004: capability must use requires/provides/communicates, not 'contains'.
    for c in idx.of_type("capability"):
        for bk in c.node.keys():
            if bk == "contains":
                rep.add(RuleResult(
                    rule_id="FR-002", group="forbidden-relationships", severity="error",
                    description="Capability must not use 'contains' (use requires/provides/communicates)",
                    passed=False, detail=f"id={c.node.get('id')!r}",
                ))


def _forbidden_constraint_resolves(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("constraint"):
        target = c.node.get("resolves-to")
        present = "resolves-to" in c.node
        rep.add(RuleResult(
            rule_id="FR-005", group="forbidden-relationships", severity="error",
            description="Constraint must not resolve to Navigation",
            passed=not present,
            detail=f"id={c.node.get('id')!r} resolves-to={target!r}" if present else "",
        ))
        forbidden_target = isinstance(target, str) and target.startswith(("state.", "action.", "feedback."))
        rep.add(RuleResult(
            rule_id="FR-006", group="forbidden-relationships", severity="error",
            description="Constraint must not resolve to State, Action, or Feedback",
            passed=not forbidden_target,
            detail=f"id={c.node.get('id')!r} resolves-to={target!r}" if forbidden_target else "",
        ))


def _forbidden_state_communicates(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("state"):
        present = "communicates" in c.node
        rep.add(RuleResult(
            rule_id="FR-007", group="forbidden-relationships", severity="error",
            description="State must not use 'communicates' to reference Feedback (use may-trigger)",
            passed=not present,
            detail=f"id={c.node.get('id')!r}" if present else "",
        ))


def _forbidden_navigation_source(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("navigation"):
        source = c.node.get("source")
        rep.add(RuleResult(
            rule_id="FR-008", group="forbidden-relationships", severity="error",
            description="Navigation.source must not be external",
            passed=source != "external",
            detail=f"id={c.node.get('id')!r} source={source!r}" if source == "external" else "",
        ))


def _forbidden_navigation_route_target(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("navigation"):
        target = c.node.get("target")
        method = c.node.get("method")
        if not isinstance(target, str):
            continue
        external = method == "external" or target.startswith("http://") or target.startswith("https://")
        route_like = target.startswith("/") or ":" in target
        canonical_internal = target.startswith(("page.", "section.", "capability."))
        ok = external or (canonical_internal and not route_like)
        rep.add(RuleResult(
            rule_id="FR-010", group="forbidden-relationships", severity="error",
            description="Internal Navigation.target must use page.*, section.*, or capability.*",
            passed=ok,
            detail=f"id={c.node.get('id')!r} target={target!r}" if not ok else "",
        ))
        rep.add(RuleResult(
            rule_id="SI-004", group="semantic", severity="error",
            description="Internal Navigation.target must not be a URL route string",
            passed=not route_like or external,
            detail=f"id={c.node.get('id')!r} target={target!r}" if route_like and not external else "",
        ))


def _forbidden_forbidden_keywords_in_actions(idx: SpecIndex, rep: ScenarioReport) -> None:
    # FR-009: no 'calls'/'handler'/'component' on Action.
    banned = ("calls", "handler", "component", "onClick")
    for c in idx.of_type("action"):
        present = [k for k in banned if k in c.node]
        rep.add(RuleResult(
            rule_id="FR-009", group="forbidden-relationships", severity="error",
            description="Action must not reference implementation concepts (calls/handler/component)",
            passed=not present,
            detail=f"id={c.node.get('id')!r} found={present}" if present else "",
        ))


def _reference_integrity(idx: SpecIndex, rep: ScenarioReport) -> None:
    known = idx.ids()
    id_to_scope = {c.node["id"]: c.scope_id for c in idx.concepts if c.node.get("id")}
    refs: list[tuple[str | None, str | None, str, str | None]] = []
    list_fields = {
        "page": {"guarded-by": "constraint", "navigation-in": "navigation", "navigation-out": "navigation"},
        "section": {"obeys": "constraint", "receives": "data"},
        "capability": {
            "requires": "input",
            "provides": "action",
            "produces": "state",
            "communicates": "feedback",
            "explains": "decision",
            "consumes": "data",
            "obeys": "constraint",
        },
        "input": {"validation": "constraint"},
        "action": {
            "triggers": "state",
            "produces": "feedback",
            "obeys": "constraint",
            "may-lead-to": "decision",
        },
        "state": {
            "may-trigger": "feedback",
            "may-lead-to": "decision",
            "may-lead-to-nav": "navigation",
            "obeys": "constraint",
        },
        "feedback": {"may-lead-to": "decision"},
        "decision": {"evaluates": "state"},
        "navigation": {"carry-state": "state", "carry-data": "data"},
        "data": {"maps-to": "input", "feeds": "section"},
    }
    scalar_fields = {
        "input": {"maps-to": "data", "source": "data"},
        "action": {"navigates-to": "navigation", "target": None},
        "feedback": {"action": "action"},
    }
    for c in idx.concepts:
        cid = c.node.get("id")
        scope = c.scope_id
        for field, expected in list_fields.get(c.type, {}).items():
            refs += _ref_list(cid, scope, c.node.get(field), expected)
        for field, expected in scalar_fields.get(c.type, {}).items():
            refs += _ref_one(cid, scope, c.node.get(field), expected)
        if c.type == "decision":
            for br in c.node.get("branches", []) or []:
                if isinstance(br, dict):
                    refs += _ref_one(cid, scope, br.get("resolves-to"), None)
            db = c.node.get("default-branch")
            if isinstance(db, dict):
                refs += _ref_one(cid, scope, db.get("resolves-to"), None)
        if c.type == "data":
            refs += _ref_list(cid, scope, c.node.get("affects"), None)
    seen = set()
    for src, src_scope, ref, expected in refs:
        key = (src, ref, expected)
        if key in seen:
            continue
        seen.add(key)
        ok, detail, sev, actual_rule = _resolve(ref, known, idx, id_to_scope, src_scope, expected)
        rep.add(RuleResult(
            rule_id=actual_rule, group="reference-integrity", severity=sev,
            description=f"reference {ref!r} (from {src!r}) must resolve",
            passed=ok, detail=detail if not ok else "",
        ))


def _ref_list(src, scope, val, expected):
    out = []
    if isinstance(val, list):
        for v in val:
            if isinstance(v, str):
                out.append((src, scope, v, expected))
    return out


def _ref_one(src, scope, val, expected):
    if isinstance(val, str):
        return [(src, scope, val, expected)]
    return []


_PREFIX_RULED = REF_PREFIX_TO_TYPE


def _find_target(idx: SpecIndex, ref_id: str, expected_type: str | None = None):
    if expected_type is not None:
        for c in idx.concepts:
            if c.node.get("id") == ref_id and c.type == expected_type:
                return c
        return None
    return idx.by_id.get(ref_id)


def _resolve(ref: str, known: set[str], idx: SpecIndex,
             id_to_scope: dict, src_scope: str | None,
             expected_type: str | None = None) -> tuple[bool, str, str, str]:
    """Return (ok, detail, severity, rule_id).

    severity is 'error' for unresolved refs, 'warning' for cross-scope
    bare-id refs that should use a typed prefix (RI-004-like).
    """
    # typed refs ("state.processing"):
    for prefix, prefix_expected in _PREFIX_RULED.items():
        if ref.startswith(prefix):
            tail = ref[len(prefix):]
            target = _find_target(idx, tail, prefix_expected)
            if target is None:
                if tail in known:
                    first = idx.by_id[tail]
                    return False, f"typed ref {ref!r} expects {prefix_expected} but target is {first.type}", "error", "RI-004"
                return False, f"unresolved typed ref {ref!r} (no {prefix_expected} id {tail!r})", "error", "RI-001"
            if expected_type is not None and prefix_expected != expected_type:
                return False, f"ref {ref!r} must target {expected_type} but targets {prefix_expected}", "error", "RI-004"
            return True, "", "error", "RI-001"
    # bare id:
    if ref in known:
        tgt = _find_target(idx, ref, expected_type)
        if tgt is None:
            first = idx.by_id[ref]
            return False, f"ref {ref!r} must target {expected_type} but target is {first.type}", "error", "RI-004"
        target_scope = id_to_scope.get(ref)
        # cross-scope bare references to global concepts (navigation/data/constraint)
        # SHOULD use typed prefix — warning, not error (canonical spec mixes both).
        if tgt.type in ("navigation", "data", "constraint"):
            return (False, f"ref {ref!r} to {tgt.type} should use typed prefix "
                    f"({tgt.type}.{ref}) for RI-004", "warning", "RI-004")
        if target_scope is not None and src_scope is not None and target_scope != src_scope:
            return (False, f"cross-scope ref {ref!r} to {tgt.type}"
                    f" should use typed prefix for RI-004", "warning", "RI-004")
        return True, "", "error", "RI-001"
    return False, f"unresolved id {ref!r}", "error", "RI-001"


def _semantic_naming(idx: SpecIndex, rep: ScenarioReport) -> None:
    # SI-001: no component names as whole tokens in ids/labels (case-sensitive).
    comp_pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in COMPONENT_WORDS) + r")\b")
    # SI-002: no CSS words (lowercase whole token) in ids/labels.
    css_pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in CSS_WORDS) + r")\b")
    for c in idx.concepts:
        for field in ("id", "label", "intent"):
            val = c.node.get(field)
            if not isinstance(val, str):
                continue
            m = comp_pat.search(val)
            if m:
                rep.add(RuleResult(
                    rule_id="SI-001", group="semantic", severity="error",
                    description=f"{c.type}.{field} must not contain component word",
                    passed=False, detail=f"id={c.node.get('id')!r} {field}={val!r} hit={m.group(1)!r}",
                ))
            m2 = css_pat.search(val)
            if m2:
                rep.add(RuleResult(
                    rule_id="SI-002", group="semantic", severity="error",
                    description=f"{c.type}.{field} must not contain CSS word",
                    passed=False, detail=f"id={c.node.get('id')!r} {field}={val!r} hit={m2.group(1)!r}",
                ))
            low = val.lower()
            hits = [tok for tok in FRAMEWORK_TOKENS if tok in low]
            if hits:
                rep.add(RuleResult(
                    rule_id="SI-003", group="semantic", severity="error",
                    description=f"{c.type}.{field} must not contain framework token",
                    passed=False, detail=f"id={c.node.get('id')!r} hit={hits}",
                ))


def _constraint_props(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("constraint"):
        eff = c.node.get("effect")
        rep.add(RuleResult(
            rule_id="CT-001", group="constraint-rules", severity="error",
            description="constraint.effect must be visibility|availability|validity",
            passed=eff is None or eff in VALID_EFFECTS,
            detail=f"id={c.node.get('id')!r} effect={eff!r}" if eff is not None and eff not in VALID_EFFECTS else "",
        ))
        sev = c.node.get("severity")
        rep.add(RuleResult(
            rule_id="CT-002", group="constraint-rules", severity="error",
            description="constraint.severity must be error|warning|info|success",
            passed=sev is None or sev in VALID_SEVERITIES,
            detail=f"id={c.node.get('id')!r} severity={sev!r}" if sev is not None and sev not in VALID_SEVERITIES else "",
        ))


def _decision_rules(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("decision"):
        branches = c.node.get("branches")
        rep.add(RuleResult(
            rule_id="CA-005", group="cardinality", severity="error",
            description="decision.branches must be non-empty",
            passed=bool(branches),
            detail=f"id={c.node.get('id')!r}" if not branches else "",
        ))
        db = c.node.get("default-branch")
        if isinstance(db, dict) and "condition" in db:
            rep.add(RuleResult(
                rule_id="DE-002", group="decision-rules", severity="error",
                description="default-branch must not have a 'condition' property",
                passed=False, detail=f"id={c.node.get('id')!r}",
            ))


def _cardinality(idx: SpecIndex, rep: ScenarioReport) -> None:
    # CA-001: page should have at least one section (warning).
    for c in idx.of_type("page"):
        sections = c.node.get("sections", []) or []
        rep.add(RuleResult(
            rule_id="CA-001", group="cardinality", severity="warning",
            description="page should have at least one section",
            passed=bool(sections),
            detail=f"id={c.node.get('id')!r}" if not sections else "",
        ))
    for c in idx.of_type("navigation"):
        target = c.node.get("target")
        rep.add(RuleResult(
            rule_id="CA-002", group="cardinality", severity="error",
            description="navigation.target must be a single string",
            passed=isinstance(target, str) and bool(target),
            detail=f"id={c.node.get('id')!r} target={target!r}" if not isinstance(target, str) or not target else "",
        ))
    for c in idx.of_type("input"):
        maps_to = c.node.get("maps-to")
        rep.add(RuleResult(
            rule_id="CA-004", group="cardinality", severity="error",
            description="input.maps-to must be a single string when present",
            passed=maps_to is None or isinstance(maps_to, str),
            detail=f"id={c.node.get('id')!r} maps-to={maps_to!r}" if maps_to is not None and not isinstance(maps_to, str) else "",
        ))


def _intent_vocabulary(idx: SpecIndex, rep: ScenarioReport) -> None:
    for c in idx.of_type("action"):
        it = c.node.get("intent")
        rep.add(RuleResult(
            rule_id="SI-005", group="semantic", severity="warning",
            description="action.intent must be a canonical intent value",
            passed=it in VALID_INTENTS,
            detail=f"id={c.node.get('id')!r} intent={it!r}" if it not in VALID_INTENTS else "",
        ))
