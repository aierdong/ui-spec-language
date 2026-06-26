# Navigation（导航）

## Definition
A movement between Pages, Sections, or Capabilities within an application.
Navigation answers the question: **"How does the user get from here to there?"**

Navigation describes the topology of the application — the map of where users can go
and how they get there. It is not about tabs, links, or menus (those are rendering choices).
Navigation is about *destinations* and *transitions*.

## Relationship

```
Action
  └─ may-lead-to → Navigation

Decision
  └─ resolves-to → Navigation

State
  └─ may-lead-to → Navigation

Page
  └─ connected-to → Navigation
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name within the context (e.g., `go-to-home`, `open-project-detail`) |
| `target` | Reference | The destination (Page, Section, Capability, or external URL) |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `method` | NavigationMethod | How the transition happens (`push`, `replace`, `overlay`, `inline`, `scroll-to`) |
| `carry-state` | State[] | Which States to preserve across the navigation |
| `carry-data` | Data[] | Which Data to pass to the target |
| `label` | string | Human-readable name (e.g., "Back to Projects", "View Details") |
| `icon` | string | Semantic icon reference (not a specific icon library name) |
| `back-target` | Reference | Where the user returns to (for push navigation) |
| `is-external` | boolean | Whether the target is outside the application |

## Navigation Methods

| Method | Description | Example |
|--------|-------------|---------|
| `push` | Navigate to a new destination, preserving history (user can go back) | Click project → project detail |
| `replace` | Navigate to a new destination, replacing current in history | After login → redirect to dashboard |
| `overlay` | Open above the current page in a modal/dialog | Click "New Project" → project form dialog |
| `inline` | Expand or switch content within the same page section | Tab switch, accordion expand |
| `scroll-to` | Move to a different position within the same page | "Back to top", anchor links |
| `external` | Navigate to a URL outside the application | "View documentation", OAuth redirect |

## Examples

| Navigation | Target | Method | Description |
|------------|--------|--------|-------------|
| `go-to-home` | `page:home` | `replace` | After successful login, go to home |
| `open-project-detail` | `page:projects?open=detail` | `push` | View a project's details |
| `open-create-dialog` | `capability:project-form` | `overlay` | Open the create project dialog |
| `switch-to-constraints-tab` | `section:constraints-panel` | `inline` | Switch to the constraints sub-tab |
| `back-to-projects` | `page:projects` | `push` | Return to the project list |
| `sign-out-redirect` | `page:login` | `replace` | After sign out, go to login |
| `scroll-to-top` | `section:page-top` | `scroll-to` | Scroll to the top of the current page |
| `oauth-google-redirect` | `https://accounts.google.com` | `external` | Redirect to Google OAuth |

## Counter Examples

These are **NOT** Navigation — they are other concepts:

| What | Why it's not Navigation |
|------|------------------------|
| `<a href>` | This is an HTML mechanism for navigation |
| `<Link to>` | This is a React Router component |
| `react-router` | This is a routing library |
| `pushState` | This is a browser History API method |
| `Tab bar` | This is a rendering pattern; the Navigation is the *transition* between tabs |
| `Breadcrumb` | This is a rendering pattern; the Navigation is the *path* it represents |
| `Sidebar menu` | This is a Section containing Navigation elements |
| `URL path` | This is an addressing scheme; Navigation is the *movement* |
| `redirect(302)` | This is an HTTP status code |

## Navigation Map (the topology)

A key deliverable: the Navigation Map describes the application's connectivity:

```
Page: login
  ├─ [auth success] → replace → Page: home
  └─ [OAuth]        → external → Google/GitHub

Page: home
  ├─ [Schema]       → push → Page: schema-browser
  ├─ [Projects]     → push → Page: projects
  ├─ [Settings]     → push → Page: settings
  └─ [Sign Out]     → replace → Page: login

Page: projects
  ├─ [New Project]  → overlay → dialog: project-form
  ├─ [Edit Project] → overlay → dialog: project-form
  └─ [Run History]  → overlay → dialog: execution-history
```

## Navigation Flow vs Page Route

A critical distinction:

| Concept | Question | Concern |
|---------|----------|---------|
| **Navigation** | How does the user move? | User experience, intent, context |
| **Route** | What URL maps to what? | Technical routing, bookmarkability |

Navigation answers "the user wants to see project details" — the route (`/projects/:id`) is an implementation
detail of how that Navigation is realized on the web.

## Design Rule

> "If I explain this movement to a user without showing them the screen, do they understand where they're going?"
> If yes → it's Navigation. If it requires explaining URLs, routes, or browser mechanics → you're
> describing implementation, not the user's journey.

## Related Concepts

- **Action**: Actions may lead to Navigation
- **Decision**: Decisions resolve to Navigation targets
- **State**: State transitions may trigger Navigation (e.g., `auth-state == authenticated`)
- **Page**: Navigation connects Pages into an application map
- **Section**: Internally, inline Navigation moves between Sections
