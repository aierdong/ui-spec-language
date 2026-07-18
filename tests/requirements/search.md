# Requirement — Search

## 场景

一个面向记录集合的搜索页：用户输入查询词，系统按条件筛选并展示命中列表。

## 需求描述

Create a search page. The user enters a query, optionally applies one or more
filters (e.g. record status), and submits. The matching records are shown in a
results region. When there are no matches, an empty-state message is shown.
When the query is invalid (too short), an inline validation message appears
near the search input. The user can clear results.

## 语义要点

- 一个 **Search** capability
- 一个 **search-query Input**
- 一个或多个 **filter Input**（这里用 single-selection）
- 一个 **search Action**（trigger search）+ 一个 **clear Action**（dismiss/empty）
- 三个 state：**searching / has-results / no-results**
- **empty-state Feedback** 与 **validation Feedback**
- 一个 **Decision** 解释"有结果 / 无结果"两条分支
- 不应出现 "DataTable"、"Grid" 组件语义；无登录概念
