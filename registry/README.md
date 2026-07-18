# Vocabulary Registry — Phase 5

Registry 是高频、可直接复用的 **vocabulary instance 壳**，让 Agent 选词时"不用猜"：
锁定一个概念的 canonical `id`、登记它的已知别名、给出推荐接线。

Registry **不重述** Ontology / Taxonomy / Normal Forms 已定义的内容，而是把这三者
交汇成一份份可复用的构件。

## 与其他 Phase 的分工

| 产物 | 回答 | Registry 是否重复 |
|---|---|---|
| `ontology/*.md` | 概念**是什么**（定义、反例、设计规则） | 否 |
| `taxonomy/*.yaml` | 概念在**分类树哪个位置**，继承什么默认 | 否 — 条目用 `taxonomy_ref` 回指 |
| `normal-forms/*.nf.yaml` | 每个语义的 **ONE canonical shape** + 等价映射 | 否 — 条目本身必须符合 NF |
| `schema/canonical-schema.yaml` | YAML 的**合法形状** | 否 — 条目是形状的填值 |
| `registry/*` | **高频概念的拿来即用构件** + 别名登记 + 推荐接线 | — |

一句话：**Taxonomy 说"Authentication 在分类树哪个位置、默认继承什么"；Registry 给
"一个可复用的 authenticate 构件、它有哪些已知别名、推荐接哪些 input/action"。**

## 条目结构

每个概念一个 `.yaml` 文件，固定形状：

```yaml
id: <slug>                          # lowercase-hyphen，同 concept 目录内唯一
label: string
intent: string                      # 来自 ontology/taxonomy 的 intent 文案
concept: Capability | Input | Action
taxonomy_ref: <Concept: Category.Leaf>   # 回指 taxonomy 叶子节点
aliases: [...]                      # 已登记别名（Agent 选词去重依据；来源 = taxonomy）
recommended:                        # 薄接线，推荐不强制
  requires:     [<Input 典型 id>]       # 仅 capability
  provides:     [<Action 典型 intent>]    # 仅 capability
  produces:     [<State 子集>]           # 仅 capability
  communicates: [<Feedback kind 子集>]   # 仅 capability
notes: string?                      # 复用注意事项 / false friend 提醒
```

### 概念专属字段

- **Capability**：含 `recommended.{requires,provides,produces,communicates}`。
  `requires`/`provides` 列典型 id/intent——指向同 registry 的其他 input/action 条目，
  或用 taxonomy 引用（如 `"Action: CRUD.Create"`）指向尚无独立条目的叶子——不内联
  完整 Input/Action 体；实例化留给具体 spec。`produces`/`communicates` 列典型
  State/Feedback 概念名（State 与 Feedback 子目录 v1 尚未建，先用概念名填写，
  引用健全性留给 Phase 6 校验脚本）。
- **Input**：必含 `kind`（NF `kind-values` 之一）。`password` 等 **secret** 类
  credential 强制 `sensitive: true`；email 身份标识类 credential 可为 `sensitive: false`
  （值本身不是秘密，参见 NF input agent-instruction #4）。`validation` 指向
  **典型 constraint 概念名**（如 `required`、`email-format`、`min-length`），保持平台
  无关、不绑死某 spec 的 `constraint.<id>` 引用，也不绑死 `maps-to`。
- **Action**：必含 `intent`（NF `intent-values` 之一）；可选 `priority`
  /`confirmation`。destructive intent（`delete`）须带 `confirmation` 文案。

## 一致性约束（v1 人工保证，脚本校验留给 Phase 6）

1. `id` 在同 concept 目录内唯一。
2. `taxonomy_ref` 指向的节点必须存在于对应 `taxonomy/*.yaml`。
3. `aliases` 必须是其 `taxonomy_ref` 节点（或其祖先节点）已声明 alias 的子集——
   Registry 不发明新别名。
4. Capability/Input/Action 的 `id`/`kind`/`intent` 命名须符合 NF canonical 形状。

## 目录与清单（v1）

```
registry/
├── README.md
├── capabilities/   (7)  authenticate, register, account-recovery,
│                          crud-records, search, upload, notification
├── inputs/         (7)  email, password, otp, search-query,
│                          agree-to-terms, file-upload, display-field
└── actions/        (8)  submit, submit-auth, cancel, dismiss,
                          delete, navigate-to, sign-out, search
```

v1 共 22 个条目，覆盖 `examples/login.spec.yaml` 用到的全部概念，外加
CRUD/Search/Upload 几条最高频。后续可按需补齐 Branch(注:Decision)、State 等子目录。

## Agent 使用方式

1. 为某个 Capability 选词时，先在 `capabilities/` 里找是否已有匹配构件。
2. 命中则用 registry 的 `id`，按 `recommended` 接线实例化（接线可裁剪）。
3. 未命中再回 `taxonomy/*.yaml` 找分类叶子节点，自行实例化并建议补登 registry。
4. 永远不要在 spec 里使用 registry `aliases` 之外的造词。

---

**Version**: 0.1.0-draft
**Status**: Phase 5 — Vocabulary Registry (v1 capability+input+action)
**Last Updated**: 2026-07-18
