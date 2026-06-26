# Normal Forms — Canonical Representation Rules

## Purpose

Many Agents fail not because they cannot write YAML, but because **the same semantic intent can be expressed in many different YAML shapes**. An Agent that encounters any of these three forms:

```yaml
# Form A
role: form-field
type: email

# Form B
field:
  kind: email

# Form C
credential:
  type: email
```

...must recognize them as **semantically equivalent** — all three describe a credential input for an email address. Without a Normal Form, the Agent sees three different patterns and cannot reliably map, validate, or compose them.

> **A Normal Form (NF) defines the ONE canonical YAML structure for each semantic entity. All equivalent expressions are mapped to this single form.**

This is borrowed from database normalization theory: just as 3NF eliminates update anomalies, UISL Normal Forms eliminate **Agent reasoning anomalies**.

---

## Core Rules

### Rule 1: One Canonical Form per Semantic Entity

For every concept in the Ontology, there is exactly ONE canonical YAML shape.

| Semantic Entity | Canonical Expression |
|----------------|---------------------|
| An email credential input | `input: { id: email, kind: credential, label: "Email" }` |
| A primary submit action | `action: { id: submit, intent: submit, priority: primary }` |
| An authentication capability | `capability: { id: authentication, requires: [email, password], provides: [submit] }` |

The canonical form is the **only form** an Agent should output when generating UISL. The Agent may READ alternative forms (input parsing), but must WRITE only canonical forms (output generation).

### Rule 2: Equivalence Mapping (Read-side Tolerance)

For every canonical form, the NF document lists **equivalent alternative expressions** that map to it. This allows the Agent to consume diverse inputs without confusion.

```
Non-canonical:  role: form-field, type: email
              → maps to: input.kind = credential, input.id = email

Non-canonical:  field: { kind: email }
              → maps to: input.kind = credential, input.id = email

Non-canonical:  credential: { type: email }
              → maps to: input.kind = credential, input.id = email
```

### Rule 3: Property Names are Canonical

There is ONE canonical property name for each attribute. Aliases are documented but never generated.

| Canonical Property | Aliases (never generate) |
|-------------------|--------------------------|
| `kind` | `type`, `role`, `category`, `input-type`, `field-type` |
| `id` | `name`, `key`, `ref`, `identifier` |
| `intent` | `purpose`, `goal`, `action-type`, `behavior` |
| `priority` | `importance`, `level`, `emphasis`, `weight` |
| `label` | `title`, `display`, `text`, `caption` |
| `requires` | `needs`, `inputs`, `dependencies`, `fields` |
| `provides` | `offers`, `actions`, `operations` |
| `produces` | `results-in`, `yields`, `creates`, `outcomes` |
| `obeys` | `follows`, `constrained-by`, `rules`, `validations` |
| `consumes` | `reads`, `uses`, `fetches`, `depends-on` |

### Rule 4: Structure is Canonical

The nesting / containment structure is fixed. No flattening, no reordering of semantic layers.

```
✅ Canonical:
capability:
  id: authentication
  requires:
    - input:
        id: email
        kind: credential

❌ Non-canonical (flattened):
capability: authentication
requires-email: credential    # Missing Input wrapper

❌ Non-canonical (inverted):
inputs:
  - email: credential         # Input is not the outer key
capability: authentication
```

### Rule 5: Value Types are Canonical

For enumerations, there is exactly ONE valid string form.

| Concept | Canonical Values | Aliases |
|---------|-----------------|---------|
| `input.kind` | `credential`, `text`, `long-text`, `number`, `boolean`, `single-select`, `multi-select`, `date`, `datetime`, `duration`, `file`, `tag-list` | `email` → `credential`; `textarea` → `long-text`; `dropdown` → `single-select`; `checkbox` → `boolean` |
| `action.priority` | `primary`, `secondary`, `tertiary`, `destructive` | `main` → `primary`; `danger` → `destructive` |
| `state` | `idle`, `loading`, `empty`, `error`, `success`, `processing` | `fetching` → `loading`; `failed` → `error` |

---

## Equivalence Mapping Reference

### Input Equivalences

| Non-Canonical Expression | Canonical Form | Resolution Rule |
|--------------------------|----------------|-----------------|
| `type: email` | `kind: credential` | `email` maps to credential Input by Taxonomy: Input → Credential → Email |
| `field: email` | `input: { kind: credential }` | `field` is alias for `input`; `email` maps to credential |
| `input-type: password` | `kind: credential`, `sensitive: true` | `password` maps to credential; inherently sensitive |
| `component: Checkbox` | `kind: boolean` | Widget name → InputKind mapping |
| `widget: dropdown` | `kind: single-select` | Widget name → InputKind mapping |
| `role: form-control` | *(no equivalence)* | Too generic; requires additional context |

### Action Equivalences

| Non-Canonical Expression | Canonical Form | Resolution Rule |
|--------------------------|----------------|-----------------|
| `component: Button, variant: primary` | `priority: primary` | Button variant → Action priority |
| `onClick: handleSubmit` | `intent: submit` | Event handler name → Action intent |
| `type: submit` (in HTML context) | `intent: submit, priority: primary` | HTML button type → Action intent |
| `role: destructive-action` | `priority: destructive` | Role description → Action priority |
| `button: Save` | `intent: submit, label: "Save"` | Button label + context → Action intent |

### Capability Equivalences

| Non-Canonical Expression | Canonical Form | Resolution Rule |
|--------------------------|----------------|-----------------|
| `page-type: login` | `capability: { id: authentication }` | Page type → primary Capability |
| `feature: sign-in` | `capability: { id: authentication }` | Feature name → Taxonomy alias match |
| `screen: LoginScreen` | `page: { id: login, capability: authentication }` | Screen name → Page + Capability |
| `section: auth-form` | `section: { id: credential-entry, contains: authentication }` | Section name → Section taxonomy + Capability |

### State Equivalences

| Non-Canonical Expression | Canonical Form | Resolution Rule |
|--------------------------|----------------|-----------------|
| `isLoading: true` | `state: loading` | Boolean flag → State name |
| `hasError: true` | `state: error` | Error flag → State name |
| `isEmpty: true` | `state: empty` | Empty flag → State name |
| `showSpinner: true` | *(not a State — this is Feedback.Progress)* | Visual description → Feedback concept |

---

## Agent Decision Tree

When an Agent receives ambiguous input, it resolves to canonical form using this decision tree:

```
1. PARSE: Extract all key-value pairs
   ↓
2. CLASSIFY: For each value, check Taxonomy aliases
   Example: "email" → Input.Credential.Email → kind: credential
   ↓
3. STRUCTURE: Map flattened keys to canonical nesting
   Example: "requires-email" → capability.requires[input(id=email, kind=credential)]
   ↓
4. VALIDATE: Check against NF rules
   Example: credential + sensitive:true → valid; text → must not have sensitive:true
   ↓
5. OUTPUT: Emit only canonical form
```

### Example: Agent resolves ambiguous auth page spec

**Input** (ambiguous, from a human prompt):
```yaml
page: login
fields:
  - type: email
  - name: password, input-type: password
  - role: checkbox, label: Remember me
actions:
  - text: Sign In, variant: primary, type: submit
  - text: Cancel, variant: secondary
```

**Resolution steps**:
```
Step 2 — CLASSIFY:
  "email" → Taxonomy: Input.Credential.Email → kind: credential
  "password" → Taxonomy: Input.Credential.Password → kind: credential, sensitive: true
  "checkbox" → Taxonomy: Input.Selection.Boolean → kind: boolean

Step 3 — STRUCTURE:
  "fields" → canonical: capability.requires → Input[]
  "actions" → canonical: capability.provides → Action[]
  "page: login" → canonical: capability.id = authentication (Taxonomy alias match)

Step 4 — VALIDATE:
  credential + sensitive:true → ✓ (Password is sensitive)
  Remember me → boolean → default: false → ✓
  Sign In → intent: submit, priority: primary → ✓
  Cancel → intent: dismiss, priority: secondary → ✓
```

**Output** (canonical):
```yaml
page:
  id: login
  label: "Sign In"
  sections:
    - id: credential-entry
      capabilities:
        - id: authentication
          requires:
            - input:
                id: email
                kind: credential
                label: "Email"
                validation:
                  - format: email
            - input:
                id: password
                kind: credential
                label: "Password"
                sensitive: true
                validation:
                  - min-length: 8
            - input:
                id: remember-me
                kind: boolean
                label: "Remember me"
                default: false
          provides:
            - action:
                id: submit
                intent: submit
                priority: primary
                label: "Sign In"
            - action:
                id: cancel
                intent: dismiss
                priority: secondary
                label: "Cancel"
          produces:
            - state: loading
            - state: success
            - state: error
```

---

## Non-Equivalence: When NOT to map

Some expressions look similar but are NOT semantically equivalent. These are **false friends** that the Agent must distinguish:

| Expression A | Expression B | Why NOT equivalent |
|-------------|-------------|-------------------|
| `input: { kind: text }` | `input: { kind: long-text }` | Short text vs multi-line — different interaction model |
| `action: { intent: dismiss }` | `action: { intent: cancel }` | Dismiss = close overlay; Cancel = abandon input (may discard data) |
| `state: loading` | `state: processing` | Loading = fetching data; Processing = executing action. Different blocking rules. |
| `capability: { id: search }` | `action: { intent: search }` | Search-as-capability contains the full search UX; search-as-action is the trigger event. Not interchangeable. |
| `section: { layout-pattern: overlay }` | `section: { layout-pattern: centered-column }` | Different spatial intents; cannot auto-convert. |

---

## File Convention

| Convention | Value |
|------------|-------|
| Directory | `normal-forms/` |
| Naming | `<concept>.nf.yaml` |
| Purpose | One file per ontology concept, defining its canonical form + equivalence mappings |

Each `.nf.yaml` follows this structure:

```yaml
concept: <ConceptName>
canonical-form:
  # The ONE valid YAML shape for this concept
  <property>: <canonical key name>
  ...

equivalences:
  # Alternative expressions that map to this canonical form
  - non-canonical: <expression>
    maps-to: <canonical mapping>
    resolution: <how to resolve>

false-friends:
  # Expressions that look similar but are NOT equivalent
  - expression: <looks-like>
    not-equivalent-because: <reason>
```

---

## Next Steps

- Phase 3: Define formal Relationships between concepts
- Phase 4: Design Canonical Schema (YAML structure conforming to NFs)
- Phase 5: Build Vocabulary Registry (enforce NFs at registry entry)

---

**Version**: 0.1.0-draft
**Status**: Phase 2.5 — Normal Forms Defined
**Last Updated**: 2026-06-26
