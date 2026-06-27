# UISL Audit Findings — Phase 0/1/2/2.5 Cross-Review

**Auditor**: Automated cross-layer review
**Date**: 2026-06-27
**Scope**: All files in `ontology/`, `taxonomy/`, `normal-forms/`, `overview.md`, `phase-2.5-completion.md`

---

## Legend

| Severity | Meaning |
|----------|---------|
| **HIGH** | Semantic error, contradiction between layers, or Agent will misinterpret |
| **MEDIUM** | Inconsistency that degrades quality but won't cause outright failure |
| **LOW** | Cosmetic, documentation, or minor polish issue |

---

## 1. HIGH — Property name `description` vs `intent` / `summary` (Ontology vs NF)

**Files**: `ontology/capability.md`, `ontology/decision.md`, `normal-forms/capability.nf.yaml`, `normal-forms/decision.nf.yaml`

The NF files silently renamed ontology properties without documenting the change:

| Ontology Property | NF Property | Used In |
|-------------------|-------------|---------|
| `description` (required) | `intent` (required) | Capability |
| `description` (required) | `summary` (required) | Decision |

**Impact**: An Agent reading both ontology and NF sees contradictory required properties. The ontology says Capability requires `description`; the NF says `intent`. There is no explicit mapping or alias linking these.

**Fix options**:
- (A) Update ontology files to use `intent` / `summary`, OR
- (B) Add `description` as an explicit alias for `intent` / `summary` in the NF `property-canonical-names` section, OR
- (C) Add a "Migrated Properties" section to each NF documenting what changed from the ontology.

---

## 2. HIGH — `label` required in ontology, optional in NF

**Files**: `ontology/capability.md`, `ontology/decision.md`, `normal-forms/capability.nf.yaml`, `normal-forms/decision.nf.yaml`, `normal-forms/README.md`

| Concept | Ontology | NF README Rule 7 |
|---------|----------|-------------------|
| Capability | `label` required | `label` not listed as required |
| Decision | `description` required | `summary` required (different name!) |
| Action | `label` not required in ontology | `label` required in NF README |

This is a direct contradiction. Agents following the ontology will generate `label` as mandatory; Agents following the NF will not.

---

## 3. HIGH — Missing `taxonomy/README.md` was actually present (completion report accuracy)

**File**: `phase-2.5-completion.md`

The completion report states: "issue 2: page.taxonomy.yaml missing — Low (intentional) — Documented in taxonomy/README.md." This is accurate — the file does exist. No action needed, but the report's framing suggests this was a *fix* when it was only *documented*.

---

## 4. HIGH — Ad-hoc taxonomy properties still lack canonical form definitions

**Files**: `taxonomy/*.taxonomy.yaml`, `taxonomy/README.md`, `normal-forms/README.md`

The taxonomy uses properties not defined in any ontology or NF:

| Property | Used In | Status |
|----------|---------|--------|
| `instant` | capability, action | Documented in taxonomy/README.md as extension |
| `blocking` | action, state, feedback | Documented in taxonomy/README.md |
| `opens` | action | Documented in taxonomy/README.md |
| `pre-populates` | action | Documented in taxonomy/README.md |
| `preserves-state` | navigation | Documented in taxonomy/README.md |
| `blocks-background` | section, navigation | Documented in taxonomy/README.md |
| `collapsible` | section | NOT documented anywhere |
| `animated` | navigation | NOT documented anywhere |
| `clears-session` | action, navigation | NOT documented anywhere |
| `modifies-data` | action | NOT documented anywhere |
| `discards-changes` | action, navigation | NOT documented anywhere |
| `triggers-download` | action | NOT documented anywhere |
| `short-lived` | input | NOT documented anywhere |

**Impact**: Agents generating taxonomy-aware specs encounter properties with no canonical form or mapping rules. The documented properties (`instant`, `blocking`, etc.) have no equivalence mapping in NF files, so they are "invisible" to the NF Agent Decision Tree.

**Fix**: Either:
- (A) Add these to the relevant NF files as canonical properties with equivalences, OR
- (B) Add a "Taxonomy Extension Properties" section in each NF file mapping them, OR
- (C) Remove them from taxonomy and express the behavior through existing ontology concepts (Constraint, State, Feedback).

---

## 5. HIGH — Section taxonomy uses CSS concepts

**File**: `taxonomy/section.taxonomy.yaml`, line 67

```yaml
- id: CenteredForm
  inherits:
    max-width: narrow
```

`max-width: narrow` is a CSS concept, violating **Principle 1 (Everything is semantic)** and **Principle 2 (Platform independent)**.

**Fix**: Replace with `layout-pattern: centered-column` (which already exists in the same section's taxonomy).

---

## 6. MEDIUM — Section taxonomy attaches Data properties to Sections

**File**: `taxonomy/section.taxonomy.yaml`, lines 77-78, 89-90, 102-103

```yaml
- id: EntityList
  inherits:
    data:
      type: collection
```

Data is a standalone concept consumed by Capability (`consumes → Data`), not attached to Section. The Section ontology has no `data` property. This conflates "what data is displayed" (a Capability concern) with "where it's displayed" (a Section concern).

**Fix**: Move data type hints to the Capability that the Section contains, or add `data` as a documented taxonomy extension property.

---

## 7. MEDIUM — Data NF adds properties not in ontology

**Files**: `ontology/data.md`, `normal-forms/data.nf.yaml`

The NF adds two properties not present in the ontology:
- `maps-to: InputRef[]` — reverse relationship from Data to Input
- `feeds: SectionRef[]` — reverse relationship from Data to Section

These are undocumented additions. The ontology's Data relationship section mentions `maps-to → Input` but does not list it as a property.

---

## 8. MEDIUM — Capability NF adds `layout-pattern` not in ontology

**File**: `normal-forms/capability.nf.yaml`, line 34

The Capability NF includes `layout-pattern: LayoutPattern?` as a property, but the Capability ontology (`ontology/capability.md`) does not list this. It appears in the taxonomy (`capability.taxonomy.yaml`) as an inheritance property.

**Fix**: Either add `layout-pattern` to the Capability ontology as an optional property, or remove it from the NF.

---

## 9. MEDIUM — Action NF adds properties not in ontology

**File**: `normal-forms/action.nf.yaml`

| NF Property | In Ontology? |
|-------------|-------------|
| `sets-mode` | No |
| `keyboard-shortcut` | No |
| `confirmation` | No (only `confirmation` string, not `Confirmation` concept) |

The ontology's Action optional properties include `confirmation` (string), but `sets-mode` and `keyboard-shortcut` are absent.

---

## 10. MEDIUM — Feedback ontology does not list `action` property

**File**: `ontology/feedback.md`, `normal-forms/feedback.nf.yaml`

The NF defines `action: ActionRef?` as an optional property. The ontology's optional properties table does NOT include `action`, though the Relationship section says "Feedback may offer actions that lead to Decisions."

---

## 11. MEDIUM — overview.md Phase 1 example shows only 9 concepts (should be 11)

**File**: `overview.md`, lines 93-104

The Phase 1 example lists 9 concept files. The actual ontology directory has 11 concepts (adds `data.md` and `page.md`). The overview was not updated when these concepts were added.

---

## 12. MEDIUM — `feedback` property name inconsistency across layers

**Files**: `ontology/capability.md`, `taxonomy/capability.taxonomy.yaml`, `normal-forms/capability.nf.yaml`

| Layer | Property Name |
|-------|--------------|
| Ontology (relationship graph) | `triggers → Feedback` |
| Ontology (optional properties) | `feeds-back` |
| Taxonomy | `feedback:` |
| NF | `feedback:` |

The ontology uses `feeds-back` as the property name, but both taxonomy and NF use `feedback`. The relationship graph uses `triggers`. Three different names for the same relationship.

---

## 13. MEDIUM — Decision taxonomy uses `description` but NF uses `summary`

**Files**: `taxonomy/decision.taxonomy.yaml`, `normal-forms/decision.nf.yaml`

The taxonomy uses `description` (matching the ontology), but the NF canonical form uses `summary`. Agents reading taxonomy and outputting NF will see this mismatch.

---

## 14. MEDIUM — Capability NF Rule 7 lists different required properties than ontology

**File**: `normal-forms/README.md`, Rule 7 table

| Concept | NF Rule 7 Says | Ontology Says |
|---------|---------------|---------------|
| Capability | `id`, `intent` | `id`, `label`, `description` |
| Action | `id`, `intent`, `label` | `id`, `intent` |
| Section | `id` | `id`, `label` |
| State | `id` | `id`, `label` |

These are meaningful differences that will cause Agent confusion.

---

## 15. LOW — `search` exists as both Capability and Action

**Files**: `taxonomy/capability.taxonomy.yaml`, `taxonomy/action.taxonomy.yaml`

The dual-identity is documented in `taxonomy/README.md` ("Dual-Identity Concepts"). No fix needed, but Agents must be instructed to use context to disambiguate.

---

## 16. LOW — Feedback taxonomy uses "requirement" terminology

**File**: `taxonomy/feedback.taxonomy.yaml`, line 168

```yaml
description: "Feedback about requirement validation"
```

The project uses "Input" everywhere else, not "requirement." Minor terminology drift.

---

## 17. LOW — Navigation NF false friends: `method: push` looks like `method: replace`

**File**: `normal-forms/navigation.nf.yaml`, lines 176-178

This entry describes a distinction (push vs replace) rather than a false friend (two different expressions that look the same). It doesn't fit the false-friends pattern of the other NF files.

---

## 18. LOW — Missing `taxonomy/README.md` entry for `collapsible`, `animated`, `clears-session`

**File**: `taxonomy/README.md`

The "Taxonomy-Specific Properties" table documents 7 extension properties but misses at least 6 more used in taxonomy files (see Finding #4).

---

## Summary

| Severity | Count |
|----------|-------|
| HIGH | 4 |
| MEDIUM | 10 |
| LOW | 4 |
| **Total** | **18** |

### Priority Fix Order

1. **Property name alignment** (Findings #1, #2, #14) — Resolve `description` vs `intent`/`summary` and `label` required status across all layers
2. **Ad-hoc property formalization** (Findings #4, #18) — Either add to ontology/NF or remove from taxonomy
3. **CSS concept removal** (Finding #5) — Replace `max-width: narrow` with semantic alternative
4. **Data attachment on Section** (Finding #6) — Clarify whether Section can own data hints
5. **NF property additions** (Findings #7, #8, #9, #10) — Either add to ontology or document as NF extensions
6. **overview.md update** (Finding #11) — Add Data and Page to Phase 1 example
