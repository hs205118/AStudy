# AStudy AVF

`self-test.ps1` 是 Windows 无交互自检入口。所有用例 ID 登记在 `validation/registry/cases.json`，ID 永不复用。报告同时输出静态 HTML 和可提交给 AI 的 ZIP 包。运行时数据库、端口和 Artifact 均隔离于 `.avf`。
