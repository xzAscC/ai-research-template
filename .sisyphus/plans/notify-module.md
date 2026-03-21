# Python 通知模块 (Resend)

## TL;DR

> **Quick Summary**: 在 Copier 模板中添加 `notify` 子模块，使用 Resend API 在任务完成后发送 HTML 邮件通知，包含任务状态、日志、耗时和证据附件。采用 TDD 开发。
> 
> **Deliverables**:
> - `template/{{project_name_snake}}/notify/` 模块（4 个核心文件）
> - `template/tests/test_notify/` 测试套件（4 个测试文件）
> - 更新 `pyproject.toml.jinja` 添加 resend 依赖
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: T1(pyproject) → T2(测试) → T3-T6(实现) → T7(集成)

---

## Context

### Original Request
创建一个 Python 通知模块，在每个任务完成后通过 Resend API 发送邮件，包含任务名称、运行状态、日志、耗时和证据文件附件。

### Interview Summary
**Key Discussions**:
- **邮件服务**: Resend API
- **邮件格式**: HTML（内联 CSS，表格布局）
- **模块位置**: 模板内 `template/{{project_name_snake}}/notify/`
- **触发场景**: Sisyphus 任务完成 + 外部脚本调用
- **证据处理**: 自动扫描 `.sisyphus/evidence/` + 手动指定路径
- **错误处理**: 失败重试 3 次，指数退避
- **数据处理**: 日志截断 + 敏感数据过滤（API key、密码）
- **测试策略**: TDD

**Research Findings**:
- Resend 限制：40MB 邮件大小、5 req/s 速率
- 阻止文件类型：.exe, .bat, .js, .ps1 等
- 附件格式：`content: list[bytes]`（非 raw bytes）
- Resend SDK 异常类型：`MissingApiKeyError`, `RateLimitError`, `ValidationError`, `ApplicationError`

### Metis Review
**Identified Gaps** (addressed):
- **模块位置澄清**: 确认放在模板内，每个生成项目自带通知功能
- **日志截断**: 需要限制行数/字符数，防止邮件过大
- **敏感数据过滤**: 需要 redact API keys、密码等
- **HTML 安全**: 必须使用 `html.escape()` 防止注入
- **附件过滤**: 跳过 Resend 阻止的文件扩展名

---

## Work Objectives

### Core Objective
在 Copier 模板中添加可复用的邮件通知模块，使用 Resend API，支持任务完成通知、日志截断、敏感数据过滤和证据附件。

### Concrete Deliverables
- `template/{{project_name_snake}}/notify/__init__.py` - 模块入口，导出 `send_task_notification`
- `template/{{project_name_snake}}/notify/core.py` - 主函数实现
- `template/{{project_name_snake}}/notify/email_template.py` - HTML 邮件生成
- `template/{{project_name_snake}}/notify/evidence.py` - 证据目录扫描
- `template/tests/test_notify/` - 测试套件（4 个文件）
- `template/pyproject.toml.jinja` - 更新依赖

### Definition of Done
- [ ] `uv run pytest template/tests/test_notify/ -v` 全部通过
- [ ] `uv run mypy template/{{project_name_snake}}/notify --strict` 无错误
- [ ] 从模板生成新项目，通知模块可用
- [ ] 实际发送测试邮件到 `NOTIFICATION_EMAIL` 成功

### Must Have
- `send_task_notification()` 函数，参数：task_name, status, logs, duration, attachment_paths, evidence_dir
- 3 次重试 + 指数退避（1s, 2s, 4s）
- 日志截断（默认 500 行）
- 敏感数据过滤（API key、密码、token）
- HTML 邮件（内联 CSS）+ 纯文本回退
- 类型提示 + Google-style docstrings

### Must NOT Have (Guardrails)
- 不要添加 async/await（同步实现）
- 不要添加 CLI 接口（仅库）
- 不要添加邮件队列/调度
- 不要添加配置文件（仅环境变量）
- 不要添加 CC/BCC 支持
- 不要使用 Jinja2 模板引擎（f-string 足够）
- 不要附加 .exe, .bat, .js, .ps1 等阻止文件类型

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: YES (pytest 在模板中)
- **Automated tests**: TDD
- **Framework**: pytest + pytest-mock
- **Each task follows**: RED (failing test) → GREEN (minimal impl) → REFACTOR

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — 依赖 + 测试骨架):
├── Task 1: 更新 pyproject.toml.jinja 添加 resend 依赖 [quick]
├── Task 2: 创建测试骨架 tests/test_notify/ [quick]
└── Task 3: 创建模块骨架 notify/__init__.py [quick]

Wave 2 (After Wave 1 — 核心实现，MAX PARALLEL):
├── Task 4: 实现 evidence.py (证据扫描 + 过滤) [quick]
├── Task 5: 实现 email_template.py (HTML 生成) [quick]
├── Task 6: 实现 core.py (主函数 + 重试) [unspecified-high]
└── Task 7: 实现敏感数据过滤 [quick]

Wave 3 (After Wave 2 — 集成 + 验证):
├── Task 8: 模块导出 + 类型完整 [quick]
└── Task 9: 集成测试 + 实际邮件发送 [unspecified-high]

Critical Path: T1 → T2 → T4-T7 → T8 → T9
Parallel Speedup: ~50% faster than sequential
Max Concurrent: 4 (Wave 2)
```

### Dependency Matrix

- **1**: — — 2, 3, 4, 5, 6, 7, 8, 9
- **2**: 1 — 4, 5, 6, 7
- **3**: 1 — 8
- **4**: 2 — 6
- **5**: 2 — 6
- **6**: 2, 4, 5 — 8
- **7**: 2 — 6
- **8**: 3, 6 — 9
- **9**: 8 —

### Agent Dispatch Summary

- **Wave 1**: **3** — T1-T3 → `quick`
- **Wave 2**: **4** — T4-T5, T7 → `quick`, T6 → `unspecified-high`
- **Wave 3**: **2** — T8 → `quick`, T9 → `unspecified-high`

---

## TODOs

- [x] 1. 更新 pyproject.toml.jinja 添加 resend 依赖

  **What to do**:
  - 在 `[dependency-groups].dev` 添加 `pytest-mock>=3.12.0`
  - 添加新 `[project.dependencies]` 段，包含 `resend>=2.0.0`
  - 保持现有格式和变量插值

  **Must NOT do**:
  - 不要改变现有依赖顺序
  - 不要删除任何现有配置

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单配置文件修改
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 2-9 (所有后续任务)
  - **Blocked By**: None

  **References**:
  - `template/pyproject.toml.jinja` - 现有配置结构
  - Resend SDK: `https://github.com/resend/resend-python#installation`

  **Acceptance Criteria**:
  - [ ] `resend>=2.0.0` 在 `[project.dependencies]` 中
  - [ ] `pytest-mock>=3.12.0` 在 `[dependency-groups.dev]` 中
  - [ ] `uv sync` 在模板目录成功

  **QA Scenarios**:
  ```
  Scenario: 依赖安装成功
    Tool: Bash
    Steps:
      1. cd template && uv sync
      2. uv pip show resend
    Expected Result: Package resend found with version >=2.0.0
    Evidence: .sisyphus/evidence/task-01-deps-install.txt
  ```

  **Commit**: YES
  - Message: `feat(notify): add resend and pytest-mock dependencies`
  - Files: template/pyproject.toml.jinja

- [x] 2. 创建测试骨架 tests/test_notify/

  **What to do**:
  - 创建 `template/tests/test_notify/__init__.py`（空文件）
  - 创建 `template/tests/test_notify/test_core.py` - 主函数测试（先写 FAILING 测试）
  - 创建 `template/tests/test_notify/test_evidence.py` - 证据扫描测试（FAILING）
  - 创建 `template/tests/test_notify/test_email_template.py` - HTML 模板测试（FAILING）
  - 创建 `template/tests/test_notify/test_redact.py` - 敏感数据过滤测试（FAILING）
  - 每个测试文件包含 2-3 个基础测试用例框架

  **Must NOT do**:
  - 不要实现被测代码（TDD：测试先行）
  - 不要添加集成测试（Task 9）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 创建测试文件骨架
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Tasks 4-7 (需要测试先存在)
  - **Blocked By**: Task 1 (pyproject 需要先更新)

  **References**:
  - `template/tests/test_hello.py.jinja` - 现有测试结构参考

  **Acceptance Criteria**:
  - [ ] 4 个测试文件存在
  - [ ] `uv run pytest tests/test_notify/ -v` 显示 FAILING 测试（预期）

  **QA Scenarios**:
  ```
  Scenario: 测试文件结构正确
    Tool: Bash
    Steps:
      1. ls -la template/tests/test_notify/
    Expected Result: __init__.py, test_core.py, test_evidence.py, test_email_template.py, test_redact.py 存在
    Evidence: .sisyphus/evidence/task-02-test-structure.txt
  ```

  **Commit**: YES (groups with T3)
  - Message: `feat(notify): add test skeleton for TDD`
  - Files: template/tests/test_notify/

- [x] 3. 创建模块骨架 notify/__init__.py

  **What to do**:
  - 创建 `template/{{project_name_snake}}/notify/__init__.py`
  - 导出 `send_task_notification` 函数（stub，raise NotImplementedError）
  - 创建 `template/{{project_name_snake}}/notify/core.py`（stub）
  - 创建 `template/{{project_name_snake}}/notify/email_template.py`（stub）
  - 创建 `template/{{project_name_snake}}/notify/evidence.py`（stub）
  - 创建 `template/{{project_name_snake}}/notify/redact.py`（stub）
  - 添加基础类型定义

  **Must NOT do**:
  - 不要实现实际逻辑（仅 stub）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 创建模块骨架
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Tasks 4-8
  - **Blocked By**: Task 1

  **References**:
  - `template/{{project_name_snake}}/__init__.py.jinja` - 现有模块结构参考

  **Acceptance Criteria**:
  - [ ] `template/{{project_name_snake}}/notify/` 目录存在
  - [ ] 5 个 Python 文件存在
  - [ ] `from {{project_name_snake}}.notify import send_task_notification` 可导入（运行时报 NotImplementedError）

  **QA Scenarios**:
  ```
  Scenario: 模块导入成功
    Tool: Bash
    Steps:
      1. cd template && uv run python -c "from {{project_name_snake}}.notify import send_task_notification; send_task_notification('test', 'success', [], 1.0)"
    Expected Result: ImportError 或 NotImplementedError（stub 状态）
    Evidence: .sisyphus/evidence/task-03-module-import.txt
  ```

  **Commit**: YES (groups with T2)
  - Message: `feat(notify): add test skeleton for TDD`
  - Files: template/{{project_name_snake}}/notify/

- [x] 4. 实现 evidence.py (证据扫描 + 过滤)

  **What to do**:
  - 实现 `scan_evidence_dir(directory: Path) -> list[Path]` - 扫描目录返回有效文件路径
  - 实现 `filter_blocked_extensions(files: list[Path]) -> list[Path]` - 过滤 .exe, .bat, .js, .ps1 等
  - 实现 `prepare_attachments(paths: list[Path]) -> list[dict]` - 读取文件，转换为 Resend 格式 `{"filename": str, "content": list[bytes]}`
  - 空目录返回空列表并记录 warning 日志
  - 不存在的目录抛出 `EvidenceDirNotFoundError`
  - 写测试：test_scan_evidence_dir, test_filter_blocked_extensions, test_prepare_attachments, test_empty_dir, test_missing_dir

  **Must NOT do**:
  - 不要检查文件大小（<10MB，不需要）
  - 不要递归扫描（仅顶层文件）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 独立功能模块，逻辑清晰
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 6, 7)
  - **Blocks**: Task 6 (core 需要 evidence 模块)
  - **Blocked By**: Task 2 (测试需先存在)

  **References**:
  - Resend 附件格式: `https://resend.com/docs/api-reference/emails/send-email#attachments`
  - 阻止文件类型: .exe, .bat, .js, .ps1, .cmd, .com, .scr, .vbs, .jar

  **Acceptance Criteria**:
  - [ ] `uv run pytest tests/test_notify/test_evidence.py -v` 全部通过
  - [ ] 阻止的扩展名被过滤
  - [ ] 附件格式正确 (`content: list[bytes]`)

  **QA Scenarios**:
  ```
  Scenario: 证据扫描成功
    Tool: Bash
    Preconditions: 创建测试目录含 .txt, .png, .exe 文件
    Steps:
      1. uv run pytest tests/test_notify/test_evidence.py::test_scan_evidence_dir -v
      2. uv run pytest tests/test_notify/test_evidence.py::test_filter_blocked_extensions -v
    Expected Result: All tests pass, .exe filtered out
    Evidence: .sisyphus/evidence/task-04-evidence-scan.txt

  Scenario: 空目录处理
    Tool: Bash
    Preconditions: 空目录
    Steps:
      1. uv run pytest tests/test_notify/test_evidence.py::test_empty_evidence_dir -v
    Expected Result: Returns empty list, logs warning
    Evidence: .sisyphus/evidence/task-04-empty-dir.txt
  ```

  **Commit**: YES
  - Message: `feat(notify): implement evidence scanner with file filtering`
  - Files: template/{{project_name_snake}}/notify/evidence.py, template/tests/test_notify/test_evidence.py

- [x] 5. 实现 email_template.py (HTML 生成)

  **What to do**:
  - 实现 `generate_html_email(task_name, status, logs, duration, truncated: bool) -> str`
  - 实现 `generate_text_email(task_name, status, logs, duration) -> str` (纯文本回退)
  - 实现 `format_duration(seconds: float) -> str` - "2m 5s", "1h 1m 1s"
  - HTML 要求：内联 CSS，表格布局，响应式友好
  - 使用 `html.escape()` 转义所有用户内容
  - 状态颜色：success=绿色, failure=红色
  - 写测试：test_html_escape, test_format_duration, test_html_structure, test_text_fallback

  **Must NOT do**:
  - 不要使用外部 CSS 文件
  - 不要使用 Jinja2（f-string 足够）
  - 不要嵌入 JavaScript

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 模板生成逻辑简单
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 6, 7)
  - **Blocks**: Task 6
  - **Blocked By**: Task 2

  **References**:
  - HTML 邮件最佳实践: 内联 CSS，表格布局

  **Acceptance Criteria**:
  - [ ] `uv run pytest tests/test_notify/test_email_template.py -v` 全部通过
  - [ ] HTML 包含内联 CSS
  - [ ] `<script>` 被转义为 `&lt;script&gt;`

  **QA Scenarios**:
  ```
  Scenario: HTML 转义正确
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_email_template.py::test_html_escape_task_name -v
    Expected Result: <script> becomes &lt;script&gt;
    Evidence: .sisyphus/evidence/task-05-html-escape.txt

  Scenario: 耗时格式化正确
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_email_template.py::test_format_duration -v
    Expected Result: 125 → "2m 5s", 3661 → "1h 1m 1s"
    Evidence: .sisyphus/evidence/task-05-duration.txt
  ```

  **Commit**: YES
  - Message: `feat(notify): implement HTML email template generator`
  - Files: template/{{project_name_snake}}/notify/email_template.py, template/tests/test_notify/test_email_template.py

- [x] 6. 实现 core.py (主函数 + 重试)

  **What to do**:
  - 实现 `send_task_notification(task_name, status, logs, duration, attachment_paths=None, evidence_dir=None, max_log_lines=500) -> str`
  - 实现 3 次重试 + 指数退避（1s, 2s, 4s）
  - 集成 evidence.py 扫描附件
  - 集成 email_template.py 生成邮件
  - 集成 redact.py 过滤敏感数据
  - 日志截断：默认 500 行，超出时截断并标记
  - 环境变量验证：`RESEND_API_KEY`, `NOTIFICATION_EMAIL`
  - 异常处理：`MissingApiKeyError` 立即失败，`RateLimitError`/`ApplicationError` 重试，`ValidationError` 记录并失败
  - 写测试：test_send_success, test_retry_success, test_retry_exhausted, test_missing_api_key, test_log_truncation

  **Must NOT do**:
  - 不要使用 async/await
  - 不要超过 3 次重试

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 核心集成逻辑，需要协调多个模块
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5, 7)
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 2, 4, 5, 7 (需要测试 + evidence + template + redact)

  **References**:
  - Resend SDK: `https://github.com/resend/resend-python`
  - Resend 异常: `resend.exceptions.*`

  **Acceptance Criteria**:
  - [ ] `uv run pytest tests/test_notify/test_core.py -v` 全部通过
  - [ ] 重试逻辑正确（mock 验证调用次数）
  - [ ] 日志截断工作

  **QA Scenarios**:
  ```
  Scenario: 发送成功
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_core.py::test_send_notification_success -v
    Expected Result: Mock called once, returns email ID
    Evidence: .sisyphus/evidence/task-06-send-success.txt

  Scenario: 重试成功
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_core.py::test_retry_success_second_attempt -v
    Expected Result: First call fails, second succeeds, verify 2 calls
    Evidence: .sisyphus/evidence/task-06-retry-success.txt

  Scenario: 重试耗尽
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_core.py::test_retry_exhausts_three_attempts -v
    Expected Result: All 3 attempts fail, NotificationError raised
    Evidence: .sisyphus/evidence/task-06-retry-exhausted.txt
  ```

  **Commit**: YES
  - Message: `feat(notify): implement core notification with retry`
  - Files: template/{{project_name_snake}}/notify/core.py, template/tests/test_notify/test_core.py

- [x] 7. 实现敏感数据过滤

  **What to do**:
  - 实现 `redact_sensitive(text: str) -> str` - 过滤敏感数据
  - 过滤模式：
    - API keys: `sk-xxx`, `api_key=xxx`, `Bearer xxx`
    - 密码: `password=xxx`, `passwd xxx`
    - Tokens: `token=xxx`, `auth=xxx`
  - 替换为 `[REDACTED]`
  - 写测试：test_redact_api_key, test_redact_password, test_redact_token, test_no_match

  **Must NOT do**:
  - 不要修改原始字符串
  - 不要记录敏感数据到日志

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单正则替换
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5, 6)
  - **Blocks**: Task 6
  - **Blocked By**: Task 2

  **References**:
  - 常见敏感数据模式

  **Acceptance Criteria**:
  - [ ] `uv run pytest tests/test_notify/test_redact.py -v` 全部通过
  - [ ] API key 被替换为 `[REDACTED]`

  **QA Scenarios**:
  ```
  Scenario: API key 过滤
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_redact.py::test_redact_api_key -v
    Expected Result: sk-abc123 → [REDACTED]
    Evidence: .sisyphus/evidence/task-07-redact-apikey.txt

  Scenario: 密码过滤
    Tool: Bash
    Steps:
      1. uv run pytest tests/test_notify/test_redact.py::test_redact_password -v
    Expected Result: password=secret123 → password=[REDACTED]
    Evidence: .sisyphus/evidence/task-07-redact-password.txt
  ```

  **Commit**: YES
  - Message: `feat(notify): add sensitive data redaction`
  - Files: template/{{project_name_snake}}/notify/redact.py, template/tests/test_notify/test_redact.py

- [x] 8. 模块导出 + 类型完整

  **What to do**:
  - 更新 `template/{{project_name_snake}}/notify/__init__.py`
  - 导出: `send_task_notification`, `NotificationError`, `EvidenceDirNotFoundError`
  - 添加 `__all__` 列表
  - 确保所有公共函数有完整类型提示
  - 添加 Google-style docstrings
  - 运行 `uv run mypy --strict` 确保无错误

  **Must NOT do**:
  - 不要导出私有函数

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单的导出和类型完善
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (after Wave 2 complete)
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 3, 6 (需要 core 实现完成)

  **References**:
  - `template/{{project_name_snake}}/__init__.py.jinja` - 导出模式参考

  **Acceptance Criteria**:
  - [ ] `uv run mypy template/{{project_name_snake}}/notify --strict` 无错误
  - [ ] `from {{project_name_snake}}.notify import send_task_notification` 可用

  **QA Scenarios**:
  ```
  Scenario: 类型检查通过
    Tool: Bash
    Steps:
      1. cd template && uv run mypy {{project_name_snake}}/notify --strict
    Expected Result: Success: no issues found
    Evidence: .sisyphus/evidence/task-08-mypy.txt

  Scenario: 导入正确
    Tool: Bash
    Steps:
      1. cd template && uv run python -c "from {{project_name_snake}}.notify import send_task_notification, NotificationError; print('OK')"
    Expected Result: OK
    Evidence: .sisyphus/evidence/task-08-import.txt
  ```

  **Commit**: YES
  - Message: `feat(notify): complete module exports and type hints`
  - Files: template/{{project_name_snake}}/notify/__init__.py

- [x] 9. 集成测试 + 实际邮件发送

  **What to do**:
  - 创建 `template/tests/test_notify/test_integration.py`
  - 标记为 `@pytest.mark.integration`（默认跳过）
  - 测试实际发送邮件到 `NOTIFICATION_EMAIL`
  - 测试完整流程：创建证据目录 → 调用 `send_task_notification` → 验证邮件内容
  - 添加 README 或 docstring 说明如何运行集成测试
  - 运行全部单元测试确保无回归：`uv run pytest tests/test_notify/ -v --cov --cov-fail-under=80`

  **Must NOT do**:
  - 不要在 CI 中自动运行集成测试（需要真实 API key）
  - 不要发送垃圾邮件

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 集成测试需要谨慎处理真实 API
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (after Task 8)
  - **Blocks**: Final Verification
  - **Blocked By**: Task 8

  **References**:
  - Resend Dashboard: `https://resend.com/emails`

  **Acceptance Criteria**:
  - [ ] `uv run pytest tests/test_notify/ -v --cov --cov-fail-under=80` 通过
  - [ ] 集成测试文件存在（标记为 skip）
  - [ ] 文档说明如何运行集成测试

  **QA Scenarios**:
  ```
  Scenario: 全部单元测试通过
    Tool: Bash
    Steps:
      1. cd template && uv run pytest tests/test_notify/ -v --cov={{project_name_snake}}/notify --cov-fail-under=80
    Expected Result: All tests pass, coverage >= 80%
    Evidence: .sisyphus/evidence/task-09-all-tests.txt

  Scenario: 集成测试文件存在
    Tool: Bash
    Steps:
      1. ls template/tests/test_notify/test_integration.py
    Expected Result: File exists
    Evidence: .sisyphus/evidence/task-09-integration-file.txt

  Scenario: 实际邮件发送（手动，需要 API key）
    Tool: Bash
    Preconditions: RESEND_API_KEY 和 NOTIFICATION_EMAIL 已设置
    Steps:
      1. cd template && uv run pytest tests/test_notify/test_integration.py -m integration -v
    Expected Result: Email sent, check inbox for delivery
    Evidence: .sisyphus/evidence/task-09-real-email.txt
    Note: 此场景需要用户手动运行，CI 中跳过
  ```

  **Commit**: YES
  - Message: `test(notify): add integration test with real email`
  - Files: template/tests/test_notify/test_integration.py

---

## Final Verification Wave (MANDATORY)

- [x] F1. **Plan Compliance Audit** — `oracle`
  验证所有 "Must Have" 已实现，所有 "Must NOT Have" 未出现。检查证据文件存在。

- [x] F2. **Code Quality Review** — `unspecified-high`
  运行 `uv run mypy --strict` + `uv run pytest --cov --cov-fail-under=80`。检查 AI slop。

- [x] F3. **Real Manual QA** — `unspecified-high`
  从模板生成新项目，配置环境变量，实际发送测试邮件，验证收到。

- [x] F4. **Scope Fidelity Check** — `deep`
  验证每个任务实现与规格一致，无 scope creep。

---

## Commit Strategy

- **Task 1-3**: `feat(notify): add project skeleton with dependencies` — pyproject.toml.jinja, tests/__init__.py, notify/__init__.py
- **Task 4**: `feat(notify): implement evidence scanner with file filtering` — evidence.py, test_evidence.py
- **Task 5**: `feat(notify): implement HTML email template generator` — email_template.py, test_email_template.py
- **Task 6**: `feat(notify): implement core notification with retry` — core.py, test_core.py
- **Task 7**: `feat(notify): add sensitive data redaction` — redact.py, test_redact.py
- **Task 8**: `feat(notify): complete module exports` — __init__.py
- **Task 9**: `test(notify): add integration test with real email` — test_integration.py

---

## Success Criteria

### Verification Commands
```bash
# 类型检查
uv run mypy template/{{project_name_snake}}/notify --strict
# Expected: Success: no issues found

# 单元测试
uv run pytest template/tests/test_notify/ -v
# Expected: N passed, 0 failed

# 覆盖率
uv run pytest template/tests/test_notify/ --cov=template/{{project_name_snake}}/notify --cov-fail-under=80
# Expected: TOTAL coverage >= 80%

# 导入验证
cd template && uv run python -c "from {{project_name_snake}}.notify import send_task_notification; print('OK')"
# Expected: OK
```

### Final Checklist
- [ ] 所有 "Must Have" 功能实现
- [ ] 所有 "Must NOT Have" 未出现
- [ ] 所有测试通过
- [ ] 覆盖率 >= 80%
- [ ] 类型检查通过
- [ ] 实际邮件发送成功
