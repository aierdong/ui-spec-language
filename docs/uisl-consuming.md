# UISL Consuming Guide

## Purpose

UISL YAML is the serialized form of a UI semantic graph. It is not a component tree, wireframe, route map, API contract, or renderer instruction.

This guide defines how downstream agents, renderers, validators, and reviewers should read a UISL spec before turning it into implementation work.

## Reading frame

> **Presence = semantic obligation. Absence = renderer freedom.**

If a concept, relationship, constraint, or decision appears in UISL, the consumer must preserve that semantic obligation in its downstream output.

If UISL omits a visual or implementation detail, the consumer may choose an appropriate target-platform realization without treating the omission as a spec defect.

Examples:

```yaml
requires:
  - id: email
    kind: credential
```

Read as: this capability requires an email credential input.

Do not read as: render a specific HTML `<input type="email">`.

```yaml
provides:
  - id: submit
    intent: submit
```

Read as: this capability provides a submit action.

Do not read as: render a specific Button component.

## Source order

When consuming a spec, use the repository facts in this order:

1. `overview.md` for phase goals and boundary decisions.
2. `ontology/*.md` for what each concept means.
3. `taxonomy/*.taxonomy.yaml` for category membership and inherited defaults.
4. `registry/README.md` and `registry/{capabilities,inputs,actions}/` for registered reusable vocabulary.
5. `relationships/relationship.matrix.yaml` for legal edges, direction, cardinality, and `canonical_property`.
6. `normal-forms/README.md` and `normal-forms/required-property-matrix.yaml` for canonical shapes and required properties.
7. `normal-forms/constraint.nf.yaml` for persistent rule semantics.
8. `normal-forms/decision.nf.yaml` for branch semantics.
9. `schema/canonical-schema.yaml` for YAML shape and reference rules.
10. `tests/README.md` and `tests/validator/run.py` for conformance validation.

If these sources conflict, report the conflict before producing an implementation plan or renderer mapping.

## Consumption workflow

### 1. Validate the serialized shape

Confirm that the YAML matches the canonical schema before interpreting it deeply.

Completion criteria:

- The root `spec` shape is present.
- Required fields match `normal-forms/required-property-matrix.yaml`.
- IDs are lowercase hyphen-separated.
- Typed references such as `constraint.*`, `data.*`, and `navigation.*` resolve to root definitions.
- No component, CSS, framework, handler, route-string, or API-call concept is treated as canonical UISL.

### 2. Reconstruct the semantic graph

Read nested YAML as graph edges, not as renderer nesting.

Canonical structural path:

```text
Page
  -> sections[]
  -> Section
  -> contains[]
  -> Capability
```

Capability relationships:

```text
Capability
  -> requires[]      Input
  -> provides[]      Action
  -> produces[]      State
  -> communicates[]  Feedback
  -> consumes[]      DataRef
  -> obeys[]         ConstraintRef
  -> explains[]      Decision
```

Completion criteria:

- Every Page, Section, Capability, Input, Action, State, Feedback, Decision, Constraint, Data, and Navigation is represented as a semantic node.
- Every YAML relationship key is represented as a semantic edge.
- The consumer does not infer widgets from nesting depth.

### 3. Resolve vocabulary

Use registry entries as canonical meaning anchors.

Completion criteria:

- Registered Capability/Input/Action ids are recognized as registry vocabulary.
- Aliases are used only for normalization while reading external requirements or non-canonical drafts.
- Unknown vocabulary is reported as a vocabulary gap, not silently treated as stable vocabulary.
- Taxonomy and ontology are consulted before proposing a local interpretation for a gap.

### 4. Check relationships

Validate every emitted or consumed edge against `relationships/relationship.matrix.yaml`.

Completion criteria:

- Relationship direction is canonical.
- Relationship property names match the matrix `canonical_property`.
- Inverse/read-only relationships are not emitted downstream as canonical spec fields.
- Page does not directly contain Capability.
- Capability does not use `contains` for Input, Action, State, Feedback, Data, Constraint, or Decision.

### 5. Interpret Constraints

Constraints are persistent rules. They remain true while their condition holds.

Use them to derive availability, visibility, validity, guarded access, and other stable semantic obligations.

Examples:

| UISL pattern | Consumer obligation |
|---|---|
| `effect: validity` | Preserve validation semantics. |
| `effect: availability` | Preserve enabled/disabled availability semantics. |
| `effect: visibility` | Preserve shown/hidden or access semantics. |
| Page `guarded-by` | Preserve page access rule. |
| Input `validation` | Preserve input validity rule. |
| `obeys` | Preserve governing rule on the target concept. |

Do not convert a Constraint into an event handler. Do not replace the declarative condition with target-platform code in the semantic interpretation.

### 6. Interpret Decisions

Decisions are one-time branch points at a trigger.

Use them to derive conditional flow, outcome routing, confirmation branching, and post-action or post-state choices.

A Decision chooses among `resolves-to` targets. It is not the movement itself.

Examples:

| UISL pattern | Consumer obligation |
|---|---|
| `branches[].condition` | Preserve the branch condition semantics. |
| `branches[].resolves-to: navigation.*` | Preserve the chosen movement target. |
| `branches[].resolves-to: state.*` | Preserve the chosen state outcome. |
| `branches[].resolves-to: feedback.*` | Preserve the chosen communication outcome. |
| `default-branch` | Preserve fallback behavior. |

Do not model persistent validation or visibility rules as Decisions.

### 7. Produce the downstream contract

After interpreting the graph, produce the contract needed by the downstream task.

For explanation, output:

- Pages and their purpose.
- Sections and the semantic grouping they create.
- Capabilities and user-achievable outcomes.
- Inputs, Actions, States, Feedback, Data, Constraints, Decisions, and Navigation.
- Vocabulary gaps and validation concerns.

For implementation planning, output:

- Semantic obligations that must be preserved.
- Renderer freedoms left unspecified by UISL.
- Constraint and Decision behavior that implementation must support.
- Data and Navigation references that require integration decisions.
- Explicit non-requirements: visuals, component choices, CSS layout, and framework internals not specified by UISL.

For renderer mapping, output:

- Target-platform mapping notes for each semantic concept.
- Which mappings are required by UISL semantics.
- Which mappings are renderer choices.
- Any semantic obligations the target platform cannot represent directly.

For validation or review, output:

- Structural schema defects.
- Relationship defects.
- Vocabulary gaps or alias leakage.
- Constraint/Decision misclassifications.
- Conformance command results when available.

## What not to infer

UISL does not imply these unless explicit semantic concepts say so:

- Specific components or widgets.
- CSS layout, spacing, sizing, visual hierarchy, or breakpoints.
- Framework choice or framework APIs.
- DOM structure.
- Event handler names.
- Route strings.
- API endpoints, HTTP methods, database tables, or storage mechanisms.
- Copy beyond labels/messages already present.
- Authentication, authorization, persistence, or data fetching beyond declared Capability, Constraint, Data, Navigation, and Decision semantics.

## Implementation boundary

A UISL consumer may turn semantic obligations into target-platform implementation choices, but it must keep the distinction visible:

| Layer | Owned by UISL | Owned by renderer/implementation |
|---|---|---|
| Meaning | Capability, Input, Action, State, Feedback, Constraint, Decision | Naming of functions, components, files |
| Structure | Page -> Section -> Capability semantic graph | Component tree and layout containers |
| Flow | Navigation refs and Decision outcomes | Router library calls |
| Rules | Constraint conditions and effects | Validation library syntax |
| Data semantics | Data ids, source kind, scope, mutability | API endpoint, cache, store, transport |
| Presentation | Semantic labels/messages where present | Typography, spacing, colors, responsive design |

When writing code from UISL, first state the semantic contract, then choose an implementation mapping.

## Validation commands

Run from the UISL repository root when the validator exists:

```bash
python3 tests/validator/run.py
python3 tests/validator/run.py login --candidate <candidate-spec-path>
python3 tests/validator/run.py --candidate-dir <candidate-dir>
```

Use validation to check candidate specs, not to prove a renderer implementation is correct. Renderer tests should separately verify that the implementation preserves the consumed semantic obligations.

## Consumer checklist

Before presenting an interpretation, implementation plan, renderer mapping, or review:

- The spec was read as a semantic graph, not a component tree.
- Registered vocabulary was resolved through the registry.
- Unknown vocabulary was reported as a gap.
- Relationships were checked against the matrix.
- Constraints were treated as persistent rules.
- Decisions were treated as branch points.
- Root references for Constraint, Data, and Navigation were resolved.
- Implementation choices were separated from UISL obligations.
- No component, CSS, framework, DOM, handler, route-string, or API-call detail was attributed to UISL unless represented by a semantic concept.
- Relevant conformance validation was run or explicitly skipped with a reason.
