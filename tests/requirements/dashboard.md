# Requirement — Dashboard

## 场景

用户登录后进入的首页，展示账户概览，并提供若干入口能力。

## 需求描述

Create a home dashboard page shown after authentication. It must be gated by
authentication (only signed-in users can see it). It shows the user's profile
summary and account balance. From the dashboard the user can search records,
open the records manager, and sign out. When the session data is missing the
page must be hidden.

## 语义要点

- Page 必须 `guarded-by` 一个 authentication constraint
- 展示型 Section（profile-summary、account-balance）通过 `receives` 或 capability `consumes` 取 data
- 至少一个 **Search** 入口 capability 与一个 **CRUD / Record** 管理入口
- 一个 **sign-out** Action
- 一个 **authenticated** state 因 data 缺失而约束页面可见性
- 不应出现"未登录"专属的 captcha 输入或购物相关概念
