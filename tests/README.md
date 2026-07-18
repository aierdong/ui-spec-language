# Phase 6 — Conformance Test

## 定位

Phase 4 的 `validation/schema-rules.yaml` 是**单份 spec 的静态校验**：规则集，回答"这份 YAML 合法吗"。

Phase 6 是 **Agent 回归测试**，回答的是另一个问题：

```
需求 → Agent → Spec → Validator → PASS
```

> 给定一段自然语言需求，Agent 产出一份 spec；这套测试验证 spec 是否满足**语义断言**
> （必须含某 capability、必须含某 input、必须不含某实现概念）。

每升一次 Agent、每扩一版 registry，跑一遍全部测试。这是 UISL 的 Regression Test。

## 目录结构

```
tests/
├── README.md              # 本文件
├── requirements/          # 自然语言需求（Agent 的输入）
│   ├── login.md
│   ├── dashboard.md
│   ├── search.md
│   ├── crud.md
│   └── checkout.md
├── specs/                 # 期望 spec（canonical YAML）—— Agent 应产出与之等价的 spec
│   ├── login.spec.yaml
│   ├── dashboard.spec.yaml
│   ├── search.spec.yaml
│   ├── crud.spec.yaml
│   └── checkout.spec.yaml
├── expectations/          # 语义断言（must-contain / must-not-contain）
│   ├── login.expect.yaml
│   ├── dashboard.expect.yaml
│   ├── search.expect.yaml
│   ├── crud.expect.yaml
│   └── checkout.expect.yaml
├── validator/             # Python 校验器
│   ├── README.md
│   ├── run.py             # 入口：python3 tests/validator/run.py
│   ├── spec_rules.py      # Phase 4 规则的 Conformance 子集
│   ├── assertions.py      # 跑 expectations 的 must-contain / must-not-contain
│   └── report.py          # 汇总 PASS/FAIL 报告
└── reports/               # 校验器输出（由 run.py 生成，.gitignore，可重新生成）
```

## 三类夹具各是什么

| 夹具 | 角色 | 例子 |
|---|---|---|
| `requirements/<name>.md` | Agent 的**输入**（自然语言） | "Create a login page." |
| `specs/<name>.spec.yaml` | 期望 spec —— Agent 应产出的 canonical YAML | 含 Authentication capability、email/password input、submit action |
| `expectations/<name>.expect.yaml` | **语义断言** —— 不关心实现细节，只校验"含不含某概念" | must-contain: Authentication；must-not-contain: Shopping Cart |

`expectations` 是 Conformance Test 的核心：它对 spec 的判断与 React/Flutter/HTML 无关，
只关心 ontology 层面的概念存在性。

## 校验器怎么工作

`validator/run.py` 对每个场景跑两级校验：

1. **Structural（Phase 4 规则子集）** —— 覆盖 Conformance Test 最容易回归的规则：
   Forbidden Relationships / Required Properties / Cardinality / Reference Integrity /
   Decision Rules / Semantic Integrity / Constraint Rules 中的高价值子集。
2. **Semantic（Phase 6 断言）** —— 加载 `expectations/<name>.expect.yaml`，逐条检查：
   - `must-contain`：spec 中存在指定概念（按 capability.id / input.kind / action.intent 等）
   - `must-not-contain`：spec 中不存在禁用概念（如 `Shopping Cart`、组件名 `Button/Modal`）

两层都 PASS → 场景 PASS；任一失败 → 场景 FAIL，附失败规则 id 与说明。

## 运行

```bash
# 跑全部 canonical 场景
python3 tests/validator/run.py

# 跑单个 canonical 场景
python3 tests/validator/run.py login

# 校验 Agent 生成的候选目录（文件名与场景同名）
python3 tests/validator/run.py --candidate-dir agent-output

# 校验单个 Agent 候选 spec
python3 tests/validator/run.py login --candidate agent-output/login.spec.yaml
```

无第三方依赖（仅 PyYAML，已确认可用）。

## Candidate 与等价性

`tests/specs/*.spec.yaml` 是 canonical fixture，用来证明测试本身成立。真实回归时，Agent 产物通过
`--candidate-dir` 或 `--candidate` 输入；校验器不会要求 YAML 文本完全相等，只要求：

1. 候选 spec 通过 Phase 4 结构规则子集。
2. 候选 spec 满足 `expectations/<name>.expect.yaml` 的语义断言。

这意味着字段顺序、描述文案、非关键可选字段可以不同；Capability/Input/Action/State 等核心语义必须一致。

## 如何加一个新场景

1. 在 `requirements/` 写需求 md。
2. 在 `specs/` 写期望 spec（尽量复用 `registry/` 已有构件）。
3. 在 `expectations/` 写断言 —— 至少一条 `must-contain`、一条 `must-not-contain`。
4. `python3 tests/validator/run.py <name>` 应输出 PASS。

## 与其他 Phase 的分工

| 产物 | 回答 | Phase 6 是否重复 |
|---|---|---|
| `validation/schema-rules.yaml` | 单份 spec **形状是否合法** | 否 — validator 复用它做结构性校验 |
| `tests/specs/*.spec.yaml` | Agent **应产出什么** | 否 — 这是回测基准，不是新规则 |
| `tests/expectations/*.expect.yaml` | spec 是否**满足语义断言** | Phase 6 独有 |
| `tests/requirements/*.md` | Agent 的**真实输入** | Phase 6 独有 |

一句话：Phase 4 规则管"一份 spec 站不站得住脚"；Phase 6 测试管"Agent 写出来的 spec 满不满足
人类需求里那几个语义点"。两者叠加才构成闭环。
