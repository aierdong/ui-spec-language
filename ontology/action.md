# Action（动作）

## Definition
A behavior the user can trigger within a Capability.
An Action answers the question: **"What can the user do?"**

An Action describes an intent, not a button. The same Action (e.g., `Submit`) may be triggered
by a button click, a keyboard shortcut, a voice command, or a gesture — the *intent* is the same.

## Relationship

```
Capability
  └─ provides → Action
                  ├─ triggers → State           (what happens after the action)
                  ├─ produces → Feedback        (what the user sees/hears)
                  ├─ may-lead-to → Decision     (branching based on outcome)
                  ├─ may-lead-to → Navigation   (moving to another page)
                  ├─ obeys → Constraint         (when it is available)
                  └─ can-target → Capability    (which capability it affects)
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name within the Capability (e.g., `submit`, `cancel`) |
| `intent` | ActionIntent | What the user intends to accomplish |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `priority` | Priority | Visual emphasis: `primary`, `secondary`, `tertiary`, `destructive` |
| `label` | string | Human-readable text (e.g., "Sign In", "Delete Project") |
| `trigger` | TriggerSource | Where the action originates (`row-body`, `row-action`, `inline`, `toolbar`, `context-menu`) |
| `target` | Reference | Which Capability or UI element this action affects |
| `sets-mode` | string | When this action changes the mode of a target (e.g., `create`, `edit`, `clone`) |
| `navigates-to` | Page reference | Where the user goes after this action |
| `disabled-when` | Condition | When this action cannot be triggered |
| `visible-when` | Condition | When this action is hidden |
| `confirmation` | string | Message shown before executing a destructive action |
| `keyboard-shortcut` | string | Platform-independent shortcut hint |

## Action Priority

| Priority | Meaning | Visual treatment (web example) |
|----------|---------|-------------------------------|
| `primary` | The main action; the most common path | Filled, prominent button |
| `secondary` | Alternative or supporting action | Outlined or text button |
| `tertiary` | Low-emphasis supplementary action | Text link or icon only |
| `destructive` | Action with irreversible consequences | Red/danger styling, often with confirmation |

## Trigger Sources

| Trigger | Meaning |
|---------|---------|
| `row-body` | Triggered by clicking the body of a data row |
| `row-action` | Triggered by a dedicated action button on a data row |
| `inline` | Triggered within the natural flow of content |
| `toolbar` | Triggered from a toolbar or action bar |
| `context-menu` | Triggered from a right-click or long-press menu |
| `global` | Triggered from anywhere on the page (e.g., Ctrl+S) |

## Examples

| Action | Intent | Typical priority |
|--------|--------|------------------|
| `submit` | Finalize and send user input | `primary` |
| `cancel` | Abandon current input without saving | `secondary` |
| `dismiss` | Close an overlay or dialog | `tertiary` |
| `delete` | Permanently remove a record | `destructive` |
| `save` | Persist current changes | `primary` |
| `create` | Open a form to create a new record | `primary` |
| `edit` | Open an existing record for modification | `secondary` |
| `clone` | Create a copy of an existing record | `secondary` |
| `expand` | Reveal hidden detail content | `tertiary` |
| `search` | Execute a search query | `primary` |
| `sort` | Reorder items by a chosen attribute | `secondary` |
| `filter` | Apply filters to a collection | `secondary` |
| `sign-out` | End the current session | `tertiary` |
| `toggle-theme` | Switch between light and dark visual modes | `tertiary` |
| `remove-item` | Remove one item from a collection | `destructive` |

## Counter Examples

These are **NOT** Actions — they are rendering details or belong to other concepts:

| What | Why it's not an Action |
|------|------------------------|
| `<button>` | This is an HTML element, not a user intent |
| `onClick` | This is an event handler, not a user intent |
| `href` | This is an HTML attribute for navigation |
| `Loading` | This is a State that an Action may trigger |
| `Form Submit` | This is an HTML form behavior, not a semantic intent |
| `POST /api/login` | This is an API call, not a user-facing action |
| `Modal Open` | This is a State transition, the Action is what causes it |
| `Redirect` | This is an implementation of Navigation |

## Design Rule

> "If I rename this from 'click the blue button' to 'what the user wants to accomplish', does it still make sense?"
> If yes → it's an Action. If no → you're describing UI chrome.

## Related Concepts

- **Capability**: Actions are provided by Capabilities
- **State**: Actions trigger State transitions
- **Feedback**: Actions produce Feedback
- **Decision**: Actions may lead to Decisions
- **Navigation**: Actions may lead to Navigation
- **Constraint**: Actions obey Constraints (when disabled/hidden)
