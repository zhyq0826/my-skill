# 来源与整理范围

本次按“个人原创 / 定制配置”范围整理，不把已安装技能全部视为原创。

| 内容 | 来源 | 本次处理 |
| --- | --- | --- |
| interview-notes、report-writing | 个人实际写作需求与反馈整理 | 保留拆分后的通用版本与 Codex UI 元数据 |
| code-simplifier | 个人 Codex 配置，与 Cursor 同名版本一致 | 保留规则，补充 UI 元数据 |
| Flutter 三项、interaction-design、ops-admin-design | 个人 Cursor 配置 | 保留主要内容，移除 Flutter 原文件的生成模型与生成时间元数据 |
| Axiom 两项 | 个人 Cursor 配置 | 保留 Schema 与示例；问答交互改为跨客户端兼容说明；示例密码改为占位符 |

个人已安装配置及项目技能未提供足以确认全部上游作者和许可证的完整信息。这里记录配置来源，不声明其原创归属，也不新增覆盖所有文件的许可证。Flutter 视觉设计文本与常见前端设计技能风格相近，后续确认上游后应补齐准确归属及许可。

未收录个人目录中的第三方整套发行包（如 baoyu、Superpowers、Superset），也未复制其符号链接、工具凭据、历史对话或公司访谈材料。`frontend-design` 等第三方技能建议从上游安装，避免当作个人原创重新分发。

原技能内的任务规则保留为个人配置，不代表已验证其全部技术示例；本次验证涵盖文件结构、引用、安装和跨客户端目录适配。Axiom 的真实接口需以使用时的 MCP schema 为准。

## 项目技能的通用化提炼

从用户指定的 `service_base` 仓库只读提炼；跨客户端重复版本归并为一份标准技能，以 `.agents/skills` 版本为主要材料，结合其他副本核对。前端影响分析来自子项目的 Cursor 技能。源仓库未修改。

| 原技能 | 通用技能 | 主要处理 |
| --- | --- | --- |
| `candidate-interview-evaluator` | `candidate-interview-evaluator` | 保留岗位与证据链，评分阈值改为遵循岗位标准 |
| `no-cryptic-abbreviations-governance` | `go-naming-governance` | 移除项目规则路径，保留语义命名与契约保护 |
| `requirements-change-engineering` | `requirements-change-engineering` | 去除指定服务与命令，按真实消费者和存量判断迁移 |
| `service-logging-err-governance` | `service-error-governance` | 去除自定义错误库依赖，先确认日志观测责任 |
| `ops-panel-guidance` | `ops-panel-guidance` | 提炼说明、选项、确认与指南，不绑定组件库和业务枚举 |
| `service-base-i18n-governance` | `i18n-governance` | 移除包路径与方法硬约束，按消息接收者确定语言 |
| `prd-to-engineering` | `prd-to-engineering` | 保留生命周期账本和垂直切片，移除固定审批门控 |
| `ops-frontend-impact` | `frontend-impact-analysis` | 保留显式调用和代码影响矩阵，去除固定前端目录 |
| `service-base-relation-growth-json` | `spreadsheet-to-config` | 重新整理输入契约与校验方法，不复制业务枚举及专用脚本 |

未重复收录 `mongodb-query-optimizer`：源文件已是标注 Apache-2.0 的通用技能，本次不将第三方技能重新包装为个人能力。未复制业务数据、接口地址、人员信息、内部架构实例或本机路径。以上通用化内容为方法提炼，不等同于原项目规则的完整镜像，也未新增全仓统一许可证。
