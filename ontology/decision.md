# Decision（决策）

## Definition
A branch point where the system chooses a path based on State, Data, or user choice.
A Decision answers the question: **"What happens next, and why?"**

A Decision represents a moment of branching logic in the user flow. It is the "if-then" of the UI.
Unlike an Action (which the user initiates), a Decision can be automatic (system-directed) or
choice-based (user selects from options). Decisions make the Agent understand *conditional
flow* — what paths exist and what conditions trigger each path.

## Relationship

```
Capability
  └─ explains → Decision
                  ├─ evaluates → State         (what state(s) inform this decision)
                  ├─ evaluates → Data           (what data informs this decision)
                  ├─ resolves-to → Navigation   (where the user goes)
                  ├─ resolves-to → State        (what state results)
                  └─ evaluates → Constraint     (what rules apply)
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name (e.g., `auth-outcome`, `delete-confirmation-result`) |
| `description` | string | Human-readable explanation of what is being decided |
| `branches` | Branch[] | The possible outcomes of this decision |

## Branch Properties

| Property | Type | Description |
|----------|------|-------------|
| `condition` | Condition | When this branch is taken (e.g., `auth-state == authenticated`) |
| `resolves-to` | Reference | What this branch leads to (Navigation target, State, Action) |
| `label` | string | Human-readable description of this path |
| `priority` | Priority | Which branch to prefer when multiple conditions match |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `trigger` | TriggerType | What initiates this decision (`automatic`, `user-choice`, `time-based`) |
| `default-branch` | Branch | The fallback branch when no conditions match |

## Trigger Types

| Trigger | Description | Example |
|---------|-------------|---------|
| `automatic` | System decides based on State/Data | Auth success → navigate home |
| `user-choice` | User explicitly selects a path | "Save" vs "Discard" dialog |
| `time-based` | Decision after a timeout | Session expiry → redirect to login |
| `event-based` | Triggered by an external event | WebSocket disconnect → show offline state |

## Branch Conditions

```yaml
branches:
  - condition: "auth-state == authenticated"
    resolves-to: "home"
    label: "User is signed in"

  - condition: "auth-state == auth-failed"
    resolves-to: "auth-failed-feedback"
    label: "Credentials rejected"

  - condition: "auth-state == locked-out"
    resolves-to: "account-locked-feedback"
    label: "Too many attempts"

  - condition: "network == offline"
    resolves-to: "offline-feedback"
    label: "No network connection"
```

## Examples

| Decision | Description | Branches |
|----------|-------------|----------|
| `auth-outcome` | What happens after authentication attempt | `authenticated → home`, `auth-failed → error`, `locked-out → recovery` |
| `delete-confirmation` | User confirms or cancels deletion | `confirmed → delete-execute`, `cancelled → dismiss-dialog` |
| `empty-collection` | What to show when list has no items | `can-create → empty-state-with-cta`, `cannot-create → read-only-empty-state` |
| `session-expiry` | What happens when session expires | `has-unsaved → save-prompt`, `no-unsaved → redirect-to-login` |
| `file-too-large` | What happens when upload exceeds limit | `can-compress → offer-compression`, `cannot-compress → error-feedback` |
| `form-dirty-navigate` | User tries to leave with unsaved changes | `confirm → save-then-navigate`, `discard → navigate`, `cancel → stay` |

## Counter Examples

These are **NOT** Decisions — they are other concepts:

| What | Why it's not a Decision |
|------|------------------------|
| `if/else statement` | This is a programming construct, not a semantic decision |
| `react-router` | This is a routing library; Navigation is the target, Decision is the branching |
| `switch case` | This is a control flow construct |
| `redirect` | This is an HTTP concept; Navigation is the outcome |
| `conditional rendering` | This is a React pattern; Constraint handles visibility |
| `A/B test` | This is a product experiment, not a user flow decision |
| `feature flag` | This is a deployment concern, not a user flow concern |
| `error boundary` | This is a React error handling component |
| **Constraint** — "This button is disabled when no items are selected" | This is a Constraint (persistent rule, always true), not a Decision. Decision is triggered at a moment; Constraint is always active while the condition holds. |
| **Constraint** — "This field is hidden when account-type != business" | This is a Constraint (visibility rule), not a Decision. There is no branching to different paths; there is one conditional rule that persists. |

## Design Rule

> "Can I draw this as a flowchart on a whiteboard without mentioning any technology?"
> If yes → it's a Decision. If the flowchart requires terms like "component", "route", or "render"
> → you're describing implementation, not user flow.

## Decision vs Constraint (boundary clarification)

| | Decision | Constraint |
|---|----------|-----------|
| **Persistence** | Triggered once at a specific moment | Always true while condition holds |
| **Effect** | Branches user flow to different paths | Hides, disables, or validates an element |
| **Example** | "After delete click, ask 'Are you sure?'" | "Delete button disabled when no items selected" |
| **Example** | "If auth succeeds → home; if fails → error" | "This field hidden when account-type != business" |

## Decision vs Action vs State

A critical distinction for Agent understanding:

| Concept | Question | Who initiates |
|---------|----------|---------------|
| **Action** | What can the user do? | User |
| **State** | What is happening? | System or Action |
| **Decision** | What happens next? | System or User |
| **Constraint** | Under what conditions? | Always active rule |

Example flow:
```
Action: user clicks "Delete"
  → State: "confirming-delete"
  → Decision: "delete-confirmation"
      → Branch: user confirms → Action: "execute-delete"
      → Branch: user cancels → State: "idle"

Constraint (separate, persistent):
  "Delete button is disabled when items.length == 0"
```

## Related Concepts

- **Capability**: Decisions explain the branching logic within a Capability
- **State**: Decisions evaluate States to determine branches
- **Navigation**: Decisions resolve to Navigation targets
- **Constraint**: Decisions evaluate Constraints
- **Action**: Actions may trigger Decisions
- **Feedback**: Feedback may offer choices that lead to Decisions
