# Capability（能力）

## Definition
A user-facing function that the system provides within a specific context.
A Capability answers the question: **"What can the user accomplish on this page?"**

A Capability is always expressed in the user's language, never in implementation terms.

## Relationship

```
Section
  └─ contains → Capability
                  ├─ requires → Input        (what the user must provide)
                  ├─ provides → Action         (what the user can trigger)
                  ├─ produces → State          (what conditions arise)
                  ├─ obeys → Constraint        (what limits apply)
                  ├─ communicates → Feedback   (what the system communicates)
                  ├─ may-lead-to → Decision    (what branch happens next)
                  └─ consumes → Data           (what data it reads)
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique machine-readable name (e.g., `authentication`) |
| `intent` | string | What the user can accomplish |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `label` | string | Human-readable name (e.g., "Sign In") |
| `requires` | Input[] | Inputs the user must provide |
| `provides` | Action[] | Actions the user can trigger |
| `produces` | State[] | States that can arise from this capability |
| `obeys` | Constraint[] | Constraints that limit this capability |
| `communicates` | Feedback[] | Feedback mechanisms available |
| `may-lead-to` | Decision[] | Branch decisions this capability can trigger |
| `consumes` | Data[] | External data this capability reads |

## Examples

| Capability | Description |
|-----------|-------------|
| `authentication` | Verify user identity so they can access the system |
| `search` | Find records by matching criteria |
| `crud` | Create, read, update, delete records |
| `upload` | Transfer files from the user's device to the system |
| `notification` | Alert the user to time-sensitive or relevant events |
| `payment` | Transfer funds from the user to the system |
| `export` | Download data in a portable format |
| `sort` | Reorder a collection by a chosen attribute |
| `filter` | Narrow a collection to items matching criteria |
| `navigate` | Move between application areas or pages |
| `toggle-theme` | Switch between visual presentations (light/dark) |

## Counter Examples

These are **NOT** Capabilities — they are either implementation details or belong to other concepts:

| What | Why it's not a Capability |
|------|---------------------------|
| `Button` | This is an Action trigger, not a Capability |
| `Modal` | This is a Section pattern, not a Capability |
| `Form` | This is a Section pattern that *contains* Capabilities |
| `Text Input` | This is an Input, not a Capability |
| `Loading Spinner` | This is a State representation, not a Capability |
| `Error Message` | This is Feedback, not a Capability |
| `Dropdown` | This is an Input interaction pattern, not a Capability |
| `Data Table` | This is a Section pattern plus Data, not a Capability |
| `Tab Bar` | This is a Navigation element, not a Capability |
| `Checkbox` | This is an Input kind, not a Capability |

## Design Rule

> A test: "Could this exist on a voice interface? On a CLI? On a smartwatch?"
> If yes → Capability. If no → you're describing an implementation detail.

## Related Concepts

- **Section**: A Capability lives inside a Section
- **Input**: What the Capability requires from the user
- **Action**: What the Capability enables the user to do
- **State**: What conditions the Capability can produce
- **Decision**: How the Capability branches to next steps
