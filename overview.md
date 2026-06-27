# UI/UX 规范描述语言

## 目标

不是设计一种 UI DSL，而是设计一种 Agent 可推理的 UI Ontology + Spec Language。

```
需求
    ↓
Agent
    ↓
UI Spec（YAML）
    ↓
Agent
    ↓
React / Flutter / AMis / HTML
```
像设计一门编程语言一样，分几个阶段完成。

---

# Phase 0：确定设计原则（最重要） ✅

这是以后所有 Vocabulary 的判断依据。

### Principle 1：Everything is semantic

所有字段都必须表达**意义**。

例如：

```
❌ width、margin、flex、div
✅ authenticate、credential、marketing、search、primary-action
```

如果一个字段只能指导 CSS，它就不应该出现在 Spec。

---

### Principle 2：Everything is platform independent

不能出现：
```
Checkbox、Radio、Drawer、Popover、Card
```

应该出现：
```
Boolean Choice、 Single Selection、Overlay、Information Container
```

因为：React、Flutter、CLI、Voice 都可以映射。

---

### Principle 3：Describe intent, not implementation

例如：`submit-auth` 而不是 `button`

---

### Principle 4：Vocabulary first

DSL 第二。
Schema 第三。
Renderer 最后。

---

### Principle 5：Every concept has one definition

例如： `Authentication` 在整个 Vocabulary 里只有一个定义。

不能：
```
auth
login
signin
authenticate
```

四个词混着用。

---

# Phase 1：设计 Vocabulary（不要写 YAML） ✅

整个项目第一版只有一本文档。

例如：

```
ui-ontology/
    capability.md
    section.md
    action.md
    state.md
    input.md
    feedback.md
    navigation.md
    constraint.md
    decision.md
```

然后每个 Concept 都固定模板。

例如：

```
Capability
Definition
Relationship
Required Properties
Optional Properties
Examples
Counter Examples
```

例如：

```
Authentication
Definition: Verify user identity.
Contains
  - Credential
  - Primary Action
    - Feedback
Produces
  - Authenticated
  - Authentication Failed
Examples
  - Login
  - Register
  - SSO
Counter Examples
  - Button
  - Input
  - Modal
```

注意：

这里完全没有 YAML。

---

# Phase 2：建立 Taxonomy（分类） ✅

很多 DSL 死掉，就是 Vocabulary 没有层级。

例如：

```
Capability
├── Authentication
├── Search
├── Upload
├── CRUD
├── Payment
└── Notification
```

再例如：

```
Input
├── Credential
│     ├── Email
│     ├── Password
│     └── OTP
├── Text
├── Number
├── Date
└── Boolean
```

以后 Agent 不需要猜：
Email 属于 Credential。
Credential 属于 Input。

---

# Phase 2.5：建立 Normal Forms ✅ 已完成

> **详见 [`normal-forms/`](normal-forms/) 目录**

这是数据库设计里借来的概念，但我觉得特别适合你的项目。

很多 Agent 失败，不是因为不会写，而是因为**同一个意思可以写十种方式**。
例如：

下面三个表达其实完全等价：

```yaml
role: form-field
type: email
```

```yaml
field:
  kind: email
```

```yaml
credential:
  type: email
```

对于人来说没区别。

对于 Agent 来说，这是三个不同 Pattern。

所以我建议在 Registry 建立一条规则：

> **每个语义只有一种 Canonical Form。**

例如规定：

```
Authentication
    requires Credential

Credential
    kind = email | password | otp

PrimaryAction
    intent = authenticate
```

以后任何 Prompt、任何 Agent、任何训练样本，都只能写这一种形式。这样，你不是靠 Prompt 引导 Agent，而是在构建一个**可验证、可收敛的语言**。

### Phase 2.5 产出

| # | 文件 | 内容 |
|---|------|------|
| 0 | `normal-forms/README.md` | Normal Form 规则体系、等价映射参考、Agent 决策树 |
| 1 | `normal-forms/page.nf.yaml` | Page 规范形式 + 路由→页面映射 |
| 2 | `normal-forms/capability.nf.yaml` | Capability 规范形式 + feature/component→capability 映射 |
| 3 | `normal-forms/input.nf.yaml` | Input 规范形式 + widget/HTML→InputKind 映射 |
| 4 | `normal-forms/action.nf.yaml` | Action 规范形式 + button/handler→intent 映射 |
| 5 | `normal-forms/section.nf.yaml` | Section 规范形式 + component→layout-pattern 映射 |
| 6 | `normal-forms/state.nf.yaml` | State 规范形式 + boolean-flag→state 映射 |
| 7 | `normal-forms/feedback.nf.yaml` | Feedback 规范形式 + toast/alert→feedback-kind 映射 |
| 8 | `normal-forms/navigation.nf.yaml` | Navigation 规范形式 + router/link→method 映射 |
| 9 | `normal-forms/constraint.nf.yaml` | Constraint 规范形式 + HTML-attribute→condition 映射 |
| 10 | `normal-forms/decision.nf.yaml` | Decision 规范形式 + if-else/switch→branches 映射 |
| 11 | `normal-forms/data.nf.yaml` | Data 规范形式 + fetch/store→source 映射 |

每个 NF 文件包含：Canonical Form、Property Canonical Names、Equivalence Mappings、False Friends、Agent Instruction。

---

# Phase 3：定义 Relationship

这是我觉得最关键的一步。
不要设计字段，而是设计关系。例如：

```
Page
contains
Section
Section
contains
Capability
Capability
requires
Input
Capability
provides
Action
Capability
produces
State
State
triggers
Navigation
Decision
explains
Capability
```

以后 YAML 就不会乱。

---

# Phase 4：设计 Canonical Schema

直到这里。才开始写 YAML。
例如：

```yaml
page:
sections:
capabilities:
actions:
states:
constraints:
decisions:
```

不要一开始就出现：

```
components
```

我甚至建议：
第一版没有 component。

---

# Phase 5：建立 Vocabulary Registry

这是很多 DSL 没做，所以后来越来越乱。
例如：

```
registry/
capabilities/
    authenticate.yaml
    upload.yaml
    search.yaml
inputs/
    email.yaml
    password.yaml
actions/
    submit.yaml
    cancel.yaml
states/
    loading.yaml
    empty.yaml
    error.yaml
```

例如：

```
authenticate.yaml
```

里面：

```yaml
id: authenticate
requires:
  - credential
produces:
  - authenticated
  - auth-failed
recommended-actions:
  - submit
recommended-feedback:
  - error-message
aliases:
  - login
  - sign-in
```

以后：
Agent 根本不用猜。

---

# Phase 6：建立 Conformance Test（我认为这是最容易忽略但最关键的）

这是我建议你一定要做的。
每增加 Vocabulary。
增加测试。
例如：

```
tests/
login/
dashboard/
search/
crud/
checkout/
```

测试不是 React。而是：

```
Requirement
↓
Agent
↓
Spec
↓
Validator
↓
PASS
```

例如：

```
Input
Create a login page.
Expected
Contains Authentication Capability
Contains Credential Input
Contains Primary Action
Contains Error State
Must not contain Shopping Cart
```

Agent 每升级一次。跑全部测试。

这就是 DSL 的 Regression Test。

---

# Phase 7：最后才是 Skill

Skill 根本不用教：怎么写 YAML。

Skill 教：

```
Vocabulary。
Relationship。
Constraint。
Decision。
```

例如：

```
When describing UI:
Always use registered Capability.
Never invent vocabulary.
Never use HTML concepts.
Prefer semantic concepts.
If unknown, reference registry.
```

---

## 最后，我想给你一个我认为最重要的建议

如果这是一个长期项目，我不会把它命名为 **UI DSL**，而会命名为 **UI Ontology** 或 **UISL (UI Specification Language)**，并把仓库结构设计成下面这样：

```text
ui-spec/
├── ontology/      # 定义世界：有哪些概念，它们是什么
├── taxonomy/      # 定义层级：每个概念的分类树 + 继承规则
├── normal-forms/  # 定义规范形式：每个语义的 ONE canonical YAML shape
├── registry/      # 定义词汇：Authentication、Credential、Search...
├── schema/        # 定义 YAML 结构
├── validation/    # 校验规则和约束
├── examples/      # Login、Dashboard、Checkout...
├── tests/         # Agent 回归测试
└── renderers/     # React、AMis、Flutter 等适配器
```

在这个结构里，**YAML 只是 `schema/` 的一个序列化格式**。真正的资产是 `ontology/` 和 `registry/`——它们定义了 Agent 对 UI 世界的共同语言。等这两部分稳定以后，你会发现，无论换模型、换框架、还是增加新的 Renderer，整个体系都能保持一致。这也是我认为它能够真正实现"批量化"而不是"反复调 Prompt"的关键。
