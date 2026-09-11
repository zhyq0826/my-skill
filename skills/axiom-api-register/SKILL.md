---
name: axiom-api-register
description: "Register APIs to axiom from source code. Use when the user asks to register, import, or scan APIs into axiom, or says '注册 API', '导入接口', '扫描 API'."
---

# Axiom API 注册

帮助开发者从代码中识别 API 定义，通过 axiom MCP Server 注册到 axiom 项目。适用于开发阶段无 Swagger 文档的场景。

## 客户端兼容

文中的 `AskQuestion` 表示向用户提出选择，并非必须存在的工具名。使用客户端可用的问答工具；没有时用简短文字提问。沿用用户已明确指定的工作区、项目及操作范围；只有缺少必要信息时才询问。MCP 需单独配置，本仓库不包含凭据；以实际服务暴露的工具参数为准。

## 前置条件

用户需在所用客户端中配置指向 axiom 的 MCP endpoint。**配置文件路径因客户端而异**（Cursor 常用 `.cursor/mcp.json`，全局多为 `~/.cursor/mcp.json`）。

示例（服务端若在局域网部署）：

```json
{
  "mcpServers": {
    "axiom": {
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer <jwt-token>"
      }
    }
  }
}
```

桌面版通常仅需 `"url"`，无需 `headers`。具体请以用户在「设置 → MCP 助手集成」页面展示的片段为准。

如未配置，指导用户在所选 MCP 客户端中添加上述配置；端口与鉴权头按实际 axiom 部署调整。

---

## 工作流程

### Step 1: 选择工作区

调用 `list_workspaces` 获取所有工作区：

```
Tool: list_workspaces
Input: {}
```

**根据返回结果执行以下逻辑（不得跳过）：**

- **只有 1 个工作区**：直接使用其 `org_id`，无需询问，进入 Step 2
- **有多个工作区**：使用 `AskQuestion` 工具以**可点击选项**形式让用户选择：
  - 每个工作区作为一个选项，`id` 为工作区的 `org_id`，`label` 为工作区名称
  - **必须等用户点击选择后，再继续**

### Step 2: 选择项目

使用 Step 1 选定的 `org_id` 调用 `list_projects`：

```
Tool: list_projects
Input: { "org_id": "<选定的 org_id>" }
```

**根据返回结果执行以下逻辑（不得跳过）：**

- **只有 1 个项目**：直接使用其 `id`，无需询问，进入 Step 3
- **没有项目**：告知用户该工作区下没有项目，请先在 axiom 中创建项目
- **有多个项目**：使用 `AskQuestion` 让用户**点击选择**

### Step 3: 探测信源并提取 API

**⚠️ 关键原则：AI 从裸代码手工推导 schema 是最低质量的做法，只作兜底。必须优先寻找更可靠的信源。**

按以下优先级探测，找到高优先级信源后立即切换策略，不再往下找：

#### 优先级 1 — 已有机器可读 schema（最佳）

检查是否存在：
- `openapi.yaml` / `openapi.json` / `swagger.yaml` / `swagger.json`
- 任何 `docs/api*.yaml`、`api-spec.*` 等命名文件

**若找到**：直接解析该文件获取 endpoints、request/response schema，**跳过代码扫描**。

#### 优先级 2 — 代码生成型契约文件（次佳）

检查是否存在：
- **goctl（Go）**：`_service_api/*.api` 或 `_gateway_api/*.api` 文件
- **Protobuf**：`*.proto` 文件（含 `option (google.api.http)`）
- **Thrift**：`*.thrift` 文件

**若找到**：
1. 询问用户是否有对应的 schema 生成脚本（如 `make gen_xxx` 输出带 schema 的 JSON，或项目内 `scripts/` 下的工具）
2. 若有，运行脚本获取 JSON 格式的 payloads，直接使用；**不走 AI 手工推导**
3. 若没有：从契约文件里读取 endpoint 列表和类型定义，再结合对应的生成类型文件（如 `types/*types/types.go`）提取字段，比直接读 handler 代码可靠得多

#### 优先级 3 — 强类型注解代码（较可靠）

适用于：
- **TypeScript / Python**：有明确 interface / dataclass / Pydantic model 的项目
- **Java/Kotlin Spring**：有 `@RequestBody DTO`、`@ResponseBody` 注解的项目
- **Go**：handler 里有明确的 `var req SomeStruct` + struct 定义在同包

读取类型定义文件（不是 handler 文件），提取字段、json tag、注释。

#### 优先级 4 — 裸代码扫描（兜底，质量最低）

仅当以上均不适用时，扫描 routes 注册文件 + handler 文件推导 schema。

**使用此路径时，必须在用户确认前明确告知**：
> ⚠️ 当前只能从裸代码推导 schema，准确率有限。建议提供 OpenAPI 文档或类型定义文件以获得更准确的结果。

---

**框架识别参考（适用于优先级 3/4）：**

| 框架 | 路由注册特征 | 类型定义位置 |
|------|------------|------------|
| Go/Gin | `r.GET()`, `r.POST()` | handler 参数 struct |
| Go/goctl | `_service_api/*.api` | `types/*types/types.go` |
| Flask | `@app.route()`, `@blueprint.route()` | Pydantic/marshmallow schema 文件 |
| FastAPI | `@app.get()`, `@router.post()` | 函数参数 Pydantic model |
| Express.js | `router.get()`, `app.post()` | TypeScript interface 文件 |
| Spring | `@GetMapping`, `@PostMapping` | DTO class 文件 |
| NestJS | `@Get()`, `@Post()`, `@Controller()` | DTO class 文件 |

### Step 4: Schema 质量检查

提取完所有 API 后，在进入确认前，**必须做质量检查**：

计算「schema 降级率」= 字段中 `additionalProperties: true`（无具体 properties）的比例。

- **降级率 0–30%**：可以继续，在确认界面标注哪些字段是不透明类型
- **降级率 30–60%**：在确认前**警告用户**，说明哪些 API 的 schema 质量较低，建议提供类型定义
- **降级率 > 60%**：**必须暂停**，向用户说明原因，提供以下选项：
  ```
  AskQuestion:
    title: "Schema 质量不足，如何继续？"
    questions:
      - id: "action"
        prompt: "超过 60% 的字段无法解析为具体类型，注册后 API 文档价值有限。"
        options:
          - id: "provide"
            label: "我来提供 OpenAPI 文档 / 类型定义文件"
          - id: "continue"
            label: "知道了，仍然继续（仅注册路由结构）"
          - id: "abort"
            label: "取消本次注册"
  ```

### Step 5: Diff — 与已注册 API 对比

注册前，调用 `list_apis` 获取项目现有 API：

```
Tool: list_apis
Input: { "project_id": "<项目 ID>" }
```

将待注册列表与现有列表按 `method + path` 对比，分为三类：
- `[new]`：全新 API，直接注册
- `[update]`：method + path 已存在，将覆盖 schema
- `[skip]`：（仅当用户选择跳过已有时）

若有 `[update]` 条目，询问用户策略：

```
AskQuestion:
  title: "部分 API 已存在"
  questions:
    - id: "update_policy"
      prompt: "发现 N 条 API 已在项目中注册，如何处理？"
      options:
        - id: "overwrite"
          label: "覆盖更新所有已存在的"
        - id: "skip"
          label: "跳过已存在的，只注册新增"
        - id: "ask"
          label: "逐条决定"
```

### Step 6: 分组确认

**不得将超过 10 条 API 塞入单个确认 prompt。** 按 module / 路由前缀分组，每组展示路径清单（不展示完整 schema 内容，太长无法阅读）。

格式示例：

```
即将注册以下 API 到项目「用户中心」：

[new] POST   /api/v1/users/login         — 用户登录
[new] POST   /api/v1/users/register      — 用户注册
[update] GET /api/v1/users/{id}          — 获取用户信息（将覆盖已有 schema）
[skip] DELETE /api/v1/users/{id}         — 删除用户（已存在，跳过）

共 4 条：新增 2 / 覆盖 1 / 跳过 1
```

如果总数超过 10 条，先告知总数与分组情况，再按组询问确认：

```
AskQuestion:
  title: "确认注册 — [module 名] (1/3)"
  questions:
    - id: "confirm_group_1"
      prompt: "以下 6 条 API 属于 [module]：\n\n[路径清单]"
      options:
        - id: "yes"
          label: "确认注册这组"
        - id: "skip"
          label: "跳过这组"
        - id: "abort"
          label: "终止整个注册"
```

### Step 7: 注册并打进度

用户确认后，逐个调用 `register_api`，**每注册完 5 条输出一次进度**：

```
Tool: register_api
Input: {
  "project_id": "<选定的项目 ID>",
  "method": "POST",
  "path": "/api/users",
  "module": "users",
  "description": "创建用户",
  "handler": "CreateUserHandler",
  "request_body_schema": { "type": "object", "properties": { ... } },
  "response_body_schema": { "type": "object", "properties": { ... } }
}
```

进度输出格式（每 5 条或每组结束后）：
```
注册进度：12 / 30 完成（✓ 10 成功  ✗ 2 失败）
```

`register_api` 失败时**记录错误继续**，不中断整体流程。

### Step 8: 汇总报告

所有 API 处理完成后，输出最终报告：

```
注册完成 ✓

项目：用户中心（p-001）
━━━━━━━━━━━━━━━━━━━
新增成功：12 条
覆盖成功：3 条
跳过（已存在）：5 条
失败：1 条

失败详情：
  - POST /api/v1/admin/reset — project_id 无权限

建议：调用 list_apis 验证结果，或在 axiom 界面查看。
```

---

## Module 推导规则（优先级从高到低）

1. 显式标注：`@server(group: xxx)`、`@tag xxx`、Spring `@RequestMapping("/xxx")` 类级别
2. 路由前缀末段：`/api/v1/users/...` → `users`；`/account/httpapi/...` → `account`
3. 文件名：`user_handler.go` → `user`；`UserController.java` → `user`
4. 兜底：`default`

---

## Schema 推导规则（优先级 3/4 路径使用）

1. **类型映射：** string→`"string"`, int/int64→`"integer"`, float→`"number"`, bool→`"boolean"`, 数组→`"array"`
2. **嵌套对象：** 递归推导为 `{"type":"object","properties":{...}}`；若无法解析内部字段，标为 `{"type":"object","additionalProperties":true,"description":"opaque — 无法解析类型 Foo"}` 并计入降级率
3. **JSON tag：** 优先用 json tag 的字段名（如 `json:"user_name"` → `user_name`）；缺省则用字段名本身
4. **必填字段：** `required` / `binding:"required"` / 非 optional 标记 → 加入 `required` 数组
5. **描述：** 字段注释作为 `description`
6. **禁止使用空 schema：** 不得提交 `{}` 或仅含 `"type":"object"` 无 `properties` 的 schema；若真无法推导，使用带 description 的占位形式并告知用户

---

## 错误处理

- `register_api` 失败时记录错误并继续注册后续 API
- 最终报告成功/失败清单（见 Step 8）
- 常见错误：project_id 不存在、method 不合法、path 为空、Token 过期

### Token 过期（服务端版）

服务端版 MCP Server 需要 JWT Token 认证（有效期 90 天）。当 Token 过期时，MCP tool 调用会返回包含以下关键词的错误：

- `Token 已过期`
- `401`
- `请重新登录 Axiom 获取新 Token`

**当识别到上述错误时，必须立即停止操作并告知用户：**

```
⚠️ Axiom MCP Server 认证失败：Token 已过期。

请按以下步骤更新：
1. 在浏览器中重新登录 Axiom
2. 打开「设置 → MCP 助手集成」，复制最新的 MCP 配置片段（含 Authorization）
3. 将 MCP 客户端里指向 axiom 的配置替换为该片段（例如 Cursor：编辑 ~/.cursor/mcp.json 或项目 .cursor/mcp.json 中的对应条目）
4. 保存后按客户端要求重载 MCP 或重启客户端
```

桌面版无需 Token，不会遇到此问题。
