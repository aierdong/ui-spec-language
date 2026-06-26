# Constraint（约束）

## Definition
A condition that restricts when a Input, Action, State, or Capability is available, visible, or valid.
A Constraint answers the question: **"Under what conditions does this rule apply?"**

Constraints are the "rules engine" of the UI. They express business logic in a declarative,
platform-independent way. A Constraint never says "hide this div" — it says "this Input
is only relevant when the user selects Business account type."

## Relationship

```
Input ──── obeys ──→ Constraint
Action    ──── obeys ──→ Constraint
State     ──── obeys ──→ Constraint
Capability ── obeys ──→ Constraint
Section   ──── obeys ──→ Constraint
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name (e.g., `email-format`, `auth-required`) |
| `condition` | Condition | The expression that must be true for this constraint to apply |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `applies-to` | TargetType | What kind of effect: `visibility`, `availability`, `validity` (default: `availability`) |
| `message` | string | Human-readable explanation when the constraint is violated |
| `severity` | Severity | `error` (blocks submission), `warning` (allows with caution), `info` (advisory) |

## Constraint Target Types

| Type | Effect |
|------|--------|
| `visibility` | Whether the element is shown or hidden |
| `availability` | Whether the element is interactive or disabled |
| `validity` | Whether the value meets business rules |

## Condition Syntax

Conditions are expressed as simple declarative expressions that reference States, Data, and Input values.

```yaml
# State-based
visible-when: "dialog-mode == create"
visible-when: "active-sub-tab in [fields, constraints]"

# Data-based
disabled-when: "items.length == 0"
visible-when: "project.status == active"

# Input-based
disabled-when: "email is empty"
visible-when: "account-type == business"

# Negation
visible-when: "auth-state != authenticated"

# Compound
visible-when: "dialog-mode in [edit, clone] AND user-role == admin"
disabled-when: "selected-tables missing required upstream tables"
```

## Severity Levels

| Severity | Effect |
|----------|--------|
| `error` | Prevents the Action from completing; requirement value is invalid |
| `warning` | Warns the user but allows the Action to proceed |
| `info` | Provides non-blocking guidance |

## Examples

| Constraint | Applies To | Condition |
|------------|------------|-----------|
| `auth-required` | `availability` | `auth-state != authenticated` |
| `project-name-required` | `validity` | `project-name is empty` |
| `email-format` | `validity` | `email does not match email-pattern` |
| `password-min-length` | `validity` | `password.length < 8` |
| `admin-only-action` | `visibility` | `user-role != admin` |
| `clone-source-summary` | `visibility` | `dialog-mode == clone` |
| `dependency-impact-warning` | `visibility` | `selected-tables missing required upstream tables` |
| `no-ops-on-empty` | `availability` | `items.length == 0` |
| `delete-confirmation` | `availability` | `item-is-critical == true` |

## Counter Examples

These are **NOT** Constraints — they are other concepts:

| What | Why it's not a Constraint |
|------|---------------------------|
| `display: none` | This is a CSS property, not a business rule |
| `disabled attribute` | This is an HTML attribute, not a business rule |
| `if (loading) return <Spinner>` | This is implementation code, not a declarative rule |
| `formik validation schema` | This is a validation library, not a semantic constraint |
| `required` HTML attribute | This is an HTML attribute; the Constraint is `validity: input is empty` |
| `conditional rendering` | This is a React pattern; the Constraint is `visibility: condition` |
| `useMemo` / `useCallback` | These are performance optimizations, not business rules |
| `rate limiting` | This is a server-side concern, not a UI constraint |
| **Decision** — "When the user clicks delete, ask for confirmation" | This is a Decision (user-facing branch at a moment), not a Constraint. Constraint says "disabled when X" (always true); Decision says "if X, then ask Y" (triggered once). |
| **Decision** — "After auth, if success go home; if fail show error" | This is a Decision (branching based on State outcome), not a Constraint. Constraints are persistent rules; Decisions are one-time flow branches. |

## Constraint vs Decision (boundary clarification)

| | Constraint | Decision |
|---|-----------|----------|
| **Persistent?** | Always true while condition holds | Triggered once at a specific moment |
| **Effect** | Hides, disables, or validates an element | Branches user flow to different paths |
| **Example** | "Delete button is disabled when no items selected" | "After user clicks delete, ask for confirmation" |
| **Example** | "This input is hidden when account-type != business" | "If auth succeeds → go home; if fails → show error" |

## Design Rule

> "If I need to explain this rule to a business analyst, does it make sense without mentioning the UI?"
> If yes → it's a Constraint. If no → you're describing a UI implementation detail.

## Related Concepts

- **Input**: Inputs obey Constraints for validation
- **Action**: Actions obey Constraints for availability
- **State**: States are influenced by Constraints
- **Decision**: Decisions often evaluate Constraints to determine branching
- **Capability**: Capabilities obey Constraints as a whole
