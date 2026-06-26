# Feedback（反馈）

## Definition
Information communicated to the user about the result of an Action or State change.
Feedback answers the question: **"What does the user need to know about what just happened?"**

Feedback is the system's voice. It confirms success, explains failure, warns of consequences,
or provides guidance. Feedback is always about *communication*, not about *layout*.
The same Feedback (`submission-failed`) may render as a toast, a banner, an inline message,
a modal, or a spoken alert — the *message* is the same.

## Relationship

```
Action
  └─ produces → Feedback
                  ├─ triggered-by → State       (what state causes this feedback)
                  ├─ obeys → Constraint         (when feedback is shown)
                  └─ may-lead-to → Decision     (what the user does after seeing feedback)
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name (e.g., `auth-failed-message`, `save-success-toast`) |
| `kind` | FeedbackKind | The semantic type of feedback |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `message` | string | The content communicated to the user |
| `severity` | Severity | `success`, `error`, `warning`, `info` |
| `duration` | Duration | How long feedback persists (`transient`, `sticky`, `persistent`) |
| `placement` | Placement | Where feedback appears (`inline`, `page-top`, `overlay`, `target-proximity`) |
| `action` | Action | An optional action the user can take in response |
| `visible-when` | Condition | When this feedback is shown |

## Feedback Kinds

| Kind | Description | Typical duration |
|------|-------------|------------------|
| `confirmation` | Action completed successfully | `transient` |
| `error-message` | Action failed; explains why | `sticky` |
| `warning-notice` | Action succeeded but with caveats | `sticky` |
| `info-notice` | Neutral information for awareness | `transient` |
| `validation-error` | Input-level input error | `sticky` (until corrected) |
| `empty-state` | No data to display; guidance on next steps | `persistent` (until data exists) |
| `progress` | Ongoing operation progress | `persistent` (until complete) |
| `inline-help` | Contextual guidance or explanation | `persistent` |

## Severity Levels

| Severity | Typical treatment | Examples |
|----------|-------------------|----------|
| `success` | Green, positive icon | "Project saved successfully" |
| `error` | Red, alert icon | "Authentication failed: invalid credentials" |
| `warning` | Yellow/amber, caution icon | "Deleting this project will also remove all execution history" |
| `info` | Blue/neutral, info icon | "This action may take a few minutes" |

## Duration

| Duration | Behavior | Use case |
|----------|----------|----------|
| `transient` | Auto-dismiss after a few seconds | Success confirmation |
| `sticky` | Visible until user dismisses | Error messages, warnings |
| `persistent` | Always visible while condition is true | Empty states, progress bars, inline help |

## Placement

| Placement | Description |
|-----------|-------------|
| `inline` | Within the natural flow of content, near related elements |
| `page-top` | At the top of the page or section (banner) |
| `overlay` | Floating above content (toast, snackbar, notification) |
| `target-proximity` | Adjacent to the element that caused it (requirement-level error) |

## Examples

| Feedback | Kind | Severity | Duration |
|----------|------|----------|----------|
| `auth-failed` | `error-message` | `error` | `sticky` |
| `save-success` | `confirmation` | `success` | `transient` |
| `delete-warning` | `warning-notice` | `warning` | `sticky` |
| `no-projects` | `empty-state` | `info` | `persistent` |
| `upload-progress` | `progress` | `info` | `persistent` |
| `dependency-impact` | `inline-help` | `warning` | `persistent` |
| `network-offline` | `error-message` | `error` | `persistent` |
| `clone-source-summary` | `inline-help` | `info` | `persistent` |
| `validation-email-format` | `validation-error` | `error` | `sticky` |

## Counter Examples

These are **NOT** Feedback — they are other concepts:

| What | Why it's not Feedback |
|------|----------------------|
| `Toast component` | This is a UI component; Feedback is the *message* it contains |
| `Snackbar` | This is a Material Design component name |
| `Alert` | This is a Bootstrap/component name |
| `console.log` | This is a developer tool, not user-facing communication |
| `HTTP status code` | This is a protocol detail; Feedback is the user-facing message |
| `try/catch` | This is error handling code, not user communication |
| `Notification badge` | This is a visual indicator of count; the *message* is the Feedback |
| `Modal dialog` | This is a Section pattern; Feedback may be presented *inside* it |

## Design Rule

> "If I read this message aloud to a user who cannot see the screen, does it still make sense?"
> If yes → it's Feedback. If it relies on visual context → you're describing UI chrome, not communication.

## Feedback vs State

A common confusion. The distinction:

| Concept | Question | Example |
|---------|----------|---------|
| **State** | What is happening? | `error: auth-failed` |
| **Feedback** | What does the user need to know? | "The email or password you entered is incorrect" |

States are *conditions*. Feedback is *communication about conditions*.

## Related Concepts

- **Action**: Actions produce Feedback
- **State**: States trigger Feedback
- **Constraint**: Feedback visibility is governed by Constraints
- **Decision**: Feedback may offer actions that lead to Decisions
