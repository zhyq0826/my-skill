# My Skills

个人使用与定制的技能集，适配 **Cursor、Codex、Claude Code**。

采用标准 `SKILL.md` 保存一份内容，通过安装脚本分发到各客户端目录。保留原有中英文写作风格；不为三个客户端复制维护三套规则。

## 技能目录

| 方向 | 技能 | 用途 |
| --- | --- | --- |
| 写作 | [interview-notes](skills/interview-notes/SKILL.md) | 通用访谈整理、背景与案例、观点归属 |
| 写作 | [report-writing](skills/report-writing/SKILL.md) | 工作汇报、数字口径、语言风格和建设建议 |
| 研发 | [code-simplifier](skills/code-simplifier/SKILL.md) | 保持行为的代码简化 |
| Flutter | [flutter-design](skills/flutter-design/SKILL.md) | 界面视觉、主题与组件设计 |
| Flutter | [flutter-layout](skills/flutter-layout/SKILL.md) | 约束、响应式与布局 |
| Flutter | [flutter-animation](skills/flutter-animation/SKILL.md) | 动画选型、控制器与动效实现 |
| 设计 | [interaction-design](skills/interaction-design/SKILL.md) | 状态、反馈、过渡和微交互 |
| 设计 | [ops-admin-design](skills/ops-admin-design/SKILL.md) | 运营后台、信息密度、权限与批量操作 |
| Axiom | [axiom-api-register](skills/axiom-api-register/SKILL.md) | 从接口契约或代码注册 API |
| Axiom | [axiom-scene-register](skills/axiom-scene-register/SKILL.md) | 注册多步骤 API 测试场景 |

## 安装

需要 Python 3.9+。脚本默认只预览，添加 `--apply` 才写入；不覆盖已有同名技能，不修改模型、MCP 或全局规则配置。

```bash
git clone git@github.com:zhyq0826/my-skill.git
cd my-skill

# 查看可用技能
python3 scripts/install.py --list

# Codex：预览，然后安装两项写作技能
python3 scripts/install.py --client codex --skills interview-notes report-writing
python3 scripts/install.py --client codex --skills interview-notes report-writing --apply

# Cursor：选择 Flutter 技能
python3 scripts/install.py --client cursor --skills flutter-design flutter-layout flutter-animation --apply

# Claude Code：安装全部
python3 scripts/install.py --client claude --apply

# 项目级安装；省略 --project 时安装到个人目录
python3 scripts/install.py --client cursor --project /path/to/project --skills report-writing --apply
```

遇到已有技能时，先比较差异并自行备份处理，再运行安装。脚本以复制方式安装，后续 `git pull` 不会自动覆盖已安装文件。

## 三种客户端

| 客户端 | 个人目录 | 项目目录 | 适配说明 |
| --- | --- | --- | --- |
| [Cursor](clients/cursor/README.md) | `~/.cursor/skills/` | `.cursor/skills/` | 使用原生 Skills；不强制加载为 `.mdc` 规则 |
| [Codex](clients/codex/README.md) | `~/.agents/skills/` | `.agents/skills/` | 按官方共享目录规范安装，包含 `agents/openai.yaml` |
| [Claude Code](clients/claude/README.md) | `~/.claude/skills/` | `.claude/skills/` | 原生 Skills，支持 `/技能名` 调用 |

Cursor 也会发现共享目录及部分兼容目录。多客户端共用同一台机器时，选择一个合适安装位置，避免重复安装同名技能。已有 `~/.codex/skills` 安装也应先检查，避免与共享目录重复。

## 维护

```text
skills/             # 唯一技能源文件，含必要的示例、Schema 与 UI 元数据
clients/            # 各工具安装目录与使用方式
catalog.json        # 分类、来源与依赖清单
scripts/install.py  # 预览与安全复制安装
tests/              # 安装路径、冲突与完整性检查
```

修改 `skills/` 后运行 `python3 -m unittest discover -s tests -v`。新增技能需同步 `catalog.json` 和上表。技能仅在被选用时提供指导，不作为仓库根级 `AGENTS.md` 或 `CLAUDE.md` 全局强制规则。

Axiom 技能需要用户自行配置对应 MCP 服务；安装文件不会接入或写入任何业务系统。Flutter 技能需要目标项目具有 Flutter SDK 与相应依赖。

## 来源

本仓库是个人配置集，不宣称所有内容原创。访谈与汇报技能由个人需求和实际反馈整理；其余取自个人已安装配置，详见 [来源与整理范围](SOURCES.md)。未对来源未核实的内容统一授予新的开源许可证。
