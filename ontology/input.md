# Input（输入）

## Definition
A piece of information the user provides to fulfill a Capability.
An Input answers the question: **"What does the user need to tell the system?"**

An Input describes an information need, not an input widget.
The same Input (e.g., `Email`) may render as a text field on web, a voice prompt on smart speaker,
or a gesture on a wearable — but the *information need* is the same.

"Input" is a foundational concept across all computing paradigms: CLI, Web, Voice, VR —
every interface begins with user input. The `kind` property distinguishes what *type* of input.

## Relationship

```
Capability
  └─ requires → Input
                  ├─ obeys → Constraint      (validation, conditional visibility)
                  ├─ maps-to → Data          (what data field it binds to)
                  └─ sources-from → Data     (where selectable values come from)
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name within the Capability (e.g., `email`, `password`) |
| `label` | string | Human-readable name (e.g., "Email Address") |
| `kind` | InputKind | The semantic type of information (e.g., `credential`, `text`, `number`) |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `validation` | Constraint[] | Rules the value must satisfy (required, min-length, format) |
| `default` | any | Default value when the user provides none |
| `placeholder` | string | Example or hint text |
| `help-text` | string | Explanatory text near the input |
| `visible-when` | Condition | When this input is shown (e.g., `"account-type == business"`) |
| `enabled-when` | Condition | When this input is interactive vs read-only |
| `sensitive` | boolean | Whether the value should be masked (passwords, PINs, tokens) |
| `multiple` | boolean | Whether the user can provide multiple values |
| `searchable` | boolean | Whether values are selected from a searchable source |
| `source` | Data reference | Where selectable values come from |
| `maps-to` | Data reference | Which data field this input binds to |

## Input Kinds (semantic, not widget names)

| Kind | Description | Platform examples |
|------|-------------|-------------------|
| `credential` | Identity-verification value (email, password, OTP) | text field, biometric prompt, voice |
| `text` | Free-form short text | input, voice, handwriting |
| `long-text` | Multi-line free-form text | textarea, dictation |
| `number` | Numeric value | stepper, keypad, gesture |
| `boolean` | True/false choice | toggle, checkbox, yes/no prompt |
| `single-select` | Choose one from a list | radio, dropdown, voice menu |
| `multi-select` | Choose multiple from a list | checkboxes, tag selector |
| `date` | Calendar date | date picker, voice ("next Monday") |
| `datetime` | Date and time | datetime picker, voice |
| `duration` | Time span | duration input, voice |
| `file` | User-provided file | file picker, drag-drop, camera |
| `tag-list` | A list of labels or keywords | tag input, chips |
| `display` | Read-only presentation of data | text display, badge, icon |

## Examples

| Input | Kind | Description |
|-------|------|-------------|
| `email` | `credential` | User's email address for identification |
| `password` | `credential` | User's secret for authentication, always `sensitive: true` |
| `otp` | `credential` | One-time passcode, short numeric string |
| `username` | `text` | User-chosen display name or handle |
| `description` | `long-text` | Multi-line free-text description |
| `quantity` | `number` | A numeric quantity (count, amount) |
| `agree-to-terms` | `boolean` | Binary consent |
| `language` | `single-select` | Chosen from a predefined list of languages |
| `table-tags` | `tag-list` | A collection of labels |
| `start-date` | `date` | Calendar date selection |

## Counter Examples

These are **NOT** Inputs — they are implementation details or belong to other concepts:

| What | Why it's not an Input |
|------|----------------------|
| `<input type="text">` | This is an HTML element, not an information need |
| `TextFormField` | This is a Flutter widget class, not a semantic concept |
| `Checkbox` | This is a rendering choice for `kind: boolean` |
| `Radio Group` | This is a rendering choice for `kind: single-select` |
| `Dropdown` | This is a rendering choice for `kind: single-select` |
| `Switch` | This is a rendering choice for `kind: boolean` |
| `Searchable Select` | This is a rendering choice with `searchable: true` |
| `Form Label` | This is a UI element derived from `label` property |
| `Rich Text Editor` | This is a rendering choice for `kind: long-text` |

## Kinds vs Rendering (the mapping the Agent must understand)

```
kind: single-select   →  Web: <select> or radio group
                      →  Mobile: picker wheel
                      →  CLI: numbered menu
                      →  Voice: "Say the number of your choice"

kind: boolean         →  Web: checkbox or toggle switch
                      →  Mobile: switch
                      →  CLI: y/n prompt
                      →  Voice: "Say yes or no"

kind: credential      →  Always: sensitive: true
                      →  Web: type="email" or type="password"
                      →  Mobile: with biometric fallback
```

## Design Rule

> "If I change the platform from Web to CLI, does this still describe what information I need?"
> If yes → it's an Input. If no → you're describing a widget.

## Input vs Constraint

A common confusion. The distinction:

| Concept | Question | Example |
|---------|----------|---------|
| **Input** | What information does the user provide? | "Email address" |
| **Constraint** | What rules apply to that information? | "Must be valid email format" |

Inputs are *what* is needed; Constraints are *rules* that govern them.

## Related Concepts

- **Capability**: Inputs are required by Capabilities
- **Constraint**: Inputs obey constraints (validation, visibility conditions)
- **Data**: Inputs map to and from Data sources
- **Action**: Actions submit, modify, or clear Input values
