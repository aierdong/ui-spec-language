# Relationship — Concept Connection Rules

## Purpose

Relationship defines how UISL concepts can connect to each other.

Phase 1 defines **what each concept means**.
Phase 2 defines **where each concept sits in the taxonomy**.
Phase 2.5 defines **the one canonical shape for each concept**.
Phase 3 defines **which concepts may reference each other, in which direction, and why**.

A Relationship is semantic. It is not a YAML nesting convenience and not a renderer instruction.

---

## Core Rule

> **A Relationship must describe a meaningful dependency, containment, flow, or constraint between concepts.**

Valid relationship names answer questions such as:

| Relationship | Question |
|---|---|
| `contains` | What is structurally inside this concept? |
| `requires` | What must be provided for this capability to work? |
| `provides` | What user actions are available? |
| `produces` | What states or feedback can result? |
| `triggers` | What condition starts after this action or state? |
| `may-lead-to` | What flow may happen next? |
| `explains` | What decision describes the branch logic? |
| `evaluates` | What information determines a decision? |
| `resolves-to` | What target is chosen by a decision branch? |
| `obeys` | What persistent rule limits availability, visibility, or validity? |
| `consumes` | What data does a capability read? |
| `maps-to` | What data field does an input bind to? |
| `feeds` | What section receives data for presentation? |
| `source` | Where does navigation start? |
| `target` | Where does navigation arrive? |
| `carry-state` | What UI condition survives navigation? |
| `carry-data` | What data context moves with navigation? |

Relationship names must be verbs or verb phrases. They must not be component names, CSS concepts, framework APIs, or implementation events.

---

## Relationship Graph

```text
Page
  ├─ contains ──────────────→ Section
  ├─ guarded-by ────────────→ Constraint
  ├─ navigation-in ─────────→ Navigation
  └─ navigation-out ────────→ Navigation

Section
  ├─ contains ──────────────→ Capability
  ├─ contains ──────────────→ Section
  ├─ obeys ─────────────────→ Constraint
  └─ receives ──────────────→ Data

Capability
  ├─ requires ──────────────→ Input
  ├─ provides ──────────────→ Action
  ├─ produces ──────────────→ State
  ├─ communicates ──────────→ Feedback
  ├─ consumes ──────────────→ Data
  ├─ obeys ─────────────────→ Constraint
  └─ explains ──────────────→ Decision

Input
  ├─ obeys ─────────────────→ Constraint
  ├─ maps-to ───────────────→ Data
  └─ sources-from ──────────→ Data

Action
  ├─ triggers ──────────────→ State
  ├─ produces ──────────────→ Feedback
  ├─ obeys ─────────────────→ Constraint
  ├─ may-lead-to ───────────→ Decision
  ├─ may-lead-to ───────────→ Navigation
  └─ can-target ────────────→ Capability

State
  ├─ is-triggered-by ───────→ Action          *(inverse, read-only)*
  ├─ may-trigger ───────────→ Feedback
  ├─ may-lead-to ───────────→ Decision
  ├─ may-lead-to ───────────→ Navigation
  └─ obeys ─────────────────→ Constraint

Feedback
  ├─ triggered-by ──────────→ State           *(inverse, read-only)*
  ├─ produced-by ───────────→ Action          *(inverse, read-only)*
  ├─ obeys ─────────────────→ Constraint
  └─ may-lead-to ───────────→ Decision

Decision
  ├─ evaluates ─────────────→ State
  ├─ evaluates ─────────────→ Data
  ├─ evaluates ─────────────→ Constraint
  ├─ resolves-to ───────────→ Navigation
  ├─ resolves-to ───────────→ State
  ├─ resolves-to ───────────→ Action
  └─ resolves-to ───────────→ Feedback

Navigation
  ├─ source ────────────────→ Page | Section | Capability
  ├─ target ────────────────→ Page | Section | Capability | External
  ├─ carry-state ───────────→ State
  └─ carry-data ────────────→ Data

Data
  ├─ maps-to ───────────────→ Input
  ├─ feeds ─────────────────→ Section
  └─ affects ───────────────→ State | Constraint | Decision

Constraint
  └─ applies-to ────────────→ Input | Action | State | Capability | Section | Page | Feedback
```

> **Legend**: Entries marked *(inverse, read-only)* are inverse relationships included for reading and round-tripping only. Agents must never emit them when generating specs — always use the canonical direction instead. See [Generation Rules](#generation-rules) for details.

---

## Canonical Relationship Matrix

The full machine-readable matrix is in [`relationship.matrix.yaml`](relationship.matrix.yaml).

| Source | Relationship | Target | Cardinality | Required? | Meaning |
|---|---|---|---|---|---|
| Page | `contains` | Section | `1..*` | recommended | A page is partitioned into sections. |
| Page | `guarded-by` | Constraint | `0..*` | no | Page access is gated by persistent rules. |
| Page | `navigation-in` | Navigation | `0..*` | no | Ways users can arrive at this page. |
| Page | `navigation-out` | Navigation | `0..*` | no | Ways users can leave this page. |
| Section | `contains` | Capability | `0..*` | no | A section groups capabilities. |
| Section | `contains` | Section | `0..*` | no | Sections may be nested when spatial partitioning is hierarchical. |
| Section | `obeys` | Constraint | `0..*` | no | Section visibility or availability follows a rule. |
| Section | `receives` | Data | `0..*` | no | Section receives data for read-only presentation. *(avoid-unless-needed)* |
| Capability | `requires` | Input | `0..*` | no | Information the user must provide. |
| Capability | `provides` | Action | `0..*` | no | Actions available within the capability. |
| Capability | `produces` | State | `0..*` | no | Conditions that can arise from this capability. |
| Capability | `communicates` | Feedback | `0..*` | no | Communication available within this capability. |
| Capability | `consumes` | Data | `0..*` | no | Data read by this capability. |
| Capability | `obeys` | Constraint | `0..*` | no | Rules limiting the whole capability. |
| Capability | `explains` | Decision | `0..*` | no | Branching logic inside the capability. |
| Input | `obeys` | Constraint | `0..*` | no | Validation, visibility, or availability rules for the input. |
| Input | `maps-to` | Data | `0..1` | no | Data field the input value binds to. |
| Input | `sources-from` | Data | `0..1` | no | Data source for selectable or default values. |
| Action | `triggers` | State | `0..*` | no | State that begins when the action is invoked. |
| Action | `produces` | Feedback | `0..*` | no | User communication caused by the action. |
| Action | `obeys` | Constraint | `0..*` | no | Availability or visibility rules for the action. |
| Action | `may-lead-to` | Decision | `0..1` | no | Branch point after the action. |
| Action | `may-lead-to` | Navigation | `0..1` | no | Movement after the action. |
| Action | `can-target` | Capability | `0..1` | no | Capability affected by the action. |
| State | `may-trigger` | Feedback | `0..*` | no | Communication shown when a state occurs. |
| State | `may-lead-to` | Decision | `0..1` | no | State-driven branching. |
| State | `may-lead-to` | Navigation | `0..1` | no | State-driven movement. |
| Feedback | `may-lead-to` | Decision | `0..1` | no | A feedback message offers a choice or next step. |
| Feedback | `obeys` | Constraint | `0..*` | no | Rules controlling when feedback is shown. |
| Decision | `evaluates` | State | `0..*` | no | State informing branch selection. |
| Decision | `evaluates` | Data | `0..*` | no | Data informing branch selection. |
| Decision | `evaluates` | Constraint | `0..*` | no | Rules considered by branch selection. |
| Decision | `resolves-to` | Navigation | `0..*` | no | Branch outcome is a movement. |
| Decision | `resolves-to` | State | `0..*` | no | Branch outcome is a condition. |
| Decision | `resolves-to` | Action | `0..*` | no | Branch outcome is another user/system action. |
| Decision | `resolves-to` | Feedback | `0..*` | no | Branch outcome is user communication. |
| Navigation | `source` | Page/Section/Capability | `0..1` | no | Where movement starts. |
| Navigation | `target` | Page/Section/Capability/External | `1..1` | yes | Where movement arrives. |
| Navigation | `carry-state` | State | `0..*` | no | State preserved across movement. |
| Navigation | `carry-data` | Data | `0..*` | no | Data context passed with movement. |
| Data | `feeds` | Section | `0..*` | no | Sections that present this data. |
| Data | `maps-to` | Input | `0..*` | no | Inputs bound to this data. |
| Data | `affects` | State/Constraint/Decision | `0..*` | no | UI conditions, rules, or branches affected by data values. |
| Constraint | `applies-to` | Input/Action/State/Capability/Section/Page/Feedback | `1..*` | recommended | Targets governed by this persistent rule. |

---

## Relationship Categories

### 1. Structural Relationships

Structural relationships define stable composition.

| Relationship | Valid Sources | Valid Targets |
|---|---|---|
| `contains` | Page, Section | Section, Capability |
| `navigation-in` | Page | Navigation |
| `navigation-out` | Page | Navigation |

Rules:

1. `Page contains Section`, not `Page contains Capability` directly.
2. `Section contains Capability` or nested `Section`.
3. `Capability` is not a container; it does not `contain` Input or Action. It `requires` Input and `provides` Action.
4. Navigation links pages and destinations, but does not own pages.

### 2. Dependency Relationships

Dependency relationships say what a concept needs or reads.

| Relationship | Valid Sources | Valid Targets |
|---|---|---|
| `requires` | Capability | Input |
| `consumes` | Capability | Data |
| `sources-from` | Input | Data |
| `maps-to` | Input, Data | Data, Input |

Rules:

1. `requires` is about user-provided information, not implementation dependencies.
2. `consumes` is about data read by a capability.
3. `maps-to` expresses binding between an Input and Data, not component props.
4. `sources-from` is for selectable/default values, not for transport details.

### 3. Flow Relationships

Flow relationships describe what happens next.

| Relationship | Valid Sources | Valid Targets |
|---|---|---|
| `provides` | Capability | Action |
| `triggers` | Action | State |
| `produces` | Capability, Action | State, Feedback |
| `may-trigger` | State | Feedback |
| `may-lead-to` | Action, State, Feedback | Decision, Navigation |
| `explains` | Capability | Decision |
| `evaluates` | Decision | State, Data, Constraint |
| `resolves-to` | Decision | Navigation, State, Action, Feedback |

Rules:

1. User-initiated behavior begins with `Action`.
2. Outcome conditions are `State`; user-facing communication is `Feedback`.
3. Branching must be represented by `Decision`, not by multiple unrelated navigation entries.
4. `Decision` chooses a path; `Navigation` is the movement path.
5. `Action may-lead-to Navigation` only when no branch needs to be explained.

### 4. Rule Relationships

Rule relationships apply persistent business constraints.

| Relationship | Valid Sources | Valid Targets |
|---|---|---|
| `obeys` | Input, Action, State, Capability, Section, Feedback | Constraint |
| `guarded-by` | Page | Constraint |
| `applies-to` | Constraint | Input, Action, State, Capability, Section, Page, Feedback |

Rules:

1. Use `Constraint` for persistent conditions.
2. Use `Decision` for one-time branching.
3. `disabled-when`, `visible-when`, and validation conditions are shorthand for `obeys Constraint`.
4. A `Constraint` must not resolve to a destination; that is a `Decision`.

### 5. Navigation Context Relationships

Navigation context relationships define topology and carried context.

| Relationship | Valid Sources | Valid Targets |
|---|---|---|
| `source` | Navigation | Page, Section, Capability |
| `target` | Navigation | Page, Section, Capability, External |
| `carry-state` | Navigation | State |
| `carry-data` | Navigation | Data |

Rules:

1. `target` is required for every Navigation.
2. Internal targets use concept references: `page.home`, `section.details`, `capability.project-form`.
3. External targets may be URLs.
4. Routes and URLs are not Navigation targets unless external.
5. Post-authentication movement should usually be `method: replace` to avoid returning to login by history.

---

## Directionality Rules

Relationships are directional. The source owns the semantic statement.

| Canonical Direction | Inverse Phrase | Agent Rule |
|---|---|---|
| `Page contains Section` | Section belongs to Page | Emit `contains` from Page. |
| `Section contains Capability` | Capability lives in Section | Emit `contains` from Section. |
| `Capability requires Input` | Input is required by Capability | Emit `requires` from Capability. |
| `Capability provides Action` | Action is provided by Capability | Emit `provides` from Capability. |
| `Capability produces State` | State arises from Capability | Emit `produces` from Capability. |
| `Capability communicates Feedback` | Feedback belongs to Capability | Emit `communicates` from Capability. |
| `Action triggers State` | State is triggered by Action | Emit `triggers` from Action. |
| `Action produces Feedback` | Feedback is produced by Action | Emit `produces` from Action. |
| `Action can-target Capability` | Capability is targeted by Action | Emit `can-target` from Action when the action affects a different capability. |
| `State may-trigger Feedback` | Feedback is triggered by State | Prefer `may-trigger` from State when modeling condition-driven feedback. |
| `Decision evaluates State/Data/Constraint` | State/Data/Constraint informs Decision | Emit `evaluates` from Decision. |
| `Decision resolves-to Navigation/State/Action/Feedback` | Navigation/State/Action/Feedback is outcome of Decision | Emit `resolves-to` inside branches. |
| `Navigation target Page` | Page is target of Navigation | Emit `target` from Navigation. |

Inverse phrases can appear in prose, but canonical UISL output must use the canonical direction.

---

## Cardinality Rules

Cardinality describes valid relationship count, not required properties.
Required properties are still defined by `normal-forms/required-property-matrix.yaml`.

| Pattern | Meaning |
|---|---|
| `0..1` | Optional single target. |
| `1..1` | Exactly one target. |
| `0..*` | Optional list. |
| `1..*` | At least one target. |

Important distinctions:

1. `Page contains Section` is `1..*` as a modeling recommendation; however, `page.sections` is optional in Phase 2.5 normal forms until Phase 4 schema hardens structure.
2. `Navigation target` is `1..1` and also a required property in the required property matrix.
3. `Decision branches` are required by the Decision concept, but `Decision resolves-to` appears per branch and may target different concept types.

---

## Generation Rules

Some relationships in the matrix carry a `generation` field that constrains how Agents may emit them.

| Generation Value | Meaning | Agent Rule |
|---|---|---|
| *(absent)* | Normal forward relationship. | Emit freely from the canonical source. |
| `read-side-only` | Inverse relationship included for reading/round-tripping. | **Never emit when generating specs.** Use the canonical direction instead. |
| `avoid-unless-needed` | Forward relationship that exists for completeness but has a preferred alternative. | Prefer the alternative noted in the relationship's `rules`. Emit only when the alternative cannot express the intent. |

### Relationships with `generation` constraints

| Relationship ID | Generation | Preferred Alternative |
|---|---|---|
| `state-is-triggered-by-action` | `read-side-only` | `Action triggers State` |
| `feedback-produced-by-action` | `read-side-only` | `Action produces Feedback` |
| `data-maps-to-input` | `read-side-only` | `Input maps-to Data` |
| `data-affects-decision` | `read-side-only` | `Decision evaluates Data` |
| `constraint-applies-to-target` | `read-side-only` | `Target obeys Constraint` |
| `section-receives-data` | `avoid-unless-needed` | `Capability consumes Data` (for user work) or `Data feeds Section` (for read-only presentation) |

---

## Shorthand vs Explicit Relationship

Normal Forms use properties such as `requires`, `provides`, `produces`, `visible-when`, and `navigates-to`.
These are canonical shorthand for relationships.

| Shorthand | Expands To |
|---|---|
| `capability.requires: [input.email]` | `Capability(authentication) requires Input(email)` |
| `capability.provides: [action.submit]` | `Capability(authentication) provides Action(submit)` |
| `capability.produces: [state.loading]` | `Capability(authentication) produces State(loading)` |
| `capability.communicates: [feedback.auth-failed-message]` | `Capability(authentication) communicates Feedback(auth-failed-message)` |
| `capability.consumes: [data.projects]` | `Capability(crud) consumes Data(projects)` |
| `action.disabled-when: "items.length == 0"` | `Action(delete) obeys Constraint(no-items-selected)` |
| `action.target: capability.project-management` | `Action(delete-project) can-target Capability(project-management)` |
| `action.navigates-to: page.home` | `Action(submit) may-lead-to Navigation(go-to-home)` |
| `navigation.target: page.home` | `Navigation(go-to-home) target Page(home)` |
| `decision.branches[].resolves-to: feedback.auth-failed` | `Decision(auth-outcome) resolves-to Feedback(auth-failed)` |

Agent rule: use shorthand when writing Canonical Schema later; use explicit triples for reasoning, validation, and documentation.

---

## Validity Rules

### Rule 1: No direct Page → Capability

```text
❌ Page contains Capability
✅ Page contains Section contains Capability
```

Why: Section is the semantic partition that explains where a capability lives.

### Rule 2: Capability does not contain Input, Action, or Feedback

```text
❌ Capability contains Input
❌ Capability contains Action
❌ Capability contains Feedback
✅ Capability requires Input
✅ Capability provides Action
✅ Capability communicates Feedback
```

Why: Inputs, Actions, and Feedback are not spatial children; they are requirements, affordances, and communications.

### Rule 3: Constraint is not Decision

```text
❌ Constraint resolves-to Navigation
✅ Decision resolves-to Navigation
✅ Action obeys Constraint
```

Why: Constraints are persistent rules; Decisions are branch points.

### Rule 4: State is not Feedback

```text
❌ State message: "Invalid password" as the only representation
✅ State: auth-failed
✅ Feedback: auth-failed-message
```

Why: State is what happened; Feedback is what the user is told.

### Rule 5: Navigation is not Route

```text
❌ Navigation target: /projects/:id
✅ Navigation target: page.project-detail
✅ Navigation carry-data: data.project-id
```

Why: UISL describes the user's journey, not web routing implementation.

### Rule 6: Action is not Handler

```text
❌ Action: onClick
✅ Action: submit
✅ Action may-lead-to Navigation(go-to-home)
```

Why: Action is user intent; handlers are implementation.

### Rule 7: Action can-target Capability (for cross-capability operations)

```text
✅ Action(delete-project) can-target Capability(project-management)
✅ Action(select-all) can-target Capability(item-list)
```

Why: Some actions affect a capability different from the one they belong to (e.g., a toolbar action that targets a data grid). Use `can-target` to express this cross-capability reference.

---

## Examples

### Authentication Flow

```text
Page(login)
  contains Section(credential-entry)

Section(credential-entry)
  contains Capability(authentication)

Capability(authentication)
  requires Input(email)
  requires Input(password)
  provides Action(submit)
  produces State(processing)
  produces State(authenticated)
  produces State(auth-failed)
  communicates Feedback(auth-failed-message)
  explains Decision(auth-outcome)

Input(email)
  obeys Constraint(email-format)

Input(password)
  obeys Constraint(password-min-length)

Action(submit)
  triggers State(processing)
  may-lead-to Decision(auth-outcome)

Decision(auth-outcome)
  evaluates State(authenticated)
  evaluates State(auth-failed)
  resolves-to Navigation(go-to-home)
  resolves-to Feedback(auth-failed-message)

Navigation(go-to-home)
  target Page(home)
```

### Cross-Capability Action (can-target)

```text
Section(project-toolbar)
  contains Capability(bulk-operations)

Section(project-list)
  contains Capability(project-management)

Capability(bulk-operations)
  provides Action(delete-selected)
  provides Action(export-selected)

Action(delete-selected)
  can-target Capability(project-management)
  obeys Constraint(at-least-one-selected)
  may-lead-to Decision(delete-confirmation)
```

Why `can-target`: The `delete-selected` action lives in a toolbar capability but affects the project-management capability (the data grid). `can-target` expresses this cross-capability reference.

### Empty Collection Flow

```text
Capability(project-browsing)
  consumes Data(projects)
  produces State(empty)
  explains Decision(empty-collection)

Data(projects)
  affects State(empty)

Decision(empty-collection)
  evaluates Data(projects)
  evaluates Constraint(can-create-project)
  resolves-to Feedback(empty-state-with-create)
  resolves-to Feedback(read-only-empty-state)

Feedback(empty-state-with-create)
  may-lead-to Decision(create-project-entry)
```

---

## Counter Examples

| Incorrect | Correct | Why |
|---|---|---|
| `Page contains Button` | `Page contains Section contains Capability provides Action` | Button is implementation. |
| `Form contains Fields` | `Section contains Capability requires Input` | Form/field are implementation-level groupings. |
| `Action renders Toast` | `Action produces Feedback` | Toast is a presentation choice. |
| `State shows Spinner` | `State may-trigger Feedback(progress)` | Spinner is visual representation. |
| `Decision redirects /home` | `Decision resolves-to Navigation(go-to-home) target page.home` | Redirect/URL are implementation details. |
| `Constraint navigates to login` | `Decision(session-expiry) resolves-to Navigation(go-to-login)` | Constraint cannot move the user. |
| `Data table provides edit` | `Capability(crud) consumes Data(projects) provides Action(edit)` | Data table is a rendering pattern. |

---

## Agent Instruction

When reasoning about UISL relationships:

1. Start from the user's journey: `Page → Section → Capability`.
2. For each Capability, ask:
   - What information does it require? → `Input`
   - What can the user do? → `Action`
   - What conditions can arise? → `State`
   - What data does it read? → `Data`
   - What rules limit it? → `Constraint`
   - What branch logic exists? → `Decision`
   - What must be communicated? → `Feedback`
3. Use `Decision` whenever there are multiple possible next paths.
4. Use `Constraint` only for persistent rules about visibility, availability, or validity.
5. Use `Navigation` only for movement to a Page, Section, Capability, or external destination.
6. Never introduce relationships to components, CSS, DOM nodes, framework hooks, handler names, URLs, or API calls.
7. Emit canonical relationship names only. Aliases may be read, but not generated.

---

## Phase 3 Output

| File | Purpose |
|---|---|
| `relationships/README.md` | Human-readable Relationship rules and examples. |
| `relationships/relationship.matrix.yaml` | Machine-readable relationship matrix for validation and future schema design. |

---

**Version**: 0.1.0-draft
**Status**: Phase 3 — Relationship Definition
**Last Updated**: 2026-06-27
