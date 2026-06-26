# Page（页面）

## Definition
A single screen in the application's navigation map — the smallest complete unit visible to the user at one time.
A Page answers the question: **"What screen is the user looking at right now?"**

A Page is the root container of the UI Spec. It is the target of Navigation events and the source of
further Navigation. It is NOT a route, NOT a URL pattern, NOT a component — it is a semantic unit
of the user's experience. The same Page may appear at different routes (e.g., `/projects/:id` and
`/projects/:id?tab=history` are the same Page).

## Relationship

```
Application
  └─ maps-to → Page
                  ├─ contains → Section        (what regions make up this screen)
                  ├─ in-navigation → Navigation (how the user gets to this page)
                  └─ out-navigation → Navigation (where the user can go from here)

Navigation
  └─ target → Page        (Pages are the destinations of navigation)
  └─ source → Page        (Pages are the starting points of navigation)
```

Pages are connected by Navigation into an application map:

```
Page: login
  ├─ out → push → Page: home          (after successful auth)
  └─ out → external → OAuth provider  (Google/GitHub SSO)

Page: home
  ├─ in ← replace ← Page: login        (arriving after auth)
  ├─ out → push → Page: schema-browser
  ├─ out → push → Page: projects
  └─ out → push → Page: settings
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name within the application (e.g., `login`, `home`, `projects`) |
| `label` | string | Human-readable name (e.g., "Sign In", "Dashboard", "Projects") |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `purpose` | string | High-level purpose of this page in the user journey (e.g., "entry-point", "workspace", "settings") |
| `sections` | Section[] | The Sections that partition this page |
| `navigation-in` | Navigation[] | How users arrive at this page |
| `navigation-out` | Navigation[] | Where users can go from this page |
| `layout` | PageLayout | The overall page-level layout pattern (semantic, not CSS) |
| `requires-auth` | boolean | Whether the user must be authenticated to access this page |
| `guarded-by` | Constraint[] | Constraints that gate access to this page |

## Page Layouts (semantic, not CSS)

| Layout | Intent | Example |
|--------|--------|---------|
| `sidebar-shell` | Persistent navigation sidebar + mutable content area | Admin panels, project management |
| `split-screen` | Two equal panels side by side | Auth page (form + marketing) |
| `centered-column` | Single focused column | Login, onboarding, confirmation |
| `full-canvas` | Content fills the entire viewport | Dashboards, maps, canvas editors |
| `master-detail` | List panel + detail panel | Email, file browser |
| `stacked` | Content stacked vertically (mobile adaptation) | Mobile-first layouts |

## Examples

| Page | Purpose | Layout | Sections |
|------|---------|--------|----------|
| `login` | Identity verification entry point | `split-screen` | credential-entry, marketing-panel |
| `home` | Application landing page | `sidebar-shell` | navigation-hub, dashboard-grid |
| `projects` | Project management workspace | `sidebar-shell` | navigation-hub, global-header, entity-list |
| `schema-browser` | Database schema exploration | `sidebar-shell` | navigation-hub, global-header, tree-view, detail-panel |
| `settings` | Application configuration | `sidebar-shell` | navigation-hub, settings-form |
| `onboarding` | First-time user setup | `centered-column` | progress-indicator, onboarding-step |

## Counter Examples

These are **NOT** Pages — they are other concepts:

| What | Why it's not a Page |
|------|----------------------|
| `/projects/:id` (URL path) | This is a route pattern; multiple routes can map to one Page |
| `Modal Dialog` | This is a Section (Overlay) within a Page, not a standalone Page |
| `Tab Panel` | This is a Section within a Page, not a standalone Page |
| `Component` | This is an implementation concept |
| `Layout Component` | This is a rendering wrapper, not a semantic screen |
| `App Shell` | This is the persistent frame that contains Pages (header, sidebar) |
| `Route Config` | This is a routing configuration, not a user-facing screen |

## Design Rule

> "If I draw the application as a map of screens connected by arrows, does this appear as a box on the map?"
> If yes → it's a Page. If it's a sub-region within a box → it's a Section.

## Page vs Route (critical distinction for Agents)

| Concept | Question | Platform Concern |
|---------|----------|------------------|
| **Page** | What screen is the user on? | User experience, application topology |
| **Route** | What URL maps to this Page? | Web routing, deep linking, bookmarkability |

An Agent should define Pages first, then map routes to them. A single Page may be reachable via
multiple routes (e.g., `/projects/:id` and `/projects/:id/edit` both serve the same Page).

## Related Concepts

- **Section**: Pages are partitioned into Sections
- **Navigation**: Pages are the targets and sources of Navigation events
- **Constraint**: Pages can be guarded by Constraints (auth-required, role-based access)
- **State**: Pages may have page-level States (loading, error, offline)
- **Capability**: Pages contain Sections that contain Capabilities
