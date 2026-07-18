# Test Validator

Python 校验器，无第三方打包依赖（仅 PyYAML）。

## 文件

- `run.py` — 入口：`python3 run.py [scenario]`，支持 `--candidate-dir` / `--candidate`
- `spec_rules.py` — Phase 4 结构规则中用于 Conformance Test 的高价值子集
- `assertions.py` — 加载 `../expectations/<name>.expect.yaml`，跑 `must-contain` / `must-not-contain`
- `report.py` — 收集 failing rule，打印 PASS/FAIL 报告并写入 `../reports/`

## 校验两级

1. **Structural**：远比不上完整的 schema 校验器（那是 Phase 4 范畴）；这里实现的是
   足以支持 Conformance Test 的一个子集 —— 主要做"必填属性存在"、"引用可解析"、
   "forbidden relationship 别名不被使用"、"语义命名不含组件/CSS 词"。
   不替代 `validation/schema-rules.yaml` 的完整规则集；Phase 6 spec 本身就是
   canonical form，结构性问题应尽量在前序 Phase 消除。
2. **Semantic**：按 `expectations` 断言查"含不含某概念"。

## 运行

```bash
python3 tests/validator/run.py
python3 tests/validator/run.py login
python3 tests/validator/run.py --candidate-dir agent-output
python3 tests/validator/run.py login --candidate agent-output/login.spec.yaml
```

## 当前 Structural 覆盖范围

已覆盖：

- Forbidden Relationships：`FR-001` 到 `FR-010` 中的直接字段与 Navigation target/source 检查。
- Required Properties：`RP-001` 到 `RP-011`。
- Cardinality：`CA-001`、`CA-002`、`CA-004`、`CA-005`。
- Reference Integrity：`RI-001`、`RI-004` 的解析与类型前缀检查。
- Decision Rules：`DE-002`。
- Semantic Integrity：`SI-001` 到 `SI-005`。
- Constraint Rules：`CT-001`、`CT-002`。

暂不覆盖：`RI-003` circular references、`DE-003`/`DE-004`、`CT-003` 这类需要表达式语义分析的规则。

## 设计原则

- 校验器会写入 `../reports/*.report.txt`，报告是可重新生成的输出。
- 失败时附规则 id 与定位信息，让 Agent 知道哪里偏了。
- 不引入 JSON Schema 库；用数据驱动地把规则展开成函数，便于后续补规则。
