# Canonical Schema — Phase 4

## Purpose

The Canonical Schema defines the valid YAML shapes for UISL specs. Every field is derived from one of three Phase 1–3 sources:

| Source | Phase | What it provides |
|---|---|---|
| `normal-forms/required-property-matrix.yaml` | 2.5 | Required properties per concept |
| `relationships/relationship.matrix.yaml` | 3 | Relationship fields (`canonical_property` per relationship) |
| `ontology/*.md` | 1 | Optional properties and concept definitions |

A field exists in the schema **only if** it appears in one of these sources. Nothing is invented.

## Design Decisions (Phase 4)

### Mixed Nesting + References

The spec uses two structural patterns:

1. **Nesting** for spatial containment: `Page → Section → Capability`. This reflects the user's journey through the interface and is the most natural way to read a spec.

2. **Flat references** for cross-cutting concepts: Constraint, Data, and Navigation are defined at the spec root and referenced by `id`. Input, Action, State, Feedback, and Decision may be defined inline within their Capability, or at the spec root for shared reuse.

### Pure Semantic (No Layout)

Per Phase 0 Principles, the canonical schema excludes layout, style, component, and renderer concepts. A `Capability` knows nothing about `flex`, `grid`, `Card`, or `Button`. Those belong to Renderers (Phase 7).

Exception: `Section.layout-pattern` is a semantic partition description (`centered-column`, `sidebar-shell`, `vertical-stack`), not a CSS layout instruction.

### No Component Concept (v1)

The first version has no `components` or `templates`. Every concept stands on its own semantic meaning.

## File Structure

```
schema/
├── README.md              # This file
└── canonical-schema.yaml  # Machine-readable canonical schema
```

## How to Read the Schema

`canonical-schema.yaml` is organized into four sections:

1. **`meta`** — Version and scope
2. **`references`** — How concepts reference each other
3. **`concepts`** — All 11 concept shapes, each with:
   - `source` — Which phases define this shape
   - `required` — Fields from `required-property-matrix.yaml`
   - `optional` — Fields from ontology and NF
   - `relationships` — Fields derived from `relationship.matrix.yaml`, with the `canonical_property` as the YAML key
4. **`spec-structure`** — Top-level spec wrapper shape
5. **`validation`** — Structural and reference integrity rules

## Relationship to Other Phases

```
Phase 1 (Ontology)     → defines what each concept IS
Phase 2 (Taxonomy)     → defines where each concept SITS in the classification tree
Phase 2.5 (Normal Forms) → defines the ONE canonical YAML shape + equivalence mappings
Phase 3 (Relationships)  → defines which concepts may CONNECT and how
Phase 4 (Schema)        → crystallises 1–3 into a formal YAML specification ✅
Phase 5 (Registry)   ✅ → populates the schema with registered vocabulary instances
Phase 6 (Tests)       → validates Agent output against the schema
```

## Design Principles (from Phase 0)

1. Everything is semantic — no CSS, no component names
2. Everything is platform-independent — no React/Flutter/HTML concepts
3. Describe intent, not implementation
4. Vocabulary first, DSL second, Schema third
5. Every concept has one canonical definition

---

**Version**: 0.1.0-draft
**Status**: Phase 4 — Canonical Schema Design (Phase 5 Registry complete)
**Last Updated**: 2026-07-18
