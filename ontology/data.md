# Data（数据）

## Definition
External or internal information that the UI consumes, displays, or mutates.
Data answers the question: **"Where does the information come from?"**

Data is not the view — it's the source of truth. It may come from an API, a database, a file,
a URL parameter, browser storage, or a parent Capability. Data may be read-only or mutable.
The same Data can feed multiple Capabilities and Sections across the application.

## Relationship

```
Capability
  └─ consumes → Data
                  ├─ sourced-from → (API | Database | File | URL | LocalStorage | Parent)
                  ├─ maps-to → Input  (what requirements bind to this data)
                  └─ feeds → Section         (what sections display this data)
```

## Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | identifier | Unique name (e.g., `projects`, `user-profile`, `table-schema`) |
| `source` | SourceType | Where the data originates |

## Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `type` | DataType | The shape of the data (`singleton`, `collection`, `tree`, `stream`) |
| `mutable` | boolean | Whether the user can modify this data (default: `false`) |
| `keyed-by` | string | The field used as a unique identifier for collection items |
| `lazy` | boolean | Whether data is loaded on demand vs eagerly (default: `false`) |
| `freshness` | Freshness | How current the data must be (`realtime`, `near-realtime`, `on-demand`, `cache-tolerant`) |
| `scope` | Scope | Visibility scope (`page`, `section`, `application`, `session`) |

## Source Types

| Source | Description |
|--------|-------------|
| `api` | REST, GraphQL, gRPC endpoint |
| `database` | Direct database query |
| `file` | Uploaded or server-side file |
| `url-parameter` | Query string or path parameter |
| `local-storage` | Browser or device local storage |
| `session-storage` | Temporary session-scoped storage |
| `parent` | Inherited from a parent Capability or Section |
| `context` | Application-wide context (user info, theme, locale) |
| `computed` | Derived from other Data sources |

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| `singleton` | A single record or value | Current user profile |
| `collection` | An ordered or unordered list of records | List of projects |
| `tree` | Hierarchical data with parent-child relationships | File system, org chart |
| `stream` | Continuously updating data | Live log, WebSocket feed |
| `dictionary` | Key-value lookup | Translation strings, config |

## Freshness

| Level | Description | Implementation hint |
|-------|-------------|---------------------|
| `realtime` | Must reflect changes immediately | WebSocket, SSE, polling |
| `near-realtime` | Slight delay is acceptable | Debounced polling, stale-while-revalidate |
| `on-demand` | Loaded when user requests | Fetch on button click or page navigation |
| `cache-tolerant` | Can be served from cache | HTTP cache, localStorage, IndexedDB |

## Scope

| Scope | Description |
|-------|-------------|
| `page` | Data lives only for the current page |
| `section` | Data is scoped to a specific section |
| `application` | Data is shared across the entire application |
| `session` | Data persists for the duration of the user's session |

## Examples

| Data | Source | Type | Mutable |
|------|--------|------|---------|
| `projects` | `api` | `collection` | `true` |
| `table-schema` | `api` | `singleton` | `false` |
| `user-profile` | `context` | `singleton` | `true` |
| `language-preferences` | `local-storage` | `dictionary` | `true` |
| `project-exec-history` | `api` | `collection` | `false` |
| `project-table-configurations` | `parent` | `collection` | `true` |
| `translation-strings` | `file` | `dictionary` | `false` |
| `recent-projects` | `local-storage` | `collection` | `true` |
| `live-log-stream` | `api` | `stream` | `false` |

## Counter Examples

These are **NOT** Data — they are other concepts:

| What | Why it's not Data |
|------|-------------------|
| `useState` | This is a React mechanism for local UI state |
| `props` | This is a React component input mechanism |
| `redux store` | This is an implementation detail of state management |
| `API response` | This is a transport mechanism; Data is the *result* |
| `JSON` | This is a serialization format |
| `database table` | This is a storage structure; Data is the *logical entity* |
| `form values` | These are Input values, which may map to Data |
| `loading spinner` | This is a visual representation of `State: loading` |

## Design Rule

> "If I change the data source from REST API to GraphQL to local file, does the concept of what this data is change?"
> If no → it's Data. If the shape and meaning change → you might be confusing transport with data.

## Related Concepts

- **Input**: Inputs map to Data (binding)
- **Capability**: Capabilities consume Data
- **State**: Data availability affects States (`empty` when collection has no items)
- **Constraint**: Data values can constrain visibility/availability (`disabled-when: "items.length == 0"`)
