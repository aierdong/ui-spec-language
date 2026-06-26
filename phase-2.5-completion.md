# Phase 2.5 — Normal Forms: Completion Report

## What was done

Established Normal Forms for the UISL project — a system of canonical YAML representations ensuring that every semantic entity has exactly ONE valid expression form, eliminating Agent reasoning anomalies caused by multiple equivalent but syntactically different YAML shapes.

## Deliverables

Created `normal-forms/` directory with 12 files:

| File | Purpose |
|------|---------|
| `README.md` | Core rules, equivalence mapping reference table, Agent decision tree |
| `page.nf.yaml` | Page canonical form + route/component → page mapping |
| `capability.nf.yaml` | Capability canonical form + feature/operation → capability mapping |
| `input.nf.yaml` | Input canonical form + widget/HTML → InputKind mapping |
| `action.nf.yaml` | Action canonical form + button/handler → intent mapping |
| `section.nf.yaml` | Section canonical form + component → layout-pattern mapping |
| `state.nf.yaml` | State canonical form + boolean-flag → state mapping |
| `feedback.nf.yaml` | Feedback canonical form + toast/alert → feedback-kind mapping |
| `navigation.nf.yaml` | Navigation canonical form + router/link → method mapping |
| `constraint.nf.yaml` | Constraint canonical form + HTML-attribute → condition mapping |
| `decision.nf.yaml` | Decision canonical form + if-else/switch → branches mapping |
| `data.nf.yaml` | Data canonical form + fetch/store → source mapping |

Each file contains: canonical YAML shape, property canonical names (with aliases), equivalence mappings (non-canonical → canonical), false friends (look-alike but NOT equivalent), and agent instructions.

## Key design decisions

1. **5 Core Rules**: One Canonical Form per entity, Equivalence Mapping (read-side tolerance), Property Names are Canonical, Structure is Canonical, Value Types are Canonical
2. **Agent Decision Tree**: PARSE → CLASSIFY (via Taxonomy aliases) → STRUCTURE (map to canonical nesting) → VALIDATE (check NF rules) → OUTPUT (emit only canonical)
3. **False Friends**: Explicitly documented 24+ cases where expressions look similar but are NOT semantically equivalent across all concepts
4. **Agent Instructions**: Each NF file ends with precise instructions for the Agent on how to generate canonical output

## Audit findings from Phase 0/1/2

All 5 issues found during review have been fixed:

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | GoToHome carries-state → Data instead of State | Medium | ✅ Changed to `State: Outcome.Success`; Data ref moved to `carry-data` |
| 2 | page.taxonomy.yaml missing | Low (intentional) | ✅ Documented in taxonomy/README.md |
| 3 | ad-hoc properties (instant, blocking, needs) | Low | ✅ Documented in taxonomy file headers + README; `needs` → `requires` |
| 4 | capability feedback non-standard structure | Low | ✅ Normalized to structured `{kind, severity, duration, placement}` |
| 5 | Export/Navigate dual identity unclear | Low | ✅ Added "Dual-Identity Concepts" section in taxonomy/README.md |

## Next steps

- Phase 3: Formalize Relationships between concepts
- Phase 4: Design Canonical Schema (YAML structure)
- Phase 5: Build Vocabulary Registry (enforce NFs at registry entry)
