# Section（分区）

## Definition
A physical or logical partition of a Page that groups related Capabilities.
A Section answers the question: **"How are the page's functions organized spatially or logically?"**

A Section is a container. It does not perform functions — it arranges them.
It may have a visual identity (header, footer, sidebar, main) but its defining characteristic
is that it groups Capabilities into a coherent unit.

## Relationship

```
Page
  └─ contains → Section
                  ├─ contains → Capability
                  ├─ sections → Section       (nested sections)
                  └─ obeys → Constraint
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name within this page (e.g., `sidebar`, `main-content`) |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `label` | string | Human-readable name (e.g., "Navigation Hub", "Main Workspace") |
| `contains` | Capability[] | Capabilities grouped within this section |
| `sections` | Section[] | Nested Sections when spatial partitioning is hierarchical |
| `layout-pattern` | LayoutPattern | Semantic layout intent (e.g., `centered-column`, `sidebar-shell`, `split-screen`, `vertical-stack`, `grid`) |
| `zones` | Zone[] | Named sub-areas within the section (e.g., `top`, `middle`, `bottom`) |
| `static` | boolean | Whether the section's content is non-interactive decoration (e.g., marketing copy) |
| `priority` | Priority | Visual emphasis relative to sibling sections (`primary`, `secondary`, `tertiary`) |

## Layout Patterns (semantic, not CSS)

| Pattern | Intent |
|---------|--------|
| `centered-column` | Focused, single-task flow (auth, onboarding, confirmation) |
| `sidebar-shell` | Persistent navigation + mutable content area |
| `split-screen` | Two equal-weight content areas (e.g., form + marketing) |
| `vertical-stack` | Top-to-bottom list of items (feeds, lists, settings) |
| `horizontal-strip` | Left-to-right arrangement (toolbars, breadcrumbs, tabs) |
| `grid` | Equal-weight cards or items in rows and columns |
| `overlay` | Content floating above the main page (dialogs, drawers, modals) |
| `master-detail` | List on one side, detail view on the other |

## Examples

| Section | Description |
|---------|-------------|
| `navigation-hub` | Persistent sidebar or top bar with navigation links and brand identity |
| `global-header` | Top bar with app-wide controls (theme, language, settings, user menu) |
| `credential-entry` | Centered form where user provides identity credentials |
| `marketing-panel` | Non-interactive area with product copy, illustrations, or testimonials |
| `entity-list` | A list or grid of records the user can browse, select, and act on |
| `detail-panel` | Detailed view of a single selected record |
| `action-bar` | Horizontal strip of primary and secondary actions for the current context |
| `filter-panel` | Sidebar or collapsible area with filtering controls |
| `empty-state-area` | Placeholder shown when a list or view has no data |

## Counter Examples

These are **NOT** Sections — they belong to other concepts:

| What | Why it's not a Section |
|------|------------------------|
| `Authentication` | This is a Capability that a Section contains |
| `Submit` | This is an Action, not a container |
| `Email Input` | This is an Input, not a container |
| `Loading` | This is a State, not a spatial partition |
| `div` | This is an HTML element, not a semantic concept |
| `flex-container` | This is a CSS layout mode, not a semantic partition |
| `button-group` | This is a grouping of Actions within a Section, not a Section itself |
| `toast-container` | This is a Feedback presentation area within a Section |

## Nested Sections

A Section may contain child Sections through the `sections` property when the spatial partition is hierarchical. The `contains` property is reserved for Capability references:

```
Section: workspace
  ├─ Section: toolbar
  ├─ Section: canvas
  └─ Section: properties-panel
```

## Design Rule

> "If I remove this area from the page, does the page still make sense?"
> If yes → it's a Section. If the page becomes non-functional → you might be confusing Section with Capability.

> "Can I rearrange this area to a different part of the page without breaking its content?"
> If yes → it's a Section.

## Abstraction Level

Section is **one level closer to layout** than Capability. It may describe spatial relationships
(floating, sliding, stacking, zoning) that Capability never describes. This is intentional:
Section's purpose IS to express where things go. The boundary is:

| Section may say | Section may NOT say |
|----------------|---------------------|
| "This content floats above the page" (Overlay) | "Use a div with z-index: 1000" |
| "This appears from the right edge" (origin: right) | "transform: translateX(100%)" |
| "This has three zones: header, body, footer" | "Use flexbox with these CSS classes" |
| "User can dismiss this by clicking outside" (dismissable: true) | "Add click event listener to backdrop" |

Sections use semantic naming for spatial patterns (FocusOverlay, SideOverlay, ContextualMenu),
not implementation names (ModalDialog, Drawer, DropdownMenu).

## Related Concepts

- **Page**: Sections partition a Page
- **Capability**: Sections contain Capabilities
- **Constraint**: Sections can have constraints (e.g., visible only to certain roles)
- **Navigation**: Sections can be navigation targets (scroll-to, tab-switch)
