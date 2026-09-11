# 场景 Schema 参考

`register_scene` 参数与 `model.Scene` / `model.Step` 对齐。

## Scene 顶层字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `space_id` | 是 | 编排空间 ID（来自 `list_spaces`） |
| `name` | 是 | 场景名称 |
| `description` | 否 | 描述 |
| `tags` | 否 | 标签数组 |
| `source` | 否 | `manual`（默认）/ `nlp` / `test_matrix` |
| `variables` | 建议 | 场景变量，建议含 `baseUrl` |
| `steps` | 是 | 步骤数组，至少 1 步 |
| `common_params` | 否 | 公共 headers/query/body |
| `continue_on_failure` | 否 | 默认 false |
| `default_assertion_failure_policy` | 否 | `strict`（默认）/ `soft_success` |
| `scene_id` | 更新时 | 传入则覆盖更新 |
| `project_id` | 否 | 用于校验 API 是否已注册 |

## Variable

```json
{"name": "baseUrl", "value": "http://localhost:8080", "type": "static"}
```

`type` 取值：`static` | `dynamic` | `extract` | `mcp`

## Step

步骤 **不要** 传 `id` / `scene_id`（MCP 入参已省略）。落库时由服务层按 `request.method` + `request.path` 自动生成，格式为 `{method}_{path_slug}_{xx}`，例如 `post_api_users_login_ab`，与编辑器 / NLP 编排一致。

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 步骤名称 |
| `order` | 是 | 从 0 开始的顺序 |
| `phase` | 是 | `setup` / `main` / `teardown` |
| `request` | 是 | 含 `method`、`path`；可选 `headers`、`query`、`body` |
| `assertions` | 建议 | 断言数组 |
| `extract_script` | 否 | JS 脚本，须 `return { varName: value }` |
| `dependencies` | 否 | 依赖的步骤 ID 数组（由服务层按 method+path 自动分配，勿手写 UUID） |
| `skip` | 否 | 是否跳过 |
| `project_id` | 否 | 集成场景下指定 API 所属项目 |

## RequestConfig

```json
{
  "method": "POST",
  "path": "/api/users/login",
  "headers": {"Content-Type": "application/json"},
  "query": {"page": "1"},
  "body": {"email": "test@example.com", "password": "secret"}
}
```

`body` 支持 `{{variable}}` 占位符。

## Assertion

```json
{"type": "status", "operator": "eq", "expected": 200}
```

```json
{"type": "jsonpath", "operator": "exists", "path": "$.data.token"}
```

`type`：`status` | `jsonpath` | `header` | `response_time` | `body_contains` | `body_equals`

`operator`：`eq` | `ne` | `gt` | `lt` | `gte` | `lte` | `contains` | `exists` | `not_exists` | ...

## CommonParams

```json
{
  "headers": {"X-Request-Id": "{{traceId}}"},
  "query": {"locale": "zh-CN"},
  "body": {"source": "axiom"}
}
```
