
# Ontology 审查报告

## 总览

| 维度 | 状态 |
|------|------|
| Required Properties vs `required-property-matrix.yaml` | ✅ 全部一致 |
| README Relationship Graph vs `relationship.matrix.yaml` | ✅ 一致 |
| 各 concept 文件 vs README Graph | ⚠️ 2 处不一致 |
| 各 concept 文件 vs `relationship.matrix.yaml` | ⚠️ 4 处不一致 |
| 矩阵内部 `canonical_property` 逻辑 | ⚠️ 2 处可疑 |
| Forbidden Relationships 违规 | ✅ 无违规 |
| 文件结构完整性 | ✅ 11 个文件均含 7 个标准章节 + Related Concepts |

---

## 一、Required Properties 一致性（vs `required-property-matrix.yaml`）

全部 **通过** ✅，无偏差：

| Concept | Matrix 要求 | 文件实际 | 状态 |
|---------|------------|---------|------|
| page | `id`, `label` | `id`, `label` | ✅ |
| capability | `id`, `intent` | `id`, `intent` | ✅ |
| section | `id` | `id` | ✅ |
| action | `id`, `intent` | `id`, `intent` | ✅ |
| input | `id`, `kind`, `label` | `id`, `label`, `kind` | ✅ |
| state | `id` | `id` | ✅ |
| data | `id`, `source` | `id`, `source` | ✅ |
| constraint | `id`, `condition` | `id`, `condition` | ✅ |
| feedback | `id`, `kind` | `id`, `kind` | ✅ |
| decision | `id`, `intent`, `branches` | `id`, `intent`, `branches` | ✅ |
| navigation | `id`, `target` | `id`, `target` | ✅ |

---

## 二、Relationship 一致性（README Graph vs 各文件 vs Matrix）

### ✅ 完全一致的 Concept（7/11）

| Concept | 状态 |
|---------|------|
| **page** | ✅ README、file、matrix 三方一致 |
| **capability** | ✅ 三方一致（`explains` property 命名见下方矩阵问题 #1） |
| **input** | ✅ 三方一致 |
| **action** | ✅ 三方一致 |
| **state** | ✅ 三方一致 |
| **feedback** | ✅ 三方一致 |
| **decision** | ✅ 三方一致 |
| **data** | ✅ 三方一致 |
| **constraint** | ✅ 三方一致 |

### ⚠️ 存在不一致的 Concept（2/11）

---

## 三、逐文件问题清单

### 1. `section.md` — 3 个问题

**问题 S1: 缺失 `receives → Data` 关系（文件 vs README + Matrix）**

- `README.md` Relationship Graph 明确列出：`Section └─ receives → Data`
- `relationship.matrix.yaml` 定义了 `section-receives-data`（canonical_property: `receives`，generation: `avoid-unless-needed`）
- `section.md` 的 Relationship 图和 Optional Properties 表中 **均未提及此关系**

修复方案：在 `section.md` 的 Optional Properties 表中添加：

```
| `receives` | Data[] | Read-only data this section displays (prefer Capability consumes Data for interactive data) |
```

并在 Relationship 图中补充：

```
Section
  └─ contains → Section
                  ├─ contains → Capability
                  ├─ contains → Section
                  ├─ obeys → Constraint
                  └─ receives → Data
```

**问题 S2: 缺失 `obeys` 属性（关系图有，属性表无）**

- Relationship 图展示了 `obeys → Constraint`
- matrix 定义 `section-obeys-constraint`（canonical_property: `obeys`）
- 但 Optional Properties 表中没有 `obeys` 属性

修复方案：在 Optional Properties 表中添加：

```
| `obeys` | Constraint[] | Rules governing section visibility or availability |
```

**问题 S3: 嵌套 Section 属性名与 Matrix 不一致**

- matrix 定义 `section-contains-section` 的 `canonical_property: contains`
- 但 `section.md` 将嵌套 section 存储在 `sections` 属性中，而 `contains` 仅用于 Capability
- 这造成同一个 `contains` 关系在不同 target 上使用了不同的 property name，且与 matrix 的 canonical_property 冲突

修复方案（二选一）：
- **方案 A（推荐）**: 更新 matrix，将 `section-contains-section` 的 `canonical_property` 改为 `sections`，与文件一致
- **方案 B**: 将 `section.md` 的 `sections` 属性改名为 `contains`（但会与 Capability 的 `contains` 产生歧义）

---

### 2. `navigation.md` — 1 个问题

**问题 N1: 缺失 `source` 属性（文件 vs README + Matrix）**

- `README.md` Relationship Graph 列出：`Navigation ├─ source → Page | Section | Capability`
- `relationship.matrix.yaml` 定义 `navigation-source`（canonical_property: `source`，required: false，targets: `[page, section, capability]`）
- `navigation.md` 的 Optional Properties 表中 **未列出 `source`**

修复方案：在 Optional Properties 表中添加：

```
| `source` | Reference | Where the navigation starts (Page, Section, or Capability) |
```

并在 Relationship 图中补充：

```
Navigation
  ├─ source → Page | Section | Capability
  ├─ target → Page | Section | Capability | External
  ├─ carry-state → State
  └─ carry-data → Data
```

---

### 3. `page.md` — 1 个问题（低优先级）

**问题 P1: `requires-auth` 与 `guarded-by` 功能重叠**

- `page.md` 列出 `requires-auth: boolean` 作为可选属性
- 同时也列出 `guarded-by: Constraint[]`
- `guarded-by: [auth-required]` 完全可以表达 `requires-auth: true` 的语义
- 这造成两种平行机制表达同一件事

修复方案（建议）：
- 在 `page.md` 中添加注释说明 `requires-auth` 是 `guarded-by: [auth-required]` 的便捷快捷方式
- 或者直接移除 `requires-auth`，统一使用 `guarded-by`

---

### 4. `action.md` — 1 个问题（设计模式差异）

**问题 A1: Constraint 关系通过内联属性表达，未使用 canonical `obeys`**

- matrix 定义 `action-obeys-constraint`（canonical_property: `obeys`）
- `capability.md` 正确使用 `obeys: Constraint[]` 属性
- 但 `action.md` 未列出 `obeys` 属性，而是通过 `disabled-when: Condition` 和 `visible-when: Condition` 表达约束

同样的模式出现在 `state.md`（`visible-when`）。

这不一定是错误——内联条件属性更符合 Action 的使用场景。但存在两种模式的不一致：
- `capability.md`、`input.md`（`validation`）→ 使用 canonical property
- `action.md`、`state.md` → 使用内联条件属性

修复方案（建议）：
- **方案 A**: 在 `action.md` 和 `state.md` 中补充 `obeys: Constraint[]`，同时保留 `disabled-when` / `visible-when` 作为便捷属性
- **方案 B**: 在 matrix 中将 `action-obeys-constraint` 的 `canonical_property` 改为 `disabled-when`（或拆分为多个关系条目）
- **方案 C**: 在各文件中添加注释说明内联属性是 `obeys → Constraint` 的语法糖

---

## 四、Matrix 内部问题

### 问题 M1: `capability-explains-decision` 的 canonical_property 命名冲突

```yaml
- id: capability-explains-decision
  relationship: explains          # 关系名
  canonical_property: may-lead-to  # 存储属性名 ← 不匹配！
```

- 关系语义是 `explains`（Capability 解释 Decision 的分支逻辑）
- 但 canonical_property 指向 `may-lead-to`（这是 Action/State→Decision 的关系名）
- `capability.md` 和 README 都使用 `explains` 作为属性名

修复方案：将 matrix 中 `capability-explains-decision` 的 `canonical_property` 改为 `explains`。

### 问题 M2: `section-contains-section` 的 canonical_property 与实际使用冲突

如上文 S3 所述，matrix 使用 `contains` 但文件使用 `sections`。

---

## 五、跨文件不一致汇总

| # | 不一致 | 涉及文件 | 严重程度 |
|---|--------|---------|---------|
| 1 | Section 缺失 `receives → Data` | section.md vs README + matrix | 🔴 高 |
| 2 | Navigation 缺失 `source` 属性 | navigation.md vs README + matrix | 🔴 高 |
| 3 | Section `obeys` 关系图有但属性表无 | section.md 内部不一致 | 🟡 中 |
| 4 | `sections` vs `contains` 属性名冲突 | section.md vs matrix | 🟡 中 |
| 5 | `explains` vs `may-lead-to` canonical_property | capability.md vs matrix | 🟡 中 |
| 6 | Constraint 表达模式不一致 | capability/action/state/feedback | 🟢 低 |
| 7 | `requires-auth` 与 `guarded-by` 重叠 | page.md 内部 | 🟢 低 |

---

## 六、遗漏检查

### 未遗漏的概念

README 列出 11 个概念，relationship matrix 也列出 11 个，所有文件均存在。无遗漏概念。

### 未遗漏的关系

Matrix 定义的所有关系（共 28 条正向 + 8 条 forbidden）在 README Graph 和各文件中均有覆盖，除了上述 S1 和 N1 两处。

### Forbidden Relationships 检查

所有 ontology 文件均未违反 matrix 中定义的 forbidden relationships（如 Page 不能直接 contains Capability、Constraint 不能 resolves-to Navigation 等）。

---

## 七、建议修复优先级

1. **立即修复**（高优先级）:
   - 补充 `section.md` 的 `receives` 属性和关系
   - 补充 `navigation.md` 的 `source` 属性和关系

2. **尽快修复**（中优先级）:
   - 补充 `section.md` 的 `obeys` 属性
   - 修正 matrix 中 `capability-explains-decision` 的 `canonical_property` 为 `explains`
   - 统一 `section-contains-section` 的 `canonical_property` 为 `sections`

3. **可后续处理**（低优先级）:
   - 统一 Constraint 表达模式（`obeys` vs 内联条件属性）
   - 澄清 `requires-auth` 与 `guarded-by` 的关系

**Tool Call: 审查 taxonomy 文件**
Status: Completed

Now I have all the data needed. Let me compile a comprehensive review.

---

# Taxonomy 审查报告

## 一、逐文件审查

### 1. `page.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | 使用 `purpose` 而非 `intent` | 🔴 不一致 | 其他所有 taxonomy 文件使用 `intent`，唯独 page 用 `purpose`。README 示例也用 `intent`。 |
| 2 | `split-screen` 布局未被任何条目使用 | 🟡 遗漏 | ontology 定义了 6 种布局，taxonomy 只用了 3 种（`centered-column`、`sidebar-shell`、`master-detail`），`split-screen`、`full-canvas`、`stacked` 均无对应条目。 |
| 3 | EntryPoint 与 ontology 登录页示例矛盾 | 🔴 错误 | ontology page.md 示例 login 页使用 `split-screen` 布局，但 taxonomy EntryPoint 使用 `centered-column`。 |
| 4 | FlowStep / ErrorRecovery 缺少 `requires-auth` | 🟡 遗漏 | 该属性是关键继承属性，应显式声明（EntryPoint 显式设为 false，但这两项未声明）。 |
| 5 | 缺少 Confirmation/Success 页面角色 | 🟡 遗漏 | 多步流程中的"操作成功"中间页无法归类。 |

**建议修复：**
- 将 `purpose` 统一改为 `intent`
- EntryPoint 布局改为 `split-screen`（或拆分出 `AuthPage` 角色使用 `split-screen`）
- 为 FlowStep / ErrorRecovery 显式声明 `requires-auth: false`
- 补充 `full-canvas` 对应的角色（如 `Canvas` / `Dashboard`）

---

### 2. `capability.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | 使用 `feedback` 而非 `communicates` | 🔴 错误 | ontology 定义的关系是 `communicates → Feedback`，taxonomy 用 `feedback` 是自造属性。 |
| 2 | 使用 `may-lead-to` 引用 Decision | 🔴 错误 | ontology 定义 `explains → Decision`，taxonomy 用 `may-lead-to`。 |
| 3 | `states` 属性不存在于 ontology | 🔴 错误 | CRUD 用 `states: [State: Selection.Unselected, ...]`，ontology 无此属性，应为 `produces`。 |
| 4 | Registration / AccountRecovery 缺少 `produces` | 🟡 遗漏 | Authentication 有 `produces`，但同级的 Registration 和 AccountRecovery 未声明。 |
| 5 | 缺少 `obeys` (Constraint) 声明 | 🟡 遗漏 | ontology 定义了 `obeys → Constraint`，taxonomy 无任何 capability 声明约束。 |
| 6 | 缺少 `consumes` (Data) 声明 | 🟡 遗漏 | ontology 定义了 `consumes → Data`，taxonomy 无任何 capability 声明数据源。 |
| 7 | 缺少 `explains` (Decision) 声明 | 🟡 遗漏 | 只有 Authentication 用 `may-lead-to` 引用了 Decision（且格式错误）。 |
| 8 | 与 Action taxonomy 双重身份概念缺失 | 🟡 遗漏 | README 提到 Export、Navigate、Search、Sort、Filter 应在两边都有，但 Capability 缺少 Navigate、Sort（Sort 只在 DataManagement 下作为 Filter/Sort 存在，但不是独立 capability）。 |
| 9 | Communication.Confirmation 语义混淆 | 🟡 设计问题 | 它声明 `requires: Input: Selection.Boolean` 和 `provides: Action: Toggle.Selection`，更像一个 Action 模式而非 Capability。 |

**建议修复：**
- 全局替换 `feedback:` → `communicates:`
- 全局替换 `may-lead-to:` (引用 Decision 时) → `explains:`
- CRUD 的 `states:` → `produces:`
- 为 Registration / AccountRecovery 补充 `produces`
- 补充 `obeys` / `consumes` / `explains` 声明
- 补充缺失的双重身份 capability（Navigate、Sort、Filter 独立条目）

---

### 3. `section.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | EmptyState 的 `contains` 引用 Feedback | 🔴 错误 | ontology 规定 `contains` 是 `Capability[]`，但 `Decorative.EmptyState` 引用了 `Feedback: Information.EmptyState`。 |
| 2 | "EmptyState" 同时出现在 Section 和 Feedback | 🟡 命名冲突 | Section.Decorative.EmptyState 和 Feedback.Information.EmptyState 同名，跨概念引用时产生歧义。 |
| 3 | 缺少 `obeys` (Constraint) 声明 | 🟡 遗漏 | ontology 定义了 `obeys → Constraint`，但无 section 声明约束。 |

**建议修复：**
- `Decorative.EmptyState.contains` 改为引用一个 capability（如 `DataManagement.Search`）或移除该声明
- 考虑将 Section.EmptyState 重命名为 `EmptyStateArea` 以避免歧义

---

### 4. `action.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | System.SignOut 的 `requires: confirmation` 格式错误 | 🔴 错误 | ontology 定义 `requires` 为 `Input[]`（输入数组），但这里用了标量字符串。应改为 `requires: [Input: Selection.Boolean]` 或使用 `confirmation` 属性。 |
| 2 | Run 同时作为顶级 Action 和 Capability | 🟡 重复 | `Action: Run` 和 `Capability: Workflow.Run` 概念重叠，README 说这是"双重身份"，但 Capability 侧的 `Workflow.Run` 提供的 action 是 `Action: Run`，形成循环引用。 |
| 3 | 缺少 `obeys` (Constraint) 声明 | 🟡 遗漏 | ontology 定义了 `obeys → Constraint`，taxonomy 中无 action 声明约束。 |
| 4 | 缺少 `navigates-to` 声明 | 🟡 遗漏 | ontology 定义了 `navigates-to` 属性，但 taxonomy 中无 action 使用。 |
| 5 | Navigate.Dismiss 的 `discards-changes` 不在 ontology 中 | 🟡 扩展 | 该属性未在 README 的"Taxonomy-Specific Properties"表中列出。 |

**建议修复：**
- `System.SignOut.requires` 改为标准格式或使用 `confirmation` 属性
- 将 `discards-changes` 添加到 README 的 taxonomy-specific properties 表
- 补充 `obeys` 声明

---

### 5. `input.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | 缺少 `label` 属性 | 🔴 错误 | ontology 将 `label` 列为 **Required Properties**，但 taxonomy 中无任何 input 声明 `label`。 |
| 2 | 使用层级分类而非 `kind` 枚举 | 🟡 设计差异 | ontology 定义扁平的 `kind` 枚举（credential、text、number 等），taxonomy 用父子层级（Credential.Email、Text.ShortText）。映射关系需文档化。 |
| 3 | ontology 的 `long-text` 与 taxonomy 的 `Text.LongText` | 🟡 不一致 | ontology 的 `kind` 列表中 `long-text` 是独立值，taxonomy 中是 `Text` 的子节点。 |
| 4 | `Numeric` 在 ontology 的 `kind` 中不存在 | 🔴 不一致 | ontology 的 Input Kinds 没有 `number` / `numeric`，但 taxonomy 有 `Numeric` 分类。ontology 的 `kind` 列表中有 `number`。 |
| 5 | `Display` 不在 ontology 的 Input Kinds 中 | 🟡 不一致 | ontology 的 `kind` 枚举未列出 `display`，但 taxonomy 有 `Display` 分类。 |
| 6 | `KeyValue` 无 ontology 对应 | 🟡 遗漏 | taxonomy 有 `Structured.KeyValue`，但 ontology 的 Input Kinds 未定义。 |
| 7 | 缺少 `maps-to` / `sources-from` 声明 | 🟡 遗漏 | ontology 定义了 Input 到 Data 的映射关系，taxonomy 未体现。 |
| 8 | 缺少 `visible-when` / `enabled-when` 声明 | 🟡 遗漏 | ontology 定义了这些条件属性，taxonomy 未使用。 |

**建议修复：**
- 为所有 input 节点补充 `label`（或文档化 `intent` 替代 `label` 的规则）
- 文档化 taxonomy 层级到 ontology `kind` 的映射表
- 在 ontology 中补充 `number` 和 `display` 的 kind 定义（或从 taxonomy 中移除）

---

### 6. `state.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | `timeout` 在 ontology 中存在但 taxonomy 缺失 | 🟡 遗漏 | ontology 的 Outcome group 列出 `timeout`，但 taxonomy 的 Outcome 只有 Success、Error、PartialSuccess。 |
| 2 | `ready` 在 ontology 中存在但 taxonomy 缺失 | 🟡 遗漏 | ontology 的 Lifecycle group 列出 `ready`，taxonomy 只有 Idle、Loading、Processing。 |
| 3 | `all-selected` 在 ontology 中存在但 taxonomy 缺失 | 🟡 遗漏 | ontology 的 Selection group 列出 `all-selected`，taxonomy 只有 Unselected、Selected、MultiSelected。 |
| 4 | `expired` / `slow-connection` 在 ontology 中存在但 taxonomy 部分缺失 | 🟡 遗漏 | ontology 的 Availability group 列出 `expired`，Network group 列出 `slow-connection`（taxonomy 中作为 Reconnecting 的 alias 存在）。 |
| 5 | Validation.Pristine 使用 `feedback` 属性 | 🔴 错误 | 应使用 ontology 定义的 `may-trigger → Feedback` 关系。 |
| 6 | `blocking` 未在 README 的 taxonomy-specific properties 中完整列出 | 🟡 文档 | README 列出了 `blocking: true`，但未说明它可用于 State。 |

**建议修复：**
- 补充 `Outcome.Timeout`、`Lifecycle.Ready`、`Selection.AllSelected`
- 将 `feedback: none` / `feedback: deferred` 改为标准的 `may-trigger` 格式

---

### 7. `feedback.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | 顶级分类缺少 `kind` 属性 | 🔴 错误 | ontology 将 `kind` 列为 **Required Properties**，但 Confirmation、Error、Warning、Information、Validation、Background 均未声明 `kind`。 |
| 2 | `Tooltip` 不在 ontology 的 Feedback Kinds 中 | 🟡 不一致 | ontology 定义了 8 种 kind，`tooltip` 不在其中（只有 `inline-help`）。 |
| 3 | Validation 缺少 `severity` 继承 | 🟡 不一致 | 其他分类（Error、Warning）在父节点声明了 `severity`，Validation 未声明。 |
| 4 | Background 缺少 `severity` 继承 | 🟡 不一致 | 同上。 |
| 5 | ConfirmationWarning 的 `provides` 引用 Navigation.Dismiss | 🟡 语义问题 | `provides` 通常用于 Capability → Action 关系，Feedback 中使用该属性语义不清。 |

**建议修复：**
- 为所有顶级分类补充 `kind`（如 Confirmation → `kind: confirmation`，Error → `kind: error-message`）
- 考虑将 Tooltip 改为 InlineHelp 的子类型或在 ontology 中补充
- 为 Validation / Background 补充 `severity` 继承

---

### 8. `navigation.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | 使用 `carries-state` 而非 `carry-state` | 🔴 错误 | ontology 定义的属性名是 `carry-state`（单数），taxonomy 用 `carries-state`（复数）。 |
| 2 | 缺少 `target` 属性 | 🔴 错误 | ontology 将 `target` 列为 **Required Properties**，但几乎所有 navigation 节点都未声明。 |
| 3 | `discards-changes`、`clears-session`、`animated` 不在 ontology 中 | 🟡 扩展 | 这些属性未在 README 的 taxonomy-specific properties 表中列出。 |
| 4 | `opens` 属性在 ontology 中不存在 | 🟡 扩展 | README 列出了 `opens`，但仅用于 Action，navigation taxonomy 也使用了（External.opens: new-tab）。 |

**建议修复：**
- `carries-state` → `carry-state`
- 为所有 navigation 节点补充 `target`（即使是占位符）
- 将 `discards-changes`、`clears-session`、`animated` 添加到 README 的 taxonomy-specific properties 表

---

### 9. `constraint.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | 顶级分类缺少 `condition` 属性 | 🔴 错误 | ontology 将 `condition` 列为 **Required Properties**，但 Visibility、Availability、Validity、Confirmation、Timing 的父节点均未声明。 |
| 2 | Timing.SessionExpiry 使用 `resolves-to` | 🟡 语义越界 | `resolves-to` 是 Decision 的属性，Constraint 不应有导航行为。这更像一个 Decision。 |
| 3 | Confirmation 的 `applies-to: availability` 存疑 | 🟡 设计问题 | DestructiveActionWarning 的效果是"显示确认对话框"，这更像是 `visibility` 或反馈触发，而非 `availability`。 |
| 4 | Confirmation.DestructiveActionWarning 使用 `provides` | 🟡 语义问题 | `provides` 通常用于 Capability → Action，Constraint 中使用语义不清。 |

**建议修复：**
- 为顶级分类补充占位 `condition` 或文档化"分类节点不需要 condition"的规则
- 将 `Timing.SessionExpiry` 移至 Decision taxonomy 或明确其 Constraint 语义
- 考虑将 Confirmation 移至 Feedback 或 Decision

---

### 10. `decision.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | Authentication.AuthOutcome 的 `resolves-to` 格式不一致 | 🟡 不一致 | 使用 `Navigation: AuthNavigation.GoToHome` 和 `Feedback: Error.BannerError`，格式正确但与 ontology 示例中的简单字符串格式不同。 |
| 2 | FormDirtyNavigate 引用 `State: Validation.Dirty` | 🟡 跨引用 | 引用有效，但 Decision 的 `evaluates` 应更明确地说明评估的是什么条件。 |
| 3 | AfterSubmit 只有一个分支 | 🟡 遗漏 | 缺少失败分支（如 `error → stay on form`）。 |
| 4 | Upload.FileTooLarge 缺少 `evaluates` | 🟡 遗漏 | 未声明评估的是什么条件（如文件大小数据）。 |
| 5 | 顶级分类的 `trigger` 继承可能过于宽泛 | 🟡 设计问题 | Authentication 继承 `trigger: automatic`，但 SessionExpired 可能需要 `time-based` 或 `event-based`。 |

**建议修复：**
- 为 AfterSubmit 补充错误分支
- 为 Upload.FileTooLarge 补充 `evaluates`
- 考虑将 Authentication 的 `trigger` 移到子节点级别

---

### 11. `data.taxonomy.yaml`

| # | 问题 | 严重性 | 说明 |
|---|------|--------|------|
| 1 | Remote.ApiMutableCollection 重复声明 `scope: page` | 🟡 冗余 | 父节点 Remote 已继承 `scope: page`，子节点重复声明。 |
| 2 | `Data.Navigation` 与 Navigation 概念命名冲突 | 🟡 命名冲突 | Data 下的 `Navigation` 分类与独立的 Navigation 概念同名，跨引用时产生歧义。 |
| 3 | 缺少 `database` 源类型 | 🟡 遗漏 | ontology 定义了 `database` 源类型，taxonomy 未使用。 |
| 4 | File 顶级分类缺少 `source` 属性 | 🟡 遗漏 | ontology 将 `source` 列为 Required Properties。 |

**建议修复：**
- 移除 `ApiMutableCollection` 的冗余 `scope: page`
- 将 `Data.Navigation` 重命名为 `Data.UrlData` 或 `Data.NavigationData`
- 为 File 补充 `source: file`

---

## 二、跨文件不一致问题汇总

### A. 属性命名不一致

| 问题 | 文件 | 应改为 |
|------|------|--------|
| `purpose` vs `intent` | page.taxonomy.yaml | 统一为 `intent` |
| `feedback` vs `communicates` | capability.taxonomy.yaml | 改为 `communicates` |
| `may-lead-to` vs `explains` (Decision) | capability.taxonomy.yaml | 改为 `explains` |
| `carries-state` vs `carry-state` | navigation.taxonomy.yaml | 改为 `carry-state` |
| `states` vs `produces` | capability.taxonomy.yaml (CRUD) | 改为 `produces` |

### B. 缺少必需属性

| 属性 | 缺失文件 | 说明 |
|------|----------|------|
| `label` (Required) | input.taxonomy.yaml | 所有 input 节点均缺失 |
| `kind` (Required) | feedback.taxonomy.yaml | 所有顶级分类均缺失 |
| `condition` (Required) | constraint.taxonomy.yaml | 所有顶级分类均缺失 |
| `target` (Required) | navigation.taxonomy.yaml | 几乎所有节点均缺失 |

### C. 未文档化的 Taxonomy 扩展属性

以下属性在 taxonomy 中使用但未列入 README 的 "Taxonomy-Specific Properties" 表：

| 属性 | 使用位置 |
|------|----------|
| `discards-changes` | action.taxonomy.yaml, navigation.taxonomy.yaml |
| `clears-session` | action.taxonomy.yaml, navigation.taxonomy.yaml |
| `animated` | navigation.taxonomy.yaml |
| `requires` (标量) | action.taxonomy.yaml (System.SignOut) |

### D. 命名冲突

| 名称 | 出现位置 | 建议 |
|------|----------|------|
| `EmptyState` | Section.Decorative + Feedback.Information | Section 侧改为 `EmptyStateArea` |
| `Navigation` | Data.Navigation + 独立 Navigation 概念 | Data 侧改为 `NavigationData` |
| `Confirmation` | Feedback.Confirmation + Capability.Communication.Confirmation | 明确区分或重命名 |

---

## 三、遗漏分类汇总

| 概念 | 遗漏项 | 来源 |
|------|--------|------|
| **Page** | `split-screen` 布局角色、`full-canvas` 布局角色 | ontology 定义了 6 种布局 |
| **Capability** | Navigate、Payment、Sort (独立)、Filter (独立) | ontology examples + README dual-identity |
| **State** | `Outcome.Timeout`、`Lifecycle.Ready`、`Selection.AllSelected`、`Availability.Expired` | ontology State Groups |
| **Input** | `number` kind 映射、`display` kind 映射 | ontology Input Kinds |
| **Feedback** | `tooltip` kind 映射 | ontology Feedback Kinds |
| **Constraint** | 无遗漏但有语义越界（SessionExpiry） | — |
| **Decision** | AfterSubmit 缺少错误分支 | — |
| **Data** | `database` 源类型 | ontology Source Types |

---

## 四、优先修复建议

**P0（阻断性错误）：**
1. capability.taxonomy.yaml: `feedback` → `communicates`，`may-lead-to` → `explains`，`states` → `produces`
2. navigation.taxonomy.yaml: `carries-state` → `carry-state`
3. feedback.taxonomy.yaml: 为所有顶级分类补充 `kind`
4. constraint.taxonomy.yaml: 为所有顶级分类补充 `condition`（或文档化规则）
5. input.taxonomy.yaml: 补充 `label`（或文档化 `intent` 替代规则）
6. section.taxonomy.yaml: 修复 EmptyState 的 `contains` 引用

**P1（一致性问题）：**
1. page.taxonomy.yaml: `purpose` → `intent`
2. 补充遗漏的 State 节点（Timeout、Ready、AllSelected）
3. 将未文档化的扩展属性添加到 README
4. 解决命名冲突（EmptyState、Navigation、Confirmation）

**P2（增强）：**
1. 补充缺失的 Capability（Navigate、Payment、Sort、Filter 独立条目）
2. 补充 `obeys`、`consumes`、`explains` 等跨概念引用
3. 文档化 Input taxonomy 层级到 ontology `kind` 的映射关系
4. 考虑将 Timing.SessionExpiry 移至 Decision taxonomy

**Tool Call: 审查 normal-forms 文件**
Status: Completed

Confirmed — the ontology lists `display` as an input kind, but the NF's `kind-values` section doesn't include it. This is an omission.

Now I have all the data I need. Let me write the comprehensive audit report.

---

# Normal Forms 全面审查报告

## 审查概要

共审查 13 个文件，发现 **31 个问题**，按严重程度分类：

| 严重程度 | 数量 | 说明 |
|----------|------|------|
| 🔴 严重 | 8 | 跨文件不一致、属性遗漏导致语义缺失 |
| 🟡 中等 | 12 | 类型不匹配、别名冲突、等价映射错误 |
| 🟢 轻微 | 11 | 文档瑕疵、命名建议、格式问题 |

---

## 一、逐文件审查

### 1. README.md

**问题 R1（🟡 中等）**：`intent` / `purpose` 别名双向冲突

Rule 3 定义了两个独立的 canonical property：
- `intent` → 别名包括 `purpose`（用于 Capability/Action/Decision）
- `purpose` → 别名包括 `intent`（仅用于 Page）

这意味着 `intent` 既是 canonical 又是 alias，取决于上下文。Agent 在解析时需要额外的上下文判断，容易出错。

**建议**：将 Page 的 `purpose` 别名列表中的 `intent` 移除，改为 `goal` 或 `function`，避免双向 alias。

**问题 R2（🟢 轻微）**：README 中 Capability 行 `may-lead-to` 注释缺失

README 第 222 行 `Capability | explains | Decision | may-lead-to` —— 关系名是 `explains`，但 canonical property 是 `may-lead-to`。这个映射令人困惑，且与 ontology 中使用 `explains` 作为属性名不一致。

**建议**：在 README 中增加注释说明 `explains` → `may-lead-to` 的映射原因，或统一为 `explains`。

**问题 R3（🟢 轻微）**：Section 在 Relationship Table 中缺少 `receives` 关系

README 第 211 行列出了 `Section | contains | Capability` 和 `Section | obeys | Constraint`，但 Section 的 ontology 中也描述了 `Section | receives | Data` 关系，这在 README 的 Relationship Table 中缺失。

**建议**：在 Canonical Relationship Table 中增加：
```
| Section | receives | Data | `receives` |
```

---

### 2. required-property-matrix.yaml

**问题 M1（🟢 轻微）**：与 NF 文件一致，无严重问题

Matrix 与所有 NF 文件的 required properties 一致。✓

---

### 3. page.nf.yaml

**问题 P1（🟡 中等）**：`purpose` 的 alias 列表包含 `intent`

第 39 行：`purpose: { aliases: [intent, role, function, page-purpose] }`

`intent` 是 Capability/Action/Decision 的 canonical property。在 Page 上将其作为 `purpose` 的 alias，会导致 Agent 在解析包含 `intent` 的 Page 时产生歧义。

**建议**：移除 `intent` alias，保留 `[role, function, page-purpose, goal]`。

**问题 P2（🟢 轻微）**：`requires-auth` 与 `guarded-by` 功能重叠

两个属性都用于访问控制。`requires-auth` 是 `boolean`，`guarded-by` 是 `ConstraintRef[]`。在语义上，`requires-auth: true` 可以表达为 `guarded-by: [constraint.auth-required]`。

**建议**：在 NF 中增加注释说明两者的关系，或考虑将 `requires-auth` 标记为 `guarded-by` 的语法糖。

**问题 P3（🟢 轻微）**：`layout` 值与 Section 的 `layout-pattern` 值有重叠

Page 的 `layout` 值包括 `sidebar-shell`、`split-screen`、`centered-column` 等，Section 的 `layout-pattern` 也有同名值。虽然 README Rule 10 明确了"布局只属于 Page 和 Section"，但同名值可能导致 Agent 混淆层级。

**建议**：在 NF 中增加注释说明 Page.layout 描述页面骨架，Section.layout-pattern 描述区域内部排列。

---

### 4. capability.nf.yaml

**问题 C1（🔴 严重）**：`may-lead-to` 与 ontology `explains` 属性名冲突

Ontology（capability.md）使用 `explains` 作为属性名：
```yaml
| `explains` | Decision[] | Branch decisions this capability can trigger |
```

NF 使用 `may-lead-to`：
```yaml
may-lead-to: DecisionRef[]? # canonical property for the "explains" relationship
```

两者指向同一关系，但属性名不同。Agent 从 ontology 学到 `explains`，从 NF 学到 `may-lead-to`，会产生冲突。

**建议**：统一为一个名称。如果 `may-lead-to` 是 canonical，则更新 ontology；如果 `explains` 是 canonical，则更新 NF 和 Relationship Table。

**问题 C2（🟡 中等）**：等价映射中 toolbar 映射不完整

第 139-160 行的 toolbar 等价映射将 toolbar 拆分为两个独立的 capability（filter 和 sort），但没有说明它们应该在同一个 Section 中。一个 toolbar 通常是一个 Section（`layout-pattern: horizontal-strip`），包含多个 Capability。

**建议**：增加 resolution 说明 "toolbar → Section with layout-pattern: horizontal-strip, contains multiple capabilities"。

**问题 C3（🟢 轻微）**：Agent Instruction 缺少 `label` 的使用指导

Agent Instruction 列出了 canonical property names，但没有提到 `label` 是可选的且用于人类可读名称。

**建议**：增加 "label is optional — use when the capability needs a human-readable display name"。

---

### 5. section.nf.yaml

**问题 S1（🔴 严重）**：缺少 `receives` 属性

Canonical Relationship Table 定义了 `Section | receives | Data | receives`，但 section.nf.yaml 的 canonical form 中没有 `receives` 属性。这意味着 Section 无法声明它需要接收哪些 Data。

**建议**：在 canonical form 中增加：
```yaml
receives: DataRef[]?  # Data this section receives/displays
```

并在 property-canonical-names 中增加：
```yaml
receives: { aliases: [data, incoming, displays, shows] }
```

**问题 S2（🟡 中等）**：`obeys` 在 ontology 的 Optional Properties 表中缺失

Ontology（section.md）的 Relationship 图中列出了 `obeys → Constraint`，但 Optional Properties 表中没有 `obeys`。NF 中有 `obeys`，这是正确的。

**建议**：更新 ontology 的 Optional Properties 表，增加 `obeys`。

**问题 S3（🟢 轻微）**：等价映射中 `tabs` 映射为 `vertical-stack` 不准确

第 131-144 行将 `tabs` 映射为 `layout-pattern: vertical-stack`。Tabs 的语义是"切换内容面板"，更准确的 layout-pattern 应该是 `horizontal-strip`（tab bar）加上内容区域。

**建议**：考虑增加一个专门的 `tabbed` layout-pattern，或在 resolution 中说明 "tabs → Section.Content.TabPanel with zones: [tabs, content]"。

---

### 6. action.nf.yaml

**问题 A1（🔴 严重）**：缺少 4 个关系属性

Canonical Relationship Table 定义了 Action 的以下关系，但 NF 中均未体现：

| 关系 | 目标 | Canonical Property | 状态 |
|------|------|--------------------|------|
| `Action \| triggers \| State \| triggers` | State | `triggers` | ❌ 缺失 |
| `Action \| produces \| Feedback \| produces` | Feedback | `produces` | ❌ 缺失 |
| `Action \| obeys \| Constraint \| obeys` | Constraint | `obeys` | ❌ 缺失 |
| `Action \| may-lead-to \| Decision \| may-lead-to` | Decision | `may-lead-to` | ❌ 缺失 |

只有 `navigates-to`（对应 `Action | may-lead-to | Navigation | navigates-to`）存在。

**建议**：在 canonical form 中增加：
```yaml
triggers: StateRef[]?       # States that can arise from this action
produces: FeedbackRef[]?    # Feedback this action produces
obeys: ConstraintRef[]?     # Constraints on this action's availability
may-lead-to: DecisionRef[]? # Decisions this action may trigger
```

**问题 A2（🟡 中等）**：`navigates-to` 类型应为 `NavigationRef` 而非 `PageRef`

第 24 行：`navigates-to: PageRef?`

Relationship Table 说 `Action | may-lead-to | Navigation | navigates-to`，目标类型应该是 `NavigationRef`，不是 `PageRef`。Navigation 可以指向 Page、Section、Capability 或外部 URL。

**建议**：改为 `navigates-to: NavigationRef?`。

**问题 A3（🟡 中等）**：`submit` intent 的 aliases 包含 capability 级概念

第 53 行：`submit: { aliases: [save, apply, send, post, create, update, confirm, execute, finish, done, ok, sign-in, login, authenticate] }`

`sign-in`、`login`、`authenticate` 是 Capability 级概念（用户目标），不是 Action intent（按钮行为）。Action 的 `submit` 是"提交"行为，`login` 是"登录"能力。

**建议**：从 `submit` aliases 中移除 `sign-in`、`login`、`authenticate`。

**问题 A4（🟡 中等）**：等价映射中 `link` 映射为 Action 而非 Navigation

第 120-133 行将 `link` 映射为 `action` with `intent: navigate`。但 link 的本质是触发 Navigation，应该映射为 Navigation 实体，而非 Action。

**建议**：将此等价映射移至 navigation.nf.yaml，或在 resolution 中说明 "link → Navigation (with implicit Action.navigate trigger)"。

**问题 A5（🟢 轻微）**：`reset` 映射为 `intent: cancel` 可能不准确

第 177-185 行将 `type: reset` 映射为 `intent: cancel`。Reset 通常是"重置表单到默认值"，而 cancel 是"放弃当前输入"。两者语义不同：reset 保留页面，cancel 可能离开页面。

**建议**：增加 `reset` 作为独立的 intent value，或在 resolution 中说明 "reset → cancel (clears form, stays on page)"。

---

### 7. input.nf.yaml

**问题 I1（🔴 严重）**：`kind` 缺少 `display` 类型

Ontology（input.md）定义了 13 种 Input Kind，包括 `display`（Read-only presentation of data）。但 NF 的 `kind-values` 只列出了 12 种，缺少 `display`。

**建议**：在 kind-values 中增加：
```yaml
display: { aliases: [read-only, readonly, output, presentation, label-value] }
```

**问题 I2（🟡 中等）**：等价映射中 textarea 映射缺少 `id`

第 116-126 行的 textarea 等价映射：
```yaml
maps-to:
  input:
    kind: long-text
    validation: [constraint.max-length]
```

缺少 `id` 和 `label`，Agent 无法生成完整的 Input。

**建议**：增加 `id: inferred` 或在 resolution 中说明 "id and label must be inferred from context"。

**问题 I3（🟢 轻微）**：`credential` kind 的隐含行为说明不够清晰

Agent Instruction 第 4 行说 "Email fields in auth context → kind: credential; in profile context → kind: text with format: email validation"。但没有说明如何判断"auth context"。

**建议**：增加判断规则："If the Input is part of a Capability with id 'authentication' or similar, treat as credential context"。

---

### 8. state.nf.yaml

**问题 ST1（🔴 严重）**：缺少 4 个关系属性

Canonical Relationship Table 定义了 State 的以下关系，但 NF 中均未体现：

| 关系 | 目标 | Canonical Property | 状态 |
|------|------|--------------------|------|
| `State \| may-trigger \| Feedback \| may-trigger` | Feedback | `may-trigger` | ❌ 缺失 |
| `State \| may-lead-to \| Decision \| may-lead-to` | Decision | `may-lead-to` | ❌ 缺失 |
| `State \| may-lead-to \| Navigation \| may-lead-to` | Navigation | `may-lead-to` | ❌ 缺失 |
| `State \| obeys \| Constraint \| obeys` | Constraint | `obeys` | ❌ 缺失 |

**建议**：在 canonical form 中增加：
```yaml
may-trigger: FeedbackRef[]?   # Feedback this state may trigger
may-lead-to: DecisionRef[]?   # Decisions this state may lead to
may-lead-to-nav: NavigationRef[]? # Navigation this state may trigger
obeys: ConstraintRef[]?       # Constraints on this state
```

注意：`may-lead-to` 同时指向 Decision 和 Navigation，需要决定是合并为一个属性还是拆分。

**问题 ST2（🟡 中等）**：等价映射中 store 映射自相矛盾

第 128-144 行的 store 等价映射：
```yaml
resolution:
  - 'Redux state slice → multiple State concepts'
  - 'user: null → data, not state'
  - 'status → state.id'
```

Resolution 说 "user: null → data, not state"，但 maps-to 却包含了 `id: user, default: null` 作为 State。这是自相矛盾的。

**建议**：从 maps-to 中移除 `id: user`，改为在 resolution 中说明 "user data should be extracted as Data concept with source: context"。

**问题 ST3（🟡 中等）**：`visible-when` 类型应为 `ConstraintRef[]` 而非 `Condition`

Relationship Table 说 `State | obeys | Constraint | obeys`，但 NF 中使用 `visible-when: Condition?`（直接条件表达式）。这与其他概念（Action、Input）的 `visible-when` 一致，但与 Relationship Table 的语义不匹配。

**建议**：要么在 NF 中增加 `obeys: ConstraintRef[]?` 属性（与 Relationship Table 一致），要么更新 Relationship Table 将 `obeys` 改为 `visible-when`。

**问题 ST4（🟢 轻微）**：`source` 属性的值类型未定义

第 24 行：`source: StateSource?  # What triggers this state: internal | external | user-action`

但 NF 中没有定义 `StateSource` 的 canonical values。

**建议**：增加：
```yaml
source-values:
  internal: { aliases: [system, automatic, code-driven] }
  external: { aliases: [api, network, server, outside] }
  user-action: { aliases: [click, input, interaction, manual] }
```

---

### 9. feedback.nf.yaml

**问题 F1（🔴 严重）**：缺少 `may-lead-to` 属性

Canonical Relationship Table 定义了 `Feedback | may-lead-to | Decision | may-lead-to`，但 NF 中没有 `may-lead-to` 属性。

**建议**：在 canonical form 中增加：
```yaml
may-lead-to: DecisionRef[]? # Decisions this feedback may trigger
```

**问题 F2（🟡 中等）**：`visible-when` 与 Relationship Table 的 `obeys` 不一致

Relationship Table 说 `Feedback | obeys | Constraint | visible-when`，canonical property 是 `visible-when`。NF 中有 `visible-when: Condition?`，类型是 `Condition`（直接条件表达式），而非 `ConstraintRef[]`。

这与其他概念的 `visible-when` 模式一致（都是 `Condition?`），但 Relationship Table 暗示应该是 Constraint 引用。

**建议**：明确 `visible-when` 的语义——是直接条件还是 Constraint 引用。如果两者都需要，可以增加 `obeys: ConstraintRef[]?` 作为 Constraint 引用，保留 `visible-when: Condition?` 作为直接条件。

**问题 F3（🟢 轻微）**：`kind: empty-state` 的 `severity` 建议为 `info` 但示例中未体现

Agent Instruction 第 5 行说 "kind: empty-state always has duration: persistent"，但没有提到 severity。等价映射中 empty-state 的 severity 是 `info`，但 Agent Instruction 中没有这条规则。

**建议**：在 Agent Instruction 中增加 "kind: empty-state → severity: info by default"。

---

### 10. navigation.nf.yaml

**问题 N1（🟡 中等）**：缺少 `icon` 属性

Ontology（navigation.md）的 Optional Properties 中列出了 `icon: string`，但 NF 中没有。

**建议**：在 canonical form 中增加：
```yaml
icon: string?  # Semantic icon reference (not a specific icon library name)
```

**问题 N2（🟡 中等）**：Relationship Table 中的 `source` 属性在 NF 和 ontology 中均不存在

README 第 239 行：`Navigation | source | Page / Section / Capability | source`

但 navigation.nf.yaml 和 ontology/navigation.md 都没有 `source` 属性。Navigation 的来源关系实际上通过 Page 的 `navigation-in`/`navigation-out` 属性表达。

**建议**：要么从 Relationship Table 中移除 `Navigation | source` 行（因为 source 关系由 Page 侧表达），要么在 NF 中增加 `source: Reference?` 属性。

**问题 N3（🟢 轻微）**：`method` 值 `external` 与 `is-external` 属性功能重叠

`method: external` 和 `is-external: true` 表达的是同一件事。当 `method` 是 `external` 时，`is-external` 必然为 `true`。

**建议**：在 NF 中增加注释说明 "is-external is redundant when method: external, but useful when method is not specified"。

---

### 11. constraint.nf.yaml

**问题 CO1（🔴 严重）**：`applies-to` 存在双重语义冲突

`applies-to` 在两个地方有不同含义：

1. **NF canonical form**（第 19 行）：`applies-to: TargetType? # visibility | availability | validity`
2. **Relationship Table**（第 246 行）：`Constraint | applies-to | Input / Action / State / Capability / Section / Page / Feedback | applies-to`

NF 中的 `applies-to` 是约束效果类型（TargetType enum），Relationship Table 中的 `applies-to` 是约束目标实体列表（EntityRef[]）。两者同名但语义完全不同。

**建议**：将 NF 中的 `applies-to` 重命名为 `effect` 或 `constraint-type`，保留 `applies-to` 用于目标实体引用。或者在 NF 中增加 `targets: EntityRef[]?` 属性。

**问题 CO2（🟡 中等）**：等价映射中 `condition: always` 不在 canonical condition syntax 中

第 97-105 行的 disabled 等价映射：
```yaml
condition: always
```

但 canonical condition syntax（第 58-75 行）没有定义 `always` 关键字。

**建议**：在 condition-syntax 中增加 `always: "always"` 和 `never: "never"` 作为特殊值，或在等价映射中使用 `condition: "true"`。

**问题 CO3（🟢 轻微）**：`applies-to-values` 的 aliases 与 `severity-values` 有重叠

`availability` 的 aliases 包含 `active`，`severity` 的 `success` aliases 包含 `ok`。虽然不会直接冲突，但 `active` 在不同上下文中有不同含义。

**建议**：无需修改，但需注意。

---

### 12. decision.nf.yaml

**问题 D1（🟡 中等）**：`property-canonical-names` 包含嵌套属性

第 33-42 行的 `property-canonical-names` 包含了 `condition`、`resolves-to`、`label`、`priority` 等嵌套在 `branches[]` 内部的属性。这些不是 Decision 的顶层属性，放在 `property-canonical-names` 中会造成混淆。

**建议**：将嵌套属性的别名定义移至 `branches` 的注释中，或增加一个 `branch-item-properties` 节。

**问题 D2（🟢 轻微）**：`default-branch` 的 condition 语义不明确

canonical form 中 `default-branch` 没有 `condition` 属性，但 branches 中的每个 item 都有 `condition`。这意味着 default-branch 是"无条件匹配"的 fallback。

**建议**：在 NF 中增加注释说明 "default-branch is taken when no other branch condition matches; it does not have a condition property"。

**问题 D3（🟢 轻微）**：等价映射中 `resolves-to` 使用了混合引用格式

有些 `resolves-to` 使用 `navigation.go-to-home`，有些使用 `action.delete`，有些使用 `state.idle`。格式一致，但没有说明 `resolves-to` 可以指向哪些概念类型。

**建议**：在 Agent Instruction 中增加 "resolves-to can reference: navigation.*, state.*, action.*, feedback.*"。

---

### 13. data.nf.yaml

**问题 DA1（🔴 严重）**：缺少 `affects` 属性

Canonical Relationship Table 定义了 `Data | affects | State / Constraint / Decision | affects`，但 NF 中没有 `affects` 属性。

**建议**：在 canonical form 中增加：
```yaml
affects: Reference[]?  # State, Constraint, or Decision entities affected by this data
```

并在 property-canonical-names 中增加：
```yaml
affects: { aliases: [impacts, influences, triggers, drives] }
```

**问题 DA2（🟡 中等）**：`type` 值中缺少 `dictionary` 的详细说明

`dictionary` 类型在 NF 中定义了，但没有说明它与 `collection` 的区别。Agent 可能混淆两者。

**建议**：在 NF 中增加注释 "dictionary = key-value lookup (config, translations); collection = ordered list of similar items (projects, users)"。

**问题 DA3（🟢 轻微）**：`source` 值 `context` 与 `parent` 的区别不够清晰

`context` 是"应用级上下文"，`parent` 是"从父组件继承"。两者在 React 中都可能使用 `useContext`，容易混淆。

**建议**：在 NF 中增加注释 "context = app-wide ambient data (theme, locale, auth); parent = explicitly passed from container (props)"。

---

## 二、跨文件不一致问题汇总

### 🔴 严重不一致

| # | 问题 | 涉及文件 | 说明 |
|---|------|----------|------|
| X1 | Action NF 缺少 4 个关系属性 | action.nf.yaml, README | triggers, produces, obeys, may-lead-to 均缺失 |
| X2 | State NF 缺少 4 个关系属性 | state.nf.yaml, README | may-trigger, may-lead-to (×2), obeys 均缺失 |
| X3 | `explains` vs `may-lead-to` 属性名冲突 | capability.nf.yaml, ontology/capability.md | NF 用 `may-lead-to`，ontology 用 `explains` |
| X4 | `applies-to` 双重语义 | constraint.nf.yaml, README | NF 中是 TargetType enum，Relationship Table 中是 EntityRef[] |
| X5 | Section 缺少 `receives` | section.nf.yaml, README | Data → Section 的关系无法表达 |
| X6 | Data 缺少 `affects` | data.nf.yaml, README | Data → State/Constraint/Decision 的关系无法表达 |
| X7 | Feedback 缺少 `may-lead-to` | feedback.nf.yaml, README | Feedback → Decision 的关系无法表达 |
| X8 | Input 缺少 `display` kind | input.nf.yaml, ontology/input.md | ontology 定义了 13 种 kind，NF 只有 12 种 |

### 🟡 中等不一致

| # | 问题 | 涉及文件 | 说明 |
|---|------|----------|------|
| X9 | `intent`/`purpose` 别名双向冲突 | page.nf.yaml, README | `intent` 既是 canonical 又是 alias |
| X10 | Action `navigates-to` 类型错误 | action.nf.yaml, README | 应为 NavigationRef，不是 PageRef |
| X11 | Navigation 缺少 `icon` | navigation.nf.yaml, ontology/navigation.md | ontology 有，NF 没有 |
| X12 | Navigation `source` 属性在 NF 和 ontology 中均不存在 | navigation.nf.yaml, README | Relationship Table 有，但无处定义 |
| X13 | `visible-when` vs `obeys` 类型不匹配 | state.nf.yaml, feedback.nf.yaml, README | NF 用 Condition，Relationship Table 用 ConstraintRef |
| X14 | Action `submit` aliases 包含 capability 级概念 | action.nf.yaml | `login`, `authenticate` 不是 action intent |
| X15 | store 等价映射自相矛盾 | state.nf.yaml | resolution 说 "user → data" 但 maps-to 包含 user state |
| X16 | `condition: always` 不在 canonical syntax 中 | constraint.nf.yaml | 等价映射使用了未定义的条件值 |
| X17 | textarea 等价映射缺少 id | input.nf.yaml | maps-to 不完整 |
| X18 | Decision property-canonical-names 包含嵌套属性 | decision.nf.yaml | branches 内部属性不应在顶层定义 |
| X19 | link 等价映射应为 Navigation 而非 Action | action.nf.yaml | link 的本质是触发 Navigation |
| X20 | Section `obeys` 在 ontology Optional Properties 中缺失 | section.nf.yaml, ontology/section.md | Relationship 图有，属性表没有 |

---

## 三、建议的修复方案

### 优先级 1：补充缺失的关系属性

为以下 NF 文件补充 Relationship Table 中定义的关系属性：

1. **action.nf.yaml**：增加 `triggers`、`produces`、`obeys`、`may-lead-to`
2. **state.nf.yaml**：增加 `may-trigger`、`may-lead-to`（Decision 和 Navigation）、`obeys`
3. **section.nf.yaml**：增加 `receives`
4. **feedback.nf.yaml**：增加 `may-lead-to`
5. **data.nf.yaml**：增加 `affects`

### 优先级 2：解决语义冲突

1. **统一 `explains` vs `may-lead-to`**：决定 Capability → Decision 的 canonical property 名称，更新 ontology 或 NF
2. **拆分 `applies-to`**：将 constraint.nf.yaml 的 `applies-to` 重命名为 `effect`，保留 `applies-to` 用于目标实体引用
3. **明确 `visible-when` 语义**：决定是直接条件还是 Constraint 引用，或两者都支持

### 优先级 3：修复类型和别名

1. **Action `navigates-to`**：改为 `NavigationRef?`
2. **Page `purpose` alias**：移除 `intent`
3. **Action `submit` aliases**：移除 `login`、`authenticate`、`sign-in`
4. **Input `kind`**：增加 `display`
5. **Navigation**：增加 `icon`
6. **constraint.nf.yaml**：在 condition-syntax 中增加 `always`/`never`

### 优先级 4：修复等价映射

1. **state.nf.yaml store**：移除 maps-to 中的 `id: user`
2. **input.nf.yaml textarea**：增加 `id: inferred` 注释
3. **action.nf.yaml link**：移至 navigation.nf.yaml 或增加说明
4. **constraint.nf.yaml disabled**：将 `condition: always` 改为 `condition: "true"`

### 优先级 5：更新 ontology 以保持一致

1. **ontology/section.md**：在 Optional Properties 中增加 `obeys`
2. **ontology/capability.md**：将 `explains` 改为 `may-lead-to`（如果选择 `may-lead-to` 作为 canonical）
3. **ontology/navigation.md**：确认是否需要 `source` 属性

---

## 四、总结

Normal Forms 的整体设计质量很高，结构清晰，等价映射和 False Friends 有实际价值。主要问题集中在：

1. **关系属性遗漏**：多个 NF 文件没有实现 Relationship Table 中定义的关系属性，导致语义图不完整
2. **命名冲突**：`applies-to`、`explains`/`may-lead-to`、`intent`/`purpose` 存在歧义
3. **类型不一致**：`visible-when`、`navigates-to` 等属性的类型在不同文件中不一致

建议按优先级逐步修复，优先补充缺失的关系属性，然后解决语义冲突，最后修复类型和别名问题。

**Tool Call: 审查关系矩阵一致性**
Status: Completed

Now I have a comprehensive understanding of the entire system. Let me compile the final audit report.

---

# Relationship Matrix 审查报告

## 总体评估

**50 个关系条目，覆盖 11 个概念，与 ontology README 关系图 100% 对应。** 矩阵整体设计严谨，方向性清晰，generation 约束合理。以下是发现的问题，按严重程度排序。

---

## 🔴 P1 — 命名冲突（3 个问题）

### 问题 1：`capability-communicates-feedback` 的 inverse 语义错误

| 字段 | 当前值 | 问题 |
|------|--------|------|
| `inverse` | `belongs-to` | `belongs-to` 是结构包含关系的逆（Page→Section, Section→Capability），不应用于流关系 `communicates` |

**影响**：Feedback 的 `belongs-to` 会与 Section 的 `belongs-to` 和 Capability 的 `belongs-to` 混淆，无法区分是结构归属还是通信关系。

**修复**：将 inverse 改为 `communicated-by`。

```yaml
# 当前
- id: capability-communicates-feedback
  inverse: belongs-to        # ❌

# 修复
- id: capability-communicates-feedback
  inverse: communicated-by   # ✅
```

### 问题 2：`triggered-by` 作为 inverse 被两个不同关系使用

| 条目 | inverse |
|------|---------|
| `action-may-lead-to-decision` | `triggered-by` → decision triggered-by action |
| `state-may-lead-to-navigation` | `triggered-by` → navigation triggered-by state |

**影响**：同一个 inverse 名称指向两种完全不同的语义（决策触发 vs 导航触发），可能导致解析歧义。

**修复**：`state-may-lead-to-navigation` 的 inverse 改为 `driven-by`。

### 问题 3：`state-may-lead-to-navigation` 与 `action-may-lead-to-navigation` 的 inverse 不一致

| 条目 | relationship | inverse |
|------|-------------|---------|
| `action-may-lead-to-navigation` | `may-lead-to` | `initiated-by` |
| `state-may-lead-to-navigation` | `may-lead-to` | `triggered-by` |

两者都指向 Navigation，但 inverse 名称不同。应保持一致。

**修复**：统一为 `initiated-by` 或为 State 使用 `driven-by`。

---

## 🟡 P2 — 缺失关系（2 个问题）

### 问题 4：缺少 `data-sources-input` / `data-supplies-input`

| 已有 | 缺失 |
|------|------|
| `input-maps-to-data` → 有 read-side-only 逆 `data-maps-to-input` | `input-sources-from-data` → **无**对应 read-side-only 逆 |

`input-sources-from-data` 声明 `inverse: supplies`，但矩阵中没有 `data-supplies-input` 条目。这与 `input-maps-to-data` / `data-maps-to-input` 的模式不一致。

**修复**：添加 read-side-only 条目：

```yaml
- id: data-supplies-input
  category: dependency
  source: data
  relationship: supplies
  targets: [input]
  cardinality: 0..*
  required: false
  aliases: [sources, provides-choices, provides-defaults]
  inverse: sources-from
  meaning: Input values sourced from this data.
  canonical_property: supplies
  generation: read-side-only
```

### 问题 5：`feedback-may-lead-to-decision` 的 inverse 名称误导

| 字段 | 当前值 | 问题 |
|------|--------|------|
| `inverse` | `evaluates` | 暗示 Decision → evaluates → Feedback，但该关系不存在 |

矩阵中 Decision 的 `evaluates` 目标只有 State、Data、Constraint，**不包括 Feedback**。ontology 图也不包含此关系。

**修复**：将 inverse 改为 `prompted-by`。

```yaml
# 当前
- id: feedback-may-lead-to-decision
  inverse: evaluates        # ❌ 暗示不存在的关系

# 修复
- id: feedback-may-lead-to-decision
  inverse: prompted-by      # ✅
```

---

## 🟡 P3 — 语义/设计问题（4 个问题）

### 问题 6：Page 使用 `guarded-by` 而其他概念使用 `obeys`

| 概念 | 关系动词 |
|------|---------|
| Input, Action, State, Capability, Section, Feedback | `obeys` |
| Page | `guarded-by` |

这是 ontology 明确定义的语义区分（页面是"守卫"，其他概念是"服从"），但 `constraint-applies-to-target` 条目的 targets 列表中包含 `page`，使用的是 `applies-to` 而非 `guards`。这造成了双路径：

- Constraint → applies-to → Page（通过 `constraint-applies-to-target`）
- Constraint → guards → Page（通过 `page-guarded-by-constraint` 的 inverse）

**建议**：在 `constraint-applies-to-target` 的 rules 中明确说明 Page 的特殊情况，或在 README 中增加说明。

### 问题 7/8：Navigation source/target 的不对称性

| Navigation 条目 | targets |
|----------------|---------|
| `navigation-source` | `[page, section, capability]` |
| `navigation-target` | `[page, section, capability, external]` |

但从概念侧，只有 Page 定义了 `navigation-in` 和 `navigation-out`。Section 和 Capability 可以作为 Navigation 的 source/target，但没有对应的属性定义。

**影响**：从 Section/Capability 侧无法直接表达"哪些导航到达/离开此概念"。

**建议**：这可能是有意设计（Navigation-centric），但应在 README 中明确说明。

### 问题 9：`canonical_property` 与 `relationship` 名称不匹配

| 关系 ID | relationship | canonical_property | 说明 |
|---------|-------------|-------------------|------|
| `capability-explains-decision` | `explains` | `may-lead-to` | 语义不匹配 |
| `input-obeys-constraint` | `obeys` | `validation` | 语义不匹配 |
| `feedback-obeys-constraint` | `obeys` | `visible-when` | 语义不匹配 |
| `action-may-lead-to-navigation` | `may-lead-to` | `navigates-to` | 语义不匹配 |
| `state-is-triggered-by-action` | `is-triggered-by` | `source` | 语义不匹配 |
| `input-sources-from-data` | `sources-from` | `source` | 语义不匹配 |

`canonical_property` 是 YAML schema 中的属性名，`relationship` 是语义关系名。虽然功能上正确，但容易造成混淆。

**建议**：在 README 的 Shorthand 部分增加一个映射表，明确 `canonical_property` → `relationship` 的对应关系。

---

## 🟡 P4 — forbidden_relationships 缺失（3 个问题）

### 问题 10：缺少 `constraint → resolves-to → *` 的全面禁止

当前 forbidden 列表只有：
```yaml
- source: constraint
  relationship: resolves-to
  target: navigation
```

但 Constraint 不应该 resolves-to **任何**概念（State、Action、Feedback 也不行）。当前只禁止了 Navigation，遗漏了其他三个。

**修复**：添加：
```yaml
- source: constraint
  relationship: resolves-to
  target: state
  reason: Constraint is a persistent rule; Decision handles branching.
- source: constraint
  relationship: resolves-to
  target: action
  reason: Constraint is a persistent rule; Decision handles branching.
- source: constraint
  relationship: resolves-to
  target: feedback
  reason: Constraint is a persistent rule; Decision handles branching.
```

### 问题 11：缺少 `state → communicates → feedback` 的禁止

Capability 使用 `communicates` 连接 Feedback，但 State 不应使用此动词。当前只有 `state → renders → feedback` 的禁止（实现细节），但 `communicates` 也可能被误用。

**修复**：添加：
```yaml
- source: state
  relationship: communicates
  target: feedback
  reason: State may-trigger Feedback; communicates is reserved for Capability.
```

### 问题 12：缺少 `navigation → source → external` 的禁止

`navigation-target` 允许 `external`，但 `navigation-source` 不允许。当前无显式禁止条目。

**修复**：添加：
```yaml
- source: navigation
  relationship: source
  target: external
  reason: Navigation always originates from internal concepts.
```

---

## 🟢 P5 — 基数/required 一致性（1 个问题）

### 问题 13：`constraint-applies-to-target` 的 required 值

| 字段 | 当前值 | 建议 |
|------|--------|------|
| `required` | `false` | 考虑改为 `true` |
| `recommended` | `true` | — |

一个 Constraint 没有 `applies-to` 目标在语义上是无意义的。`required-property-matrix.yaml` 中 Constraint 要求 `[id, condition]`，但 `applies-to` 至少应该有 1 个目标。

**建议**：将 `required` 改为 `true`，或在 rules 中说明 `applies-to` 必须在 branches 或其他上下文中隐式指定。

---

## 🟢 P6 — required-property-matrix 交叉检查

| 概念 | required 属性 | 关系矩阵对应 | 状态 |
|------|-------------|-------------|------|
| capability | `[id, intent]` | 所有关系 `required: false` | ✅ |
| action | `[id, intent]` | 所有关系 `required: false` | ✅ |
| input | `[id, kind, label]` | 所有关系 `required: false` | ✅ |
| page | `[id, label]` | `page-contains-section` `required: false` | ✅ |
| section | `[id]` | 所有关系 `required: false` | ✅ |
| state | `[id]` | 所有关系 `required: false` | ✅ |
| feedback | `[id, kind]` | 所有关系 `required: false` | ✅ |
| navigation | `[id, target]` | `navigation-target` `required: true` ✅ | ✅ |
| constraint | `[id, condition]` | `constraint-applies-to-target` `recommended: true` | ⚠️ 见 P5 |
| decision | `[id, intent, branches]` | 所有关系 `required: false` | ✅ |
| data | `[id, source]` | 所有关系 `required: false` | ✅ |

---

## 🟢 P7 — ontology README 与矩阵一致性

| 检查项 | 结果 |
|--------|------|
| README 关系图中的所有关系是否在矩阵中有对应条目 | ✅ 50/50 全部覆盖 |
| 矩阵中的关系是否都在 ontology 概念文件中有定义 | ✅ 全部覆盖 |
| 关系方向是否一致 | ✅ 矩阵遵循 ontology 图的正向定义 |
| read-side-only 标记是否正确 | ✅ 5 个 read-side-only 条目全部正确标记 |
| forbidden_relationships 是否覆盖 README Validity Rules | ⚠️ 见 P4 |

---

## 修复方案汇总

| 优先级 | 问题 | 修复操作 | 影响文件 |
|--------|------|---------|---------|
| 🔴 P1-1 | `capability-communicates-feedback` inverse 错误 | `belongs-to` → `communicated-by` | `relationship.matrix.yaml` L207 |
| 🔴 P1-2 | `triggered-by` inverse 命名冲突 | `state-may-lead-to-navigation` inverse 改为 `driven-by` | `relationship.matrix.yaml` L419 |
| 🔴 P1-3 | Navigation inverse 不一致 | 与 P1-2 同步修复 | `relationship.matrix.yaml` L419 |
| 🟡 P2-1 | 缺少 `data-supplies-input` | 添加 read-side-only 条目 | `relationship.matrix.yaml` (Data 区域) |
| 🟡 P2-2 | `feedback-may-lead-to-decision` inverse 误导 | `evaluates` → `prompted-by` | `relationship.matrix.yaml` L487 |
| 🟡 P3-6 | Page `guarded-by` 双路径 | 在 `constraint-applies-to-target` rules 中添加说明 | `relationship.matrix.yaml` L718-720 |
| 🟡 P3-9 | `canonical_property` 命名不匹配 | 在 README 中增加映射表 | `relationships/README.md` |
| 🟡 P4-10 | Constraint resolves-to 禁止不完整 | 添加 state/action/feedback 三条 | `relationship.matrix.yaml` forbidden 区域 |
| 🟡 P4-11 | 缺少 state communicates feedback 禁止 | 添加一条 | `relationship.matrix.yaml` forbidden 区域 |
| 🟡 P4-12 | 缺少 navigation source external 禁止 | 添加一条 | `relationship.matrix.yaml` forbidden 区域 |
| 🟢 P5-13 | constraint-applies-to required 值 | `required: false` → `required: true` | `relationship.matrix.yaml` L711 |

## Assistant

<thinking>
Now I have comprehensive audit results from all four sub-agents. Let me synthesize the findings into a clear, actionable report for the user. Let me organize the findings by severity and cross-reference them across all four audit areas.
</thinking>

Now I have comprehensive audit results from all four sub-agents. Let me synthesize the findings into a clear, actionable report for the user. Let me organize the findings by severity and cross-reference them across all four audit areas. 四个子代理已完成全面审查。以下是综合审查报告。

---

# UISL Phase 0–3 综合审查报告

## 总体评估

| 维度 | 状态 |
|------|------|
| 设计原则 (Phase 0) | ✅ 清晰无问题 |
| Vocabulary/Ontology (Phase 1) | ⚠️ 2 处遗漏 |
| Taxonomy (Phase 2) | ⚠️ 多处属性名错误 + 遗漏 |
| Normal Forms (Phase 2.5) | ⚠️ 多处关系属性缺失 |
| Relationships (Phase 3) | ⚠️ 3 处命名冲突 + forbidden 不完整 |

---

## 🔴 P0 — 阻断性错误（必须立即修复）

### 1. `applies-to` 双重语义冲突

**文件**: `constraint.nf.yaml` + `relationship.matrix.yaml`

`applies-to` 在两个地方有完全不同的含义：
- NF 中：`applies-to: TargetType?`（`visibility | availability | validity`）— 约束效果类型
- Relationship Table 中：`Constraint | applies-to | Entity[]` — 约束目标实体列表

**修复**：将 NF 中的 `applies-to` 重命名为 `effect` 或 `constraint-type`，保留 `applies-to` 用于目标实体引用。

### 2. `capability-explains-decision` 的 `canonical_property` 命名冲突

**文件**: `relationship.matrix.yaml` L244, `capability.nf.yaml`, `ontology/capability.md`

- 关系语义：`explains`
- canonical_property：`may-lead-to`
- ontology 使用 `explains`，NF 使用 `may-lead-to`

**修复**：统一为 `explains`，更新 matrix 的 `canonical_property`。

### 3. Action NF 缺少 4 个关系属性

**文件**: `action.nf.yaml`

Relationship Table 定义了 Action 的 `triggers`、`produces`、`obeys`、`may-lead-to`，但 NF 中均未体现（只有 `navigates-to`）。

**修复**：在 canonical form 中补充：
```yaml
triggers: StateRef[]?
produces: FeedbackRef[]
obeys: ConstraintRef[]
may-lead-to: DecisionRef[]
```

### 4. State NF 缺少 4 个关系属性

**文件**: `state.nf.yaml`

`may-trigger`、`may-lead-to`（Decision）、`may-lead-to`（Navigation）、`obeys` 均缺失。

**修复**：补充对应属性。注意 `may-lead-to` 同时指向 Decision 和 Navigation，需决定合并或拆分。

### 5. Section NF 缺少 `receives` 属性

**文件**: `section.nf.yaml`, `ontology/section.md`

Relationship Table 定义了 `Section | receives | Data`，但 NF 和 ontology 属性表均缺失。

**修复**：在 section.nf.yaml 和 ontology/section.md 中补充 `receives: DataRef[]?`。

### 6. Data NF 缺少 `affects` 属性

**文件**: `data.nf.yaml`

`Data | affects | State / Constraint / Decision` 关系无法表达。

**修复**：补充 `affects: Reference[]?`。

### 7. Feedback NF 缺少 `may-lead-to` 属性

**文件**: `feedback.nf.yaml`

`Feedback | may-lead-to | Decision` 关系无法表达。

**修复**：补充 `may-lead-to: DecisionRef[]?`。

---

## 🟡 P1 — 一致性问题（尽快修复）

### 8. Taxonomy 属性名错误（5 处）

| 文件 | 错误 | 正确 |
|------|------|------|
| `capability.taxonomy.yaml` | `feedback:` | `communicates:` |
| `capability.taxonomy.yaml` | `may-lead-to:` (引用 Decision) | `explains:` |
| `capability.taxonomy.yaml` (CRUD) | `states:` | `produces:` |
| `navigation.taxonomy.yaml` | `carries-state` | `carry-state` |
| `page.taxonomy.yaml` | `purpose` | `intent`（与其他概念一致） |

### 9. Required Properties 缺失（Taxonomy）

| 属性 | 缺失文件 |
|------|----------|
| `label` (Required) | `input.taxonomy.yaml` — 所有 input 节点均缺失 |
| `kind` (Required) | `feedback.taxonomy.yaml` — 所有顶级分类均缺失 |
| `condition` (Required) | `constraint.taxonomy.yaml` — 所有顶级分类均缺失 |
| `target` (Required) | `navigation.taxonomy.yaml` — 几乎所有节点均缺失 |

### 10. `intent`/`purpose` 别名双向冲突

**文件**: `normal-forms/README.md`, `page.nf.yaml`

- `intent` 的别名包含 `purpose`
- `purpose` 的别名包含 `intent`

Agent 无法判断哪个是 canonical。

**修复**：从 Page 的 `purpose` 别名列表中移除 `intent`。

### 11. Action `navigates-to` 类型错误

**文件**: `action.nf.yaml`

当前类型是 `PageRef?`，应为 `NavigationRef?`（Navigation 可指向 Page、Section、Capability 或外部 URL）。

### 12. `visible-when` vs `obeys` 类型不匹配

**文件**: `state.nf.yaml`, `feedback.nf.yaml`

NF 使用 `visible-when: Condition?`（直接条件），Relationship Table 使用 `obeys: ConstraintRef[]`。需明确语义。

### 13. `triggered-by` inverse 命名冲突

**文件**: `relationship.matrix.yaml`

| 条目 | inverse |
|------|---------|
| `action-may-lead-to-decision` | `triggered-by` |
| `state-may-lead-to-navigation` | `triggered-by` |

同一 inverse 名称指向两种不同语义。

**修复**：`state-may-lead-to-navigation` 的 inverse 改为 `driven-by`。

### 14. `capability-communicates-feedback` 的 inverse 错误

**文件**: `relationship.matrix.yaml` L207

当前 inverse 是 `belongs-to`（结构包含关系），应改为 `communicated-by`。

### 15. Input NF 缺少 `display` kind

**文件**: `input.nf.yaml`

ontology 定义了 13 种 Input Kind（含 `display`），NF 只有 12 种。

### 16. Navigation NF 缺少 `icon` 属性

**文件**: `navigation.nf.yaml`

ontology Optional Properties 有 `icon`，NF 没有。

### 17. Section `obeys` 在 ontology 属性表中缺失

**文件**: `ontology/section.md`

Relationship 图有 `obeys → Constraint`，但 Optional Properties 表中没有。

---

## 🟢 P2 — 改进建议（可后续处理）

### 18. Forbidden Relationships 不完整

| 缺失 | 说明 |
|------|------|
| `constraint → resolves-to → state/action/feedback` | 只禁止了 Navigation，遗漏了其他三个 |
| `state → communicates → feedback` | State 应使用 `may-trigger`，不应使用 `communicates` |
| `navigation → source → external` | Navigation 源只能是内部概念 |

### 19. 缺少 `data-supplies-input` 反向条目

**文件**: `relationship.matrix.yaml`

`input-sources-from-data` 声明 `inverse: supplies`，但矩阵中没有 `data-supplies-input` 条目。

### 20. Taxonomy 命名冲突

| 名称 | 出现位置 | 建议 |
|------|----------|------|
| `EmptyState` | Section.Decorative + Feedback.Information | Section 侧改为 `EmptyStateArea` |
| `Navigation` | Data.Navigation + 独立 Navigation | Data 侧改为 `NavigationData` |
| `Confirmation` | Feedback + Capability.Communication | 明确区分或重命名 |

### 21. Taxonomy 遗漏的分类

| 概念 | 遗漏项 |
|------|--------|
| Page | `split-screen`、`full-canvas` 布局角色 |
| Capability | Navigate、Payment、Sort（独立）、Filter（独立） |
| State | `Outcome.Timeout`、`Lifecycle.Ready`、`Selection.AllSelected` |
| Data | `database` 源类型 |

### 22. Action `submit` aliases 包含 capability 级概念

**文件**: `action.nf.yaml`

`sign-in`、`login`、`authenticate` 是 Capability 级概念，不是 Action intent。

### 23. `requires-auth` 与 `guarded-by` 功能重叠

**文件**: `ontology/page.md`, `page.nf.yaml`

`requires-auth: true` 可表达为 `guarded-by: [auth-required]`。建议文档化两者关系或移除 `requires-auth`。

### 24. Constraint 表达模式不一致

- `capability.md`、`input.md` → 使用 canonical `obeys`/`validation`
- `action.md`、`state.md` → 使用内联 `disabled-when`/`visible-when`

建议在各文件中说明内联属性是 `obeys → Constraint` 的语法糖。

---

## 修复优先级总结

| 优先级 | 数量 | 说明 |
|--------|------|------|
| 🔴 P0 | 7 | 阻断性错误：语义冲突、关系属性缺失 |
| 🟡 P1 | 10 | 一致性问题：属性名错误、类型不匹配 |
| 🟢 P2 | 7 | 改进建议：命名冲突、遗漏分类、文档完善 |

**建议修复顺序**：
1. 先修复 P0 的 `applies-to` 语义冲突和 `explains`/`may-lead-to` 统一
2. 补充所有 NF 文件缺失的关系属性（Action、State、Section、Data、Feedback）
3. 修复 Taxonomy 的属性名错误
4. 补充 forbidden_relationships
5. 处理 P2 的命名冲突和遗漏分类
