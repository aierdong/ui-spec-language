"""Walk a UISL spec and collect every concept node with its parent context.

Phase 6 needs concept-level lookups ("does this spec contain an Action with
intent=submit?", "does it contain a Capability whose id is authenticate?") plus
the ability to detect forbidden alias usage. This module turns the nested YAML
into a flat list of concept dicts tagged with type.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Key on a Capability that, if present, violates forbidden-relationship
# FR-002/003/004 (capability must not contain input/action/feedback).
CAPABILITY_CONTAINS_KEYS = ("contains",)

# canonical key mapping per concept — used to traverse the nested tree.
SECTION_CHILDREN_KEY = "sections"
CAPABILITY_REQUIRES_KEY = "requires"
CAPABILITY_PROVIDES_KEY = "provides"
CAPABILITY_PRODUCES_KEY = "produces"
CAPABILITY_COMMUNICATES_KEY = "communicates"
CAPABILITY_EXPLAINS_KEY = "explains"


@dataclass
class Concept:
    """A single concept instance lifted out of the nested spec tree."""

    type: str            # page | section | capability | input | action | state | ...
    node: dict           # the raw dict for this concept
    parent: str | None   # parent concept id (or None for top-level concepts)
    parent_type: str | None
    scope_id: str | None  # id of the owning page/capability, for inline-scope rules


@dataclass
class SpecIndex:
    concepts: list[Concept] = field(default_factory=list)
    # id -> concept for top-level ids (constraints, navigations, data, pages and their children)
    by_id: dict[str, Concept] = field(default_factory=dict)

    def ids(self) -> set[str]:
        return set(self.by_id.keys())

    def of_type(self, t: str) -> list[Concept]:
        return [c for c in self.concepts if c.type == t]


def _is_list_of_dicts(v: Any) -> bool:
    return isinstance(v, list) and all(isinstance(x, dict) for x in v)


def _id(node: dict) -> str | None:
    return node.get("id")


def index_spec(spec: dict) -> SpecIndex:
    """Flatten the canonical spec tree into Concept records.

    Recognizes the canonical schema layout:
      spec.pages[].sections[].contains[]
        .requires[] (input)
        .provides[] (action)
        .produces[] (state)
        .communicates[] (feedback)
        .explains[] (decision)
      spec.constraints[] / spec.navigations[] / spec.data[]
    """
    idx = SpecIndex()
    root = spec.get("spec", spec)

    for page in root.get("pages", []) or []:
        pid = _id(page)
        _add(idx, "page", page, parent=None, parent_type=None, scope_id=pid)
        for section in page.get("sections", []) or []:
            sid = _id(section)
            _add(idx, "section", section, parent=pid, parent_type="page", scope_id=pid)
            _index_section(idx, section, pid)

    for concept_type, key in (
        ("constraint", "constraints"),
        ("navigation", "navigations"),
        ("data", "data"),
        ("input", "inputs"),
        ("action", "actions"),
        ("state", "states"),
        ("feedback", "feedbacks"),
        ("decision", "decisions"),
    ):
        for node in root.get(key, []) or []:
            _add(idx, concept_type, node, parent=None, parent_type=None, scope_id=_id(node))

    return idx


def _index_section(idx: SpecIndex, section: dict, page_id: str | None) -> None:
    sid = _id(section)
    for section2 in section.get("sections", []) or []:
        _add(idx, "section", section2, parent=sid, parent_type="section", scope_id=page_id)
        _index_section(idx, section2, page_id)
    for cap in section.get("contains", []) or []:
        cid = _id(cap)
        _add(idx, "capability", cap, parent=sid, parent_type="section", scope_id=cid)
        _walk_capability_children(idx, cap, cid)


def _walk_capability_children(idx: SpecIndex, cap: dict, cid: str | None) -> None:
    mapping = (
        ("input", CAPABILITY_REQUIRES_KEY),
        ("action", CAPABILITY_PROVIDES_KEY),
        ("state", CAPABILITY_PRODUCES_KEY),
        ("feedback", CAPABILITY_COMMUNICATES_KEY),
        ("decision", CAPABILITY_EXPLAINS_KEY),
    )
    for ctype, key in mapping:
        for child in cap.get(key, []) or []:
            if not isinstance(child, dict):
                continue
            _add(idx, ctype, child, parent=cid, parent_type="capability", scope_id=cid)


def _add(idx: SpecIndex, ctype: str, node: dict, parent, parent_type, scope_id) -> None:
    c = Concept(ctype, node, parent, parent_type, scope_id)
    idx.concepts.append(c)
    cid = _id(node)
    if cid:
        # later definitions overwrite earlier ones (duplicate-id detection done elsewhere)
        idx.by_id.setdefault(cid, c)
