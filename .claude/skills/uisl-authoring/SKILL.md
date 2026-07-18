---
name: uisl-authoring
description: Guide agents to author, review, normalize, or validate UISL/UI Ontology specs using Vocabulary, Relationship, Constraint, and Decision semantics. Use when users ask to write or assess UISL, UI Spec, UI Ontology, canonical spec YAML, registry vocabulary, relationship validity, constraints, decisions, or conformance scenarios.
argument-hint: "[requirement, spec path, or review goal]"
allowed-tools: Read, Bash
---

# UISL Authoring Skill

Use this skill to turn UI/UX requirements into UISL semantic specs, or to review an existing UISL spec. Do not treat UISL as a component DSL. YAML is only the final serialization format.

## Non-negotiable principles

1. Everything is semantic: describe meaning, not CSS or widgets.
2. Everything is platform independent: never emit React, Flutter, HTML, DOM, or component-library concepts.
3. Describe intent, not implementation: use `intent`, capabilities, states, constraints, and decisions rather than handlers or UI controls.
4. Vocabulary first: prefer registered vocabulary before inventing a new concept.
5. One concept has one definition: aliases are read-side normalization hints only; never emit aliases.

Forbidden output vocabulary includes component and implementation terms such as `Button`, `Checkbox`, `Radio`, `Drawer`, `Popover`, `Card`, `Modal`, `div`, `onClick`, `handler`, `className`, `width`, `margin`, `flex`, `grid`, `CSS`, `React`, and `HTML`.

## Fact source order

When authoring or reviewing, use the repository facts in this order:

1. `overview.md` for phase goals and boundary decisions.
2. `ontology/*.md` for what each concept means.
3. `registry/README.md` and `registry/{capabilities,inputs,actions}/` for reusable vocabulary entries.
4. `relationships/relationship.matrix.yaml` for legal relationships, direction, cardinality, and `canonical_property`.
5. `normal-forms/README.md` and `normal-forms/required-property-matrix.yaml` for canonical shapes and required properties.
6. `normal-forms/constraint.nf.yaml` and `normal-forms/decision.nf.yaml` when translating rules and branching.
7. `schema/canonical-schema.yaml` for final YAML shape.
8. `tests/README.md` and `tests/validator/run.py` for conformance validation.

If sources appear to conflict, stop and resolve the conflict in the source documents before relying on the skill output.

## Authoring workflow

1. Extract the user's goal as one or more Pages.
2. Partition each Page into semantic Sections.
3. Identify Capabilities as user-achievable outcomes.
4. For each Capability, look for matching registry entries first.
   - If a match exists, reuse the registered `id`, `intent`, aliases only for recognition, and recommended wiring when appropriate.
   - If no match exists, consult taxonomy and ontology, then mark the result as a vocabulary gap instead of silently inventing a stable registry term.
5. Connect concepts only through relationships allowed by `relationships/relationship.matrix.yaml`.
6. Extract Constraints for persistent rules.
7. Extract Decisions for triggered branch points.
8. Serialize only after the semantic graph is clear.
9. Run the output checklist and, when a scenario exists, run the conformance validator.

## Canonical relationship policy

Agents may emit only canonical properties from the relationship matrix and canonical schema.

Core structural flow:

```yaml
Page.sections[] -> Section
Section.contains[] -> Capability
Capability.requires[] -> Input
Capability.provides[] -> Action
Capability.produces[] -> State
Capability.communicates[] -> Feedback
Capability.consumes[] -> DataRef
Capability.obeys[] -> ConstraintRef
Capability.explains[] -> Decision
```

Important boundaries:

- Page must not directly contain Capability.
- Section groups Capabilities; it does not perform them.
- Capability must not use `contains` for Inputs, Actions, States, Feedback, or Decisions.
- Action may use `may-lead-to` for Decision and `navigates-to` for Navigation.
- Capability uses `explains` for owned Decisions; do not use `may-lead-to` there.
- Constraint, Data, and Navigation are root definitions referenced with typed refs such as `constraint.*`, `data.*`, and `navigation.*`.

## Constraint policy

Use Constraint for persistent rules that remain true while their condition holds.

Canonical examples:

- Required, min/max, pattern, and validation rules -> Constraint with `effect: validity`.
- Disabled/enabled conditions -> Constraint with `effect: availability`.
- Visible/hidden, role access, and guarded access -> Constraint with `effect: visibility`.
- Page access rules -> Page `guarded-by` ConstraintRef.
- Section/Capability/Action rules -> `obeys` ConstraintRef.
- Input validation -> Input `validation` ConstraintRef.

Never emit implementation expressions. Use declarative condition syntax from `normal-forms/constraint.nf.yaml`, such as `input.email is empty`, `data.items is empty`, `value does not match email-pattern`, or `State: Lifecycle.Processing is active`.

## Decision policy

Use Decision for one-time branching at a trigger point.

Canonical examples:

- `if/else`, `switch/case`, outcome routing, confirmation prompts, and post-action branching -> Decision.
- A Decision has `id`, `intent`, `branches`, optional `trigger`, optional `evaluates`, and optional `default-branch`.
- Branches use declarative `condition` and `resolves-to` references.
- Valid `resolves-to` targets are Navigation, State, Action, or Feedback.

Do not model a persistent rule as a Decision. Do not model movement itself as a Decision; Navigation is the movement, Decision chooses which movement or outcome applies.

## Output checklist

Before presenting or accepting a UISL spec:

- All concept ids are lowercase hyphen-separated.
- Required fields match `normal-forms/required-property-matrix.yaml`.
- Registered vocabulary is reused where available.
- Unknown vocabulary is called out as a vocabulary gap.
- Relationship keys match `relationships/relationship.matrix.yaml` and `schema/canonical-schema.yaml`.
- Section uses `contains` for Capabilities.
- Capability uses `requires`, `provides`, `produces`, `communicates`, `consumes`, `obeys`, and `explains` as appropriate.
- Constraint/Data/Navigation are root definitions when shared or cross-cutting.
- No aliases are emitted.
- No component, CSS, framework, route-string, handler, or API-call concepts appear.
- Candidate specs pass the relevant conformance command when a scenario exists.

## Verification commands

From the repository root:

```bash
python3 tests/validator/run.py
python3 tests/validator/run.py login --candidate <candidate-spec-path>
python3 tests/validator/run.py --candidate-dir <candidate-dir>
```

Use the first command to confirm canonical fixtures still pass. Use the candidate commands to validate Agent-generated specs against Phase 6 scenarios.
