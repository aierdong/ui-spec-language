# Requirement — CRUD Records

## 场景

一个记录集合管理页：用户查看记录列表，可新增、编辑、删除某条记录。

## 需求描述

Create a records management page. The user sees the list of records, can
create a new record, edit an existing one, and delete one. Before delete,
the user is asked to confirm via a prompt; cancellation returns to the
list. On error (e.g. server failure), an inline error is shown.

## 语义要点

- 一个 **CRUD** capability (`crud-records`)
- **create / edit / delete** 三个 Action
- 一个 **confirmation Feedback** + delete 走 confirm
- 一个 **selected / deleted / loading** state
- 一个 **Decision** 解释 delete confirm 后的去向（删除 vs 取消）
- 不应出现 "DataTable"、避免 "Grid"、避免按钮/对话框组件语义
