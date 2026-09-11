# Claude Code

使用个人级 `~/.claude/skills/<name>/SKILL.md` 或项目级 `.claude/skills/<name>/SKILL.md`。

```bash
python3 scripts/install.py --client claude --skills report-writing --apply
```

通过 `/report-writing` 显式调用，或由 Claude 根据技能描述自动选择。各技能沿用标准 frontmatter；不转换成 subagent，也不把全部内容塞入根目录 `CLAUDE.md`。

`agents/openai.yaml` 仅为 Codex UI 元数据。需要外部工具的技能仍依赖 Claude Code 中单独配置的 MCP 服务；文中的交互工具名称按当前可用工具执行，没有选择工具时用文字询问。

这里的 Claude 适配指 **Claude Code**。Claude 网页及 API 的技能上传与运行方式不在本安装脚本范围内。

[官方规范](https://code.claude.com/docs/en/skills) · 核对日期：2026-09-11。
