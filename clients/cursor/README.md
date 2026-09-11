# Cursor

使用原生 Agent Skills：个人级 `~/.cursor/skills/<name>/SKILL.md`，项目级 `.cursor/skills/<name>/SKILL.md`。

```bash
python3 scripts/install.py --client cursor --skills report-writing --apply
```

通过技能选择或任务描述使用，例如“使用 report-writing 优化本周项目汇报”。Skills 按相关性发现与加载，适合这组任务型指导；不转换为始终生效的 Rules，也不额外生成 `.cursor/rules/*.mdc`。

安装脚本复制完整技能目录。`agents/openai.yaml` 是 Codex 的可选 UI 元数据，Cursor 使用 `SKILL.md` 的名称、描述与内容。Axiom 中的 `AskQuestion` 是交互意图示例，使用当前版本可用的问答能力。

[官方规范](https://cursor.com/docs/context/skills) · 核对日期：2026-09-11。
