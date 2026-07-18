# Requirement — Login

## 场景

用户需要在登录页输入凭据（邮箱 + 密码）完成身份认证。

## 需求描述

Create a login page. The user provides their email address and password and
submits them. On success, the user is navigated to the home page. On failure,
an inline error message is shown near the form. There is also a link to create
a new account.

## 语义要点（Agent 必须捕捉）

- 一个 **Authentication Capability**
- 两个 **Credential Input**（email、password）
- 一个 **Primary Action**（submit / authenticate）
- 至少一个 **Error State / Failure State**
- 至少一条 **Error Feedback**（inline，靠近表单）
- 一条 **Navigation** 指向 home
- 一个 **Decision** 解释成功 / 失败两条分支
- 不应出现 Shopping Cart、Button、Modal 等实现或无关概念
