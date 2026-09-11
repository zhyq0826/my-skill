# Codex

按官方共享技能目录安装：个人级 `~/.agents/skills/<name>/SKILL.md`，项目级 `.agents/skills/<name>/SKILL.md`。

```bash
python3 scripts/install.py --client codex --skills interview-notes report-writing --apply
```

调用示例：`$interview-notes`、`$report-writing`。每个技能包含 `agents/openai.yaml`，提供中文展示名与默认提示词；保持默认的自动发现行为，不固定模型和推理强度。

部分已有桌面配置将技能放在 `~/.codex/skills`。本仓库使用官方当前推荐的 `.agents/skills`，不会自动搬迁旧目录；安装前应自行检查同名技能。自定义目标目录可使用 `--dest /path/to/skills`。

[官方规范](https://developers.openai.com/codex/skills/) · 核对日期：2026-09-11。
