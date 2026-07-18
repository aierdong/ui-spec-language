# Requirement — Checkout

## 场景

用户的订单结算页：核对订单项、选择支付方式、提交订单。

## 需求描述

Create a checkout page. The user reviews the order summary, selects a payment
method (single selection), agrees to the terms (boolean choice), and submits
the order. With no payment selected or terms unchecked, the submit action is
disabled and an inline constraint message is shown. On success navigate to a
confirmation page; on failure show an error.

## 语义要点

- 一个 **Payment** / checkout capability
- 一个 **payment-method** Input (single-selection)，source 自 data
- 一个 **agree-to-terms** Input (boolean-choice)
- 一个 **submit** Action (priority primary) — disabled by constraint
- 一个 **placed / failed / processing** state
- 一个 **error-message Feedback**
- 一个 **Decision** 成功→navigation、失败→feedback
- 不应出现 "Cart" 命名（这是 checkout 不是 cart）、不应出现 "Btn"
