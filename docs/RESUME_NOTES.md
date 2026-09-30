# Resume and interview notes

Project: **Containerised Text Processing and Monitoring Platform**
中文：**容器化文本处理与服务监测平台**
Repository: https://github.com/Russwang/text-processing-monitoring-platform

## English bullets

- Extended a coursework text editor with four containerised services in Python, Go, Ruby and Java, implementing vowel, comma, standalone-word and palindrome counting alongside the supplied PHP and Node.js services.
- Built a configurable Flask gateway and SQLite-backed text save/retrieve APIs; added request timeouts, upstream error propagation, atomic duplicate-ID rejection and regression tests for asynchronous frontend requests.
- Implemented periodic expected-answer checks and latency monitoring for six services, SQLite health history and optional webhook alerts; packaged the application with Docker Compose and GitHub Actions for language tests and HTTP integration checks.

## 中文条目

- 在课程提供的 PHP/Node.js 文本服务基础上，使用 Python、Go、Ruby、Java 新增四个容器化统计服务，实现元音、逗号、独立单词 and 及回文词统计。
- 开发配置驱动的 Flask 网关与 SQLite 文本保存/读取 API，完善请求超时、上游错误传递、重复 ID 原子校验及前端异步请求回归测试。
- 为六个服务实现周期性预期答案检查、请求延迟监测、SQLite 状态历史及可选 Webhook 告警，并使用 Docker Compose 和 GitHub Actions 配置部署、语言测试与 HTTP 集成验证。

## Interview boundaries

Explain the supplied starter components separately from your own coursework contribution and the later AI-assisted portfolio repairs. Do not claim production traffic, performance improvements, AWS/GCP deployment, failover or measured high availability. State whether CI has actually passed using the repository's current Actions results. The original assignment's multi-cloud material was a design proposal.
