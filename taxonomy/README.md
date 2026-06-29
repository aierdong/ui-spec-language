# Taxonomy — Inheritance Rules

## Purpose

Taxonomy defines the "is-a" hierarchy of each concept.
Each node inherits default behavior rules from its ancestors.
The Agent uses this to infer behavior without requiring explicit declarations in every Spec.

## File Conventions

| Convention | Value |
|------------|-------|
| Directory | `taxonomy/` |
| Naming | `<concept>.taxonomy.yaml` |
| Format | YAML (both human-readable and machine-parseable) |

## Inheritance Rules

### Rule 1: Cascade
A child node inherits ALL `inherits` properties from its parent, grandparent, and all ancestors.

### Rule 2: Override
A child node can override an inherited property by redeclaring the same key with a different value.

```
Create inherits priority: primary from CRUD
→ Create can override to priority: secondary if the Spec demands it
```

### Rule 3: Extend (for lists)
For list-valued properties like `produces` or `feedback`, a child node's values are **appended** to the parent's values, not replaced.

```
CRUD inherits:
  produces:
    - "State: Lifecycle.Loading"
    - "State: Outcome.Error"

Create extends:
  produces:
    - "State: Validation.Validating"   # ← appended, not replacing parent's list

→ Create resolves to: produces [Lifecycle.Loading, Outcome.Error, Validation.Validating]
```

### Rule 4: Spec Override (highest priority)
Any property explicitly declared in a UISpec YAML trumps ALL Taxonomy inheritance.

```
Priority chain: Spec declaration > Taxonomy inheritance > Concept default
```

### Rule 5: Undefined properties
An undefined property in `inherits` at any level means the Agent should use a sensible platform default. It does NOT mean the property is forbidden.

## How the Agent Uses Taxonomy

When an Agent encounters an Action in a Spec:

```yaml
capability: authentication
  actions:
    - id: submit
      intent: submit-auth
      # Note: no priority declared, no feedback declared
```

The Agent resolves the action through the Taxonomy:

```
1. Look up "submit-auth" in taxonomy/action.taxonomy.yaml
2. Find it under Action → Submit → SubmitAuth
3. Inherit from ancestors:
   - Submit: priority=primary, feedback(error)=sticky-error-message
   - SubmitAuth: feedback(error)=auth-failed-message (overrides parent)
4. Resolved:
   priority: primary (from Submit)
   produces: [State: Lifecycle.Loading, State: Outcome.Success, State: Outcome.Error] (from Submit)
   feedback.error: auth-failed-message (from SubmitAuth, overrode Submit)
   may-lead-to: Decision: Authentication.AuthOutcome (from SubmitAuth)
5. Agent writes code with these defaults — no need to declare in Spec
```

## Cross-Reference Format

Taxonomy files reference nodes across concepts using a unified format. Local UISL specs use lowercase `concept.id` references; taxonomy files use the full `Concept: Category.Child` form below.

### Format

```
Concept: Category.Child
```

### Rules

| Rule | Example | Meaning |
|------|---------|---------|
| **Leaf reference** | `State: Lifecycle.Loading` | References a specific leaf node at its full hierarchy path |
| **Subtree reference** | `Action: Submit` | References all descendants of a category node (used in `blocks`, `triggers`) |
| **Parent.Child** | Use `.` as hierarchy separator within a concept | |
| **Cross-concept** | Use `: ` (colon-space) between concept name and path | |

### Examples

```yaml
# Leaf reference — specific node
produces:
  - "State: Lifecycle.Loading"       # ✅ full path
  - "State: Outcome.Success"          # ✅ full path

# Subtree reference — entire category
blocks:
  - "Action: Submit"                  # ✅ blocks all Submit.* actions
  - "Action: CRUD.Delete"             # ✅ leaf: blocks only Delete

# Cross-concept in conditions
condition: "State: Lifecycle.Processing is active"
condition: "Action: CRUD.Delete is triggered"

# Common errors (NOT valid)
- "State: Loading"                    # ❌ missing category
- "Decision: auth-outcome"            # ❌ kebab-case, missing category
- "Action: SubmitAuth"                # ❌ missing Submit. prefix
```

### How the Agent Resolves References

```
Agent reads: "State: Lifecycle.Loading"
  → Look up: state.taxonomy.yaml
  → Walk path: Lifecycle → Loading
  → Found leaf: inherits { blocks: [...], triggers: [...] }
  → Apply inherited behavior

Agent reads: "Action: Submit" (subtree)
  → Look up: action.taxonomy.yaml
  → Walk path: Submit
  → This is a category node, match all descendants
  → Resolves to: SubmitAuth, SubmitForm, SubmitPayment
```

---

## Files

| # | File | Status |
|---|------|--------|
| 1 | `action.taxonomy.yaml` | ✓ Complete |
| 2 | `input.taxonomy.yaml` | ✓ Complete |
| 3 | `state.taxonomy.yaml` | ✓ Complete |
| 4 | `feedback.taxonomy.yaml` | ✓ Complete |
| 5 | `capability.taxonomy.yaml` | ✓ Complete |
| 6 | `section.taxonomy.yaml` | ✓ Complete |
| 7 | `data.taxonomy.yaml` | ✓ Complete |
| 8 | `constraint.taxonomy.yaml` | ✓ Complete |
| 9 | `decision.taxonomy.yaml` | ✓ Complete |
| 10 | `navigation.taxonomy.yaml` | ✓ Complete |
| 11 | `page.taxonomy.yaml` | ✓ Minimal |

### Page taxonomy scope

Page taxonomy exists only for generic page roles and inherited page-level defaults, such as entry points, workspaces, detail pages, settings pages, flow steps, and error-recovery pages. It must not enumerate concrete application pages, routes, or URLs.

Concrete pages remain application-defined in specs and registries. Page taxonomy helps Agents infer defaults such as `layout` and `requires-auth` from a generic role, not from a route name.

## Rule: Required Properties on Category Nodes

Category nodes (non-leaf nodes) are classification abstractions, not spec instances.
They do not need to carry Required Properties (e.g., `target` for Navigation, `condition` for Constraint, `kind` for Feedback, `source` for Data).
Required Properties are enforced at instantiation time when the taxonomy node is used in a spec.

Category nodes exist to define inheritance and classification rules. Their children (leaf nodes or spec instances) carry the required properties needed for generation.

## Taxonomy-Specific Properties

Some properties in taxonomy files are not defined in the corresponding ontology. These are **taxonomy-level extensions** — behavioral hints that help the Agent make rendering decisions during code generation. They do NOT change the ontology definition; they add implementation guidance within the inheritance chain.

| Property | Used In | Meaning |
|----------|---------|---------|
| `blocking: true` | Action, State, Feedback | Blocks user interaction during processing |
| `instant: true` | Action, Capability | Takes effect without loading indicator |
| `opens: overlay\|inline\|external` | Action, Navigation | Where the result is presented |
| `pre-populates: bool` | Action | Whether form fields start with existing data |
| `requires: [...]` | Action | Inputs this Action type typically needs |
| `preserves-state: bool` | Navigation | Back-button returns to previous page state |
| `blocks-background: bool` | Navigation | Overlay blocks interaction with background |
| `discards-changes: bool` | Action, Navigation | Whether the action/navigation discards unsaved changes |
| `clears-session: bool` | Action, Navigation | Whether the action/navigation terminates the user session |
| `animated: bool` | Navigation | Whether the navigation transition is animated |

## Dual-Identity Concepts: Capability vs Action

Some concepts appear both as Capabilities and as Actions in the taxonomy. This is intentional:

| Concept | As Capability | As Action |
|---------|-------------|-----------|
| **Export** | A workspace function that manages data export (select format, configure options, trigger download) | The trigger event that initiates the export (click "Export") |
| **Navigate** | A capability that manages navigation state (breadcrumbs, history, deep links) | The trigger event that moves the user to a target (click a link) |
| **Search** | A complete search UX (input field, results display, filters, facets) | The trigger event that executes the search (click "Search") |
| **Sort** | A capability for ordering data columns (column header clicks, sort direction state) | The trigger event that applies sort (click column header) |
| **Filter** | A capability for data filtering (filter panel, active filter chips, clear-all) | The trigger event that applies a filter (select filter option) |

**Rule**: A Capability *provides* Actions. When a concept appears in both trees, the Capability describes the function space, and the Action describes the trigger. The Agent uses context to determine which level is being referenced.

---

**Version**: 0.1.0-draft
**Last Updated**: 2026-06-26
