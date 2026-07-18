# Normal Forms — Canonical Representation Rules

## Purpose

A Normal Form (NF) defines the one canonical representation for each semantic entity in UISL. Agents may read alternative expressions, but must emit only canonical forms.

Normal Forms eliminate Agent reasoning anomalies: the same semantic intent should not be expressible in multiple output shapes.

---

## Core Rules

### Rule 1: One Canonical Form per Semantic Entity

Every ontology concept has one `.nf.yaml` file and one canonical output shape. Equivalent input expressions are read-side only and must normalize to that shape.

### Rule 2: Required Properties Come From the Matrix

[`required-property-matrix.yaml`](required-property-matrix.yaml) is the single source of truth for required properties.

NF canonical forms mark every non-required field with `?` in the type/comment notation. Do **not** add `?` to the emitted property name.

| Concept | Required Properties |
|---------|---------------------|
| Capability | `id`, `intent` |
| Action | `id`, `intent` |
| Input | `id`, `kind`, `label` |
| Page | `id`, `label` |
| Section | `id` |
| State | `id` |
| Feedback | `id`, `kind` |
| Navigation | `id`, `target` |
| Constraint | `id`, `condition` |
| Decision | `id`, `intent`, `branches` |
| Data | `id`, `source` |

### Rule 3: Property Names Are Canonical

Aliases are documented for read-side normalization only. Agents must never emit aliases.

| Canonical Property | Aliases (never generate) |
|-------------------|--------------------------|
| `kind` | `type`, `role`, `category`, `input-type`, `field-type` |
| `id` | `name`, `key`, `ref`, `identifier` |
| `intent` | `goal`, `objective`, `aim`, `action-type`, `behavior`, `description`, `summary` |
| `purpose` | `role`, `function`, `page-purpose`, `goal` — Page only |
| `priority` | `importance`, `level`, `emphasis`, `weight` |
| `label` | `title`, `display`, `text`, `caption` |
| `requires` | `needs`, `inputs`, `dependencies`, `fields` |
| `provides` | `offers`, `actions`, `operations` |
| `produces` | `results-in`, `yields`, `creates`, `outcomes` |
| `obeys` | `follows`, `constrained-by`, `rules`, `validations` |
| `consumes` | `reads`, `uses`, `fetches`, `depends-on` |

### Rule 4: Reference Shapes Are Layered

UISL uses two reference shapes. Do not mix them in the same position.

#### Local Spec References

Local/spec references use lowercase `concept.id`:

```yaml
page.login
section.credential-entry
capability.authentication
input.email
action.submit
state.loading
constraint.email-format
feedback.auth-failed
navigation.go-to-home
data.projects
```

Use these inside Normal Forms and canonical UISL specs.

#### Taxonomy References

Taxonomy references use full taxonomy paths:

```yaml
State: Lifecycle.Loading
Action: CRUD.Delete
Section: Overlay.FocusOverlay
Page: EntryPoint
```

Use these inside taxonomy files or when explicitly referring to taxonomy nodes.

### Rule 5: Definition vs Reference

Define entities as complete objects where they are declared. Reference already-defined entities by `concept.id`.

```yaml
inputs:
  - id: email
    kind: credential
    label: "Email"
    validation:
      - constraint.email-format

capabilities:
  - id: authentication
    intent: "user verifies identity"
    requires:
      - input.email
    provides:
      - action.submit
```

Do not inline partial objects in reference positions.

### Rule 6: Value Types Are Canonical

For enumerations, there is exactly one canonical value. If an alias can map to more than one canonical value, it is ambiguous and must require context rather than auto-normalizing.

### Rule 7: Alias Policy

- Aliases are read-only normalization hints.
- Agents must never emit aliases.
- An alias must resolve to one canonical value within its local concept/property context.
- If context is insufficient, the expression is ambiguous and must not auto-map.
- Ambiguous aliases should be documented as false friends or context-required mappings.

### Rule 8: Conditions Are Declarative

Condition syntax is canonical — no JS expressions, React patterns, or implementation code.

```text
State: Category.Leaf is active
data-id.field == value
input-id is empty
input-id is not empty
value != expected
value in [a, b, c]
value not in [a, b, c]
value matches pattern-id
value does not match pattern-id
expr1 AND expr2
expr1 OR expr2
value < N
```

Examples:

- `State: Lifecycle.Processing is active`
- `data.items is empty`
- `input.email is empty`
- `data.user-role != admin`
- `data.dialog-mode in [edit, clone] AND data.user-role == admin`

### Rule 9: Validation Uses Constraints

Input validation is canonicalized through `Constraint` entities. Inputs reference constraints; they do not inline validation fragments.

```yaml
input:
  id: email
  kind: credential
  label: "Email"
  validation:
    - constraint.email-format
    - constraint.email-required
```

Non-canonical inputs like HTML `required`, `min`, `max`, `pattern`, or schema-library validators normalize to Constraint records first.

### Rule 10: Layout Belongs Only to Page and Section

- Page may use `layout`.
- Section may use `layout-pattern`.
- Capability must not carry layout. A Capability describes what the user can accomplish, not where or how it is spatially arranged.

---

## Shared Enum Types

### Priority

Used by: `action`, `section`, `decision`

| Canonical Value | Aliases |
|-----------------|---------|
| `primary` | `main`, `principal`, `default`, `filled`, `solid`, `strong`, `emphasized` |
| `secondary` | `supporting`, `auxiliary`, `side` |
| `tertiary` | `minor`, `subtle`, `peripheral`, `low-emphasis`, `footnote` |
| `destructive` | `danger`, `critical`, `harmful`, `delete`, `remove` |

### Severity

Used by: `constraint`, `feedback`

| Canonical Value | Aliases |
|-----------------|---------|
| `error` | `fail`, `problem`, `negative`, `red`, `critical`, `block`, `reject`, `invalid` |
| `warning` | `caution`, `amber`, `yellow`, `attention`, `alert`, `warn` |
| `info` | `neutral`, `blue`, `note`, `informational`, `notice`, `hint` |
| `success` | `ok`, `done`, `positive`, `green`, `pass` |

---

## Canonical Relationship Table

| Source | Relationship | Target | Canonical Property |
|--------|--------------|--------|--------------------|
| Page | contains | Section | `sections` |
| Page | guarded-by | Constraint | `guarded-by` |
| Page | navigation-in | Navigation | `navigation-in` |
| Page | navigation-out | Navigation | `navigation-out` |
| Section | contains | Capability | `contains` |
| Section | contains | Section | `sections` |
| Section | obeys | Constraint | `obeys` |
| Section | receives | Data | `receives` |
| Capability | requires | Input | `requires` |
| Capability | provides | Action | `provides` |
| Capability | produces | State | `produces` |
| Capability | communicates | Feedback | `communicates` |
| Capability | consumes | Data | `consumes` |
| Capability | obeys | Constraint | `obeys` |
| Capability | explains | Decision | `explains` |
| Input | obeys | Constraint | `validation` |
| Input | maps-to | Data | `maps-to` |
| Input | sources-from | Data | `source` |
| Action | triggers | State | `triggers` |
| Action | produces | Feedback | `produces` |
| Action | obeys | Constraint | `obeys` |
| Action | may-lead-to | Decision | `may-lead-to` |
| Action | may-lead-to | Navigation | `navigates-to` |
| Action | can-target | Capability | `target` |
| State | may-trigger | Feedback | `may-trigger` |
| State | may-lead-to | Decision | `may-lead-to` |
| State | may-lead-to | Navigation | `may-lead-to` |
| State | obeys | Constraint | `obeys` |
| Feedback | obeys | Constraint | `visible-when` |
| Feedback | may-lead-to | Decision | `may-lead-to` |
| Decision | evaluates | State / Data / Constraint | `evaluates` |
| Decision | resolves-to | Navigation / State / Action / Feedback | `branches[].resolves-to` |
| Navigation | source | Page / Section / Capability | `source` |
| Navigation | target | Page / Section / Capability / External | `target` |
| Navigation | carry-state | State | `carry-state` |
| Navigation | carry-data | Data | `carry-data` |
| Data | maps-to | Input | `maps-to` |
| Data | feeds | Section | `feeds` |
| Data | affects | State / Constraint / Decision | `affects` |
| Constraint | applies-to | Input / Action / State / Capability / Section / Page / Feedback | `applies-to` |

---

## Example: Canonical Auth Page

```yaml
page:
  id: login
  label: "Sign In"
  purpose: "entry-point for identity verification"
  layout: centered-column
  sections:
    - section.credential-entry

sections:
  - id: credential-entry
    contains:
      - capability.authentication

capabilities:
  - id: authentication
    intent: "user provides credentials to verify identity"
    requires:
      - input.email
      - input.password
    provides:
      - action.submit
    produces:
      - state.loading
      - state.success
      - state.error

inputs:
  - id: email
    kind: credential
    label: "Email"
    validation:
      - constraint.email-format
  - id: password
    kind: credential
    label: "Password"
    sensitive: true
    validation:
      - constraint.password-min-length

actions:
  - id: submit
    intent: submit
    priority: primary
    label: "Sign In"

constraints:
  - id: email-format
    condition: "input.email does not match email-pattern"
    applies-to: validity
    severity: error
  - id: password-min-length
    condition: "input.password.length < 8"
    applies-to: validity
    severity: error
```

---

## Non-Equivalence: When NOT to Map

| Expression A | Expression B | Why NOT equivalent |
|-------------|-------------|-------------------|
| `input: { kind: text }` | `input: { kind: long-text }` | Short text vs multi-line — different interaction model |
| `action: { intent: dismiss }` | `action: { intent: cancel }` | Dismiss = close overlay; Cancel = abandon input |
| `state: loading` | `feedback: { kind: progress }` | Loading is the condition; progress is communication about it |
| `capability.search` | `action.search` | Search-as-capability is the complete UX; search-as-action is the trigger |
| `section: { layout-pattern: overlay }` | `page: { layout: centered-column }` | Section and Page have distinct layout scopes |

---

## File Convention

| Convention | Value |
|------------|-------|
| Directory | `normal-forms/` |
| Naming | `<concept>.nf.yaml` |
| Purpose | One file per ontology concept, defining canonical form + read-side equivalence mappings |

Each `.nf.yaml` follows this structure:

```yaml
concept: <ConceptName>
canonical-form:
  <concept>:
    <required-property>: <Type>
    <optional-property>: <Type?>

equivalences:
  - non-canonical: <expression>
    maps-to: <canonical mapping>
    resolution: <how to resolve>

false-friends:
  - expression: <looks-like>
    not-equivalent-because: <reason>
```

---

## Next Steps

- Phase 4: Design Canonical Schema (YAML structure conforming to NFs and Relationship Matrix)
- Phase 5: Build Vocabulary Registry ✅ — see [`../registry/`](../registry/)

---

**Version**: 0.1.0-draft
**Status**: Phase 2.5 — Normal Forms Defined
**Last Updated**: 2026-06-27
