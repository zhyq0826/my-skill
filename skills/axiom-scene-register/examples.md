# register_scene 示例

## 示例 1：登录 + 查用户（两步骤）

```json
{
  "space_id": "sp-001",
  "project_id": "p-001",
  "name": "登录后查询用户详情",
  "description": "先登录获取 token，再带 token 查询当前用户",
  "variables": [
    {"name": "baseUrl", "value": "http://localhost:8080", "type": "static"}
  ],
  "steps": [
    {
      "name": "用户登录",
      "order": 0,
      "phase": "main",
      "request": {
        "method": "POST",
        "path": "/api/users/login",
        "headers": {"Content-Type": "application/json"},
        "body": {
          "email": "zhangsan@example.com",
          "password": "<test-password>"
        }
      },
      "assertions": [
        {"type": "status", "operator": "eq", "expected": 200},
        {"type": "jsonpath", "operator": "exists", "path": "$.data.token"}
      ],
      "extract_script": "const b = JSON.parse(response.body); return { token: b.data.token };"
    },
    {
      "name": "查询用户详情",
      "order": 1,
      "phase": "main",
      "request": {
        "method": "GET",
        "path": "/api/users/me",
        "headers": {
          "Authorization": "Bearer {{token}}"
        }
      },
      "assertions": [
        {"type": "status", "operator": "eq", "expected": 200},
        {"type": "jsonpath", "operator": "exists", "path": "$.data.email"}
      ]
    }
  ]
}
```

## 示例 2：单步冒烟

```json
{
  "space_id": "sp-001",
  "project_id": "p-001",
  "name": "健康检查",
  "variables": [
    {"name": "baseUrl", "value": "http://localhost:8080", "type": "static"}
  ],
  "steps": [
    {
      "name": "Ping",
      "order": 0,
      "phase": "main",
      "request": {"method": "GET", "path": "/health"},
      "assertions": [
        {"type": "status", "operator": "eq", "expected": 200}
      ]
    }
  ]
}
```

## 示例 3：覆盖更新已有场景

先 `list_scenes` 拿到 `scene_id`，再：

```json
{
  "scene_id": "scene-abc123",
  "space_id": "sp-001",
  "name": "登录后查询用户详情（v2）",
  "variables": [
    {"name": "baseUrl", "value": "http://localhost:8080", "type": "static"}
  ],
  "steps": [
    {
      "name": "用户登录",
      "order": 0,
      "phase": "main",
      "request": {
        "method": "POST",
        "path": "/api/users/login",
        "body": {"email": "admin@example.com", "password": "<test-password>"}
      },
      "assertions": [{"type": "status", "operator": "eq", "expected": 200}],
      "extract_script": "const b = JSON.parse(response.body); return { token: b.data.token };"
    }
  ]
}
```

## 从场景 JSON 文件导入

仓库内 `scenes/login-flow.json`：

```json
{
  "name": "登录流程",
  "variables": [{"name": "baseUrl", "value": "http://localhost:8080", "type": "static"}],
  "steps": []
}
```

调用时补上 `space_id` 和 `project_id`：

```json
{
  "space_id": "<来自 list_spaces>",
  "project_id": "<来自 list_projects>",
  "name": "登录流程",
  "variables": [],
  "steps": []
}
```
