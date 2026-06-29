# UI Ontology — Concept Index

This directory defines the **vocabulary of UI** — the concepts an Agent uses to understand and describe user interfaces.
These concepts are platform-independent, semantic, and designed for Agentic Coding consumption.

## Concepts

| # | Concept | Question It Answers | File |
|---|---------|---------------------|------|
| 1 | **Capability** | What can the user accomplish? | [capability.md](capability.md) |
| 2 | **Section** | How are functions partitioned? | [section.md](section.md) |
| 3 | **Input** | What information does the user provide? | [input.md](input.md) |
| 4 | **Action** | What can the user do? | [action.md](action.md) |
| 5 | **State** | What is happening right now? | [state.md](state.md) |
| 6 | **Data** | Where does the information come from? | [data.md](data.md) |
| 7 | **Constraint** | Under what conditions does this apply? | [constraint.md](constraint.md) |
| 8 | **Feedback** | What does the user need to know? | [feedback.md](feedback.md) |
| 9 | **Decision** | What happens next? | [decision.md](decision.md) |
| 10 | **Page** | What screen is the user looking at? | [page.md](page.md) |
| 11 | **Navigation** | How does the user get there? | [navigation.md](navigation.md) |

## Relationship Graph

```
Page
  ├─ contains → Section
  ├─ navigation-in → Navigation
  └─ navigation-out → Navigation
                  ├─ contains → Capability
                  ├─ sections → Section
                  └─ obeys → Constraint
                                  ├─ requires → Input
                                  │              └─ validation → Constraint
                                  ├─ provides → Action
                                  │              ├─ triggers → State
                                  │              └─ obeys → Constraint
                                  ├─ produces → State
                                  ├─ feedback → Feedback
                                  ├─ consumes → Data
                                  ├─ may-lead-to → Decision
                                  │              ├─ evaluates → State/Data/Constraint
                                  │              └─ resolves-to → Navigation/State/Action/Feedback/Page
                                  └─ obeys → Constraint

Navigation connects Pages into an application map through source/target relationships.
```

## Design Principles (from Phase 0)

1. **Everything is semantic** — no `width`, `margin`, `div`
2. **Platform independent** — no `Checkbox`, `Radio`, `Drawer`
3. **Describe intent, not implementation** — `submit-auth` not `button`
4. **Vocabulary first** — concepts before syntax
5. **One concept, one definition** — `authentication` means one thing everywhere

## How to Read a Concept File

Each `.md` file follows this structure:

1. **Definition** — What it is, in one sentence
2. **Relationship** — How it connects to other concepts
3. **Required Properties** — What must be specified
4. **Optional Properties** — What can be specified
5. **Examples** — Real-world instances
6. **Counter Examples** — What it is NOT (boundary definition)
7. **Design Rule** — A test to verify correct usage

## Next Steps

- Phase 4: Design Canonical Schema (YAML structure)
- Phase 5: Build Vocabulary Registry

---

**Version**: 0.1.0-draft
**Status**: Phase 1 — Vocabulary Definition + Phase 2 — Taxonomy + Phase 3 — Relationships Complete
**Last Updated**: 2026-06-27
