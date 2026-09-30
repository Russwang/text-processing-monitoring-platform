# 容器化文本处理与服务监测平台

这是基于云计算课程作业整理的作品集项目。六个独立服务通过网关处理文字；文本存储服务使用 SQLite；监控模块每分钟检查服务的预期答案和请求耗时。

## 运行

安装 Docker 和 Docker Compose 后，在仓库根目录执行：

```bash
cp .env.example .env
docker compose up --build -d
```

打开 http://localhost:8080。首次运行需要下载镜像和依赖。

```bash
python3 scripts/smoke_test.py
docker compose down
```

停止容器会保留两个 SQLite 数据卷。可在 `.env` 配置网页端口及可选的 `DISCORD_WEBHOOK_URL`，告警默认关闭。

## 功能和技术

- PHP 单词统计、Node.js 字符统计、Python 元音统计、Go 逗号统计、Ruby 独立单词 and 统计、Java 回文词统计。
- Flask 网关支持配置路由、手动重载、服务健康检查、超时及上游错误处理。
- 文本存储 API 支持指定 ID 保存和读取，使用数据库主键防止并发重复写入。
- 监控验证固定样本的预期统计结果，测量同一次请求延迟，记录成功、失败和慢响应状态。
- Nginx 转发同源 API 请求，Compose 使用容器 DNS 和持久化数据卷，GitHub Actions 执行各语言测试及容器 HTTP 集成测试。

课程提供了最初的网页、PHP 和 Node.js 服务。本人课程贡献是新增四种语言服务、网关、存储、监控及前端扩展；后续作品集维护加入修复、部署和回归测试。详见 [贡献说明](../ATTRIBUTION.md)。

此项目没有实现或实测公有云部署、多云高可用、负载均衡、自动故障转移或生产级安全，不应在简历中写成已完成这些能力。

[英文说明](../README.md) · [API 文档](API.md) · [修复与验证报告](REPAIR_REPORT.md) · [简历与面试文案](RESUME_NOTES.md)
