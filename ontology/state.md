# State（状态）

## Definition
A transient condition of the UI at a given moment.
A State answers the question: **"What is happening right now?"**

A State is not data — it's a *condition* that the UI is in. It may be triggered by an Action,
produced by a Capability, or arise from external events. States are always named after the condition,
not after the visual representation.

## Relationship

```
Capability
  └─ produces → State
                  ├─ is-triggered-by → Action
                  ├─ may-lead-to → Decision
                  ├─ may-lead-to → Navigation
                  └─ may-trigger → Feedback
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name (e.g., `loading`, `empty`, `error`, `selected`) |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `label` | string | Human-readable name (e.g., "Loading", "No Results", "Submission Failed") |
| `values` | string[] | Enumerated possible values (e.g., `[success, failed, partial-failed]`) |
| `default` | string | The initial value when the page or component mounts |
| `persistent` | boolean | Whether this state survives page navigation (default: `false`) |
| `visible-when` | Condition | When this state is shown to the user |
| `message` | string | Human-readable description of the state for the user |
| `source` | string | What triggers this state (`internal`, `external`, `user-action`) |

## Common States (universal, platform-independent)

| State | Description | Typical trigger |
|-------|-------------|-----------------|
| `loading` | Data or content is being fetched | Page mount, Action triggered |
| `empty` | A collection or view has no items to display | Data source returns zero results |
| `error` | An operation failed | API error, network failure, validation failure |
| `success` | An operation completed successfully | Action completed |
| `idle` | Normal, interactive state (default) | Page mount, Action completed |
| `selected` | One or more items are selected | User selects an item |
| `expanded` | Detail content is revealed | User expands a row or section |
| `focused` | An element has input focus | User tabs or clicks into a field |
| `disabled` | An element is not interactive | Constraint applied |
| `processing` | An operation is in progress | Action triggered, awaiting result |
| `validating` | Input is being checked | Input value changed |

## Examples

| State | Context |
|-------|---------|
| `auth-failed` | Authentication Capability: credentials were rejected |
| `no-search-results` | Search Capability: query returned zero matches |
| `uploading` | Upload Capability: file transfer in progress |
| `out-of-stock` | Commerce Capability: item cannot be purchased |
| `offline` | System-level: network unavailable |
| `dialog-mode: create` | CRUD Capability: modal dialog is in create mode |
| `active-sub-tab: constraints` | Detail Section: the "constraints" tab is active |

## Counter Examples

These are **NOT** States — they are other concepts:

| What | Why it's not a State |
|------|----------------------|
| `spinner` | This is a visual representation of `loading` |
| `skeleton screen` | This is a visual representation of `loading` |
| `red border` | This is a visual representation of `error` |
| `toast message` | This is Feedback, not the State itself |
| `isLoading = true` | This is the *value* of a State, not the State concept |
| `useState(false)` | This is a React hook, not a semantic State |
| `HTTP 500` | This is an error code, but `error` is the State |
| `undefined` | This is a JavaScript value, not a semantic condition |
| `setLoading(true)` | This is a state mutation function, not a State |

## State Groups (semantic categories)

| Group | States | Description |
|-------|--------|-------------|
| **Lifecycle** | `idle`, `loading`, `ready`, `processing` | Where the Capability is in its execution lifecycle |
| **Outcome** | `success`, `error`, `partial-success`, `timeout` | Result of an Action |
| **Selection** | `unselected`, `selected`, `multi-selected`, `all-selected` | What items are chosen |
| **Availability** | `enabled`, `disabled`, `locked`, `expired` | Whether an item can be interacted with |
| **Visibility** | `visible`, `hidden`, `collapsed`, `expanded` | Whether content is shown |
| **Network** | `online`, `offline`, `reconnecting`, `slow-connection` | Connection quality |
| **Validation** | `valid`, `invalid`, `validating`, `pristine`, `dirty` | Form field state |

## Design Rule

> "If I remove all CSS and icons, can I still describe this condition in words?"
> If yes → it's a State. If no → you're describing visual decoration.

## Related Concepts

- **Action**: Actions trigger State transitions
- **Decision**: States inform Decisions (if `auth-failed` → show error; if `authenticated` → navigate home)
- **Feedback**: States may trigger Feedback (e.g., `error` → error message)
- **Constraint**: States can be constrained (e.g., `disabled` when condition is met)
- **Capability**: Capabilities produce States
