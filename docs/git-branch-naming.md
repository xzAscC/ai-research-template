# Git Branch 命名规范

本文档定义了项目中 Git 分支的命名约定。**除了 `main` 分支外，所有分支必须遵循此规范。**

## 允许的分支前缀

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能开发 | `feature/user-authentication` |
| `fix/` | Bug 修复 | `fix/login-timeout-error` |
| `hotfix/` | 紧急生产环境修复 | `hotfix/critical-security-patch` |
| `release/` | 发布准备 | `release/v1.2.0` |
| `docs/` | 文档更新 | `docs/api-reference-update` |
| `refactor/` | 代码重构 | `refactor/database-layer` |
| `test/` | 测试相关 | `test/integration-tests` |
| `chore/` | 杂项（依赖更新、配置等） | `chore/upgrade-dependencies` |
| `ci/` | CI/CD 配置变更 | `ci/add-github-actions` |
| `perf/` | 性能优化 | `perf/optimize-database-query` |

## 命名规则

### 格式

```
<前缀>/<简短描述>
```

### 要求

1. **前缀**：必须使用上表中列出的前缀之一
2. **分隔符**：前缀与描述之间使用单个 `/` 分隔
3. **描述**：
   - 使用小写字母
   - 使用 kebab-case（短横线连接单词）
   - 简洁明了，建议不超过 50 个字符
   - 允许字母、数字、短横线、点号（用于版本号如 `v1.2.0`）
   - 可选的 issue 编号前缀（如 `issue-123-`）

### 正则表达式

用于验证分支名称的正则表达式：

```regex
^(main|develop|(feature|fix|hotfix|release|docs|refactor|test|chore|ci|perf)/(issue-[0-9]+-)?[a-z0-9][a-z0-9.-]*)$
```

**说明**：
- `main` 和 `develop` 是例外分支，无需前缀
- 其他分支必须以允许的前缀开头，后跟 `/` 和描述
- 描述可包含可选的 issue 编号（如 `issue-123-`）
- 描述允许字母、数字、短横线、点号

## 示例

### ✅ 正确示例

```
feature/add-user-dashboard
feature/issue-42-add-oauth
fix/memory-leak-in-parser
hotfix/patch-sql-injection
release/v2.0.0
release/v2.1.0-beta
docs/update-installation-guide
refactor/simplify-auth-logic
test/add-unit-tests-for-utils
chore/update-eslint-config
ci/add-github-actions
perf/optimize-database-query
main
develop
```

### ❌ 错误示例

```
my-feature                    # 缺少前缀
Feature/user-auth             # 前缀应使用小写
feature/user_auth             # 应使用短横线而非下划线
fix/BugInLogin                # 描述应使用小写 kebab-case
feature/this-is-a-very-very-very-long-description-that-exceeds-reasonable-length  # 过长
wip/temp-stuff                # 未授权的前缀
main/some-feature             # main 不应作为前缀
```

## 例外

- `main` 分支：主分支，不需要前缀
- `develop` 分支：开发分支（如采用 Git Flow），不需要前缀
- 不允许其他无前缀的分支名称

## 强制执行

在创建 Pull Request 或合并到 `main` 时，CI 流程会自动检查分支名称是否符合此规范。不符合规范的分支将无法合并。

### GitHub Actions CI 检查

本项目已配置 GitHub Actions 工作流来自动验证分支名称：

- **工作流文件**：`.github/workflows/validate-branch-name.yml`
- **触发条件**：Pull Request 创建、编辑、同步、重新打开时
- **检查内容**：验证源分支名称是否符合命名规范

#### 设置为必需检查

要使 CI 检查成为合并的必要条件：

1. 进入仓库 **Settings** → **Branches**
2. 点击 `main` 分支保护规则的 **Edit** 按钮（或创建新规则）
3. 在 **Protect matching branches** 下勾选 **Require status checks to pass before merging**
4. 在搜索框中找到并勾选 `check-branch-name`
5. 点击 **Save changes**

设置完成后，分支名不符合规范的 PR 将无法合并。

### 本地检查

在创建分支前，可以使用以下命令验证：

```bash
# 验证分支名称
echo "feature/my-new-feature" | grep -E '^(main|develop|(feature|fix|hotfix|release|docs|refactor|test|chore|ci|perf)/(issue-[0-9]+-)?[a-z0-9][a-z0-9.-]*)$'

# 验证 release 分支（带版本号）
echo "release/v1.2.0" | grep -E '^(main|develop|(feature|fix|hotfix|release|docs|refactor|test|chore|ci|perf)/(issue-[0-9]+-)?[a-z0-9][a-z0-9.-]*)$'
```

## 工作流建议

1. **创建分支时**：从 `main` 分支检出新分支，使用规范的前缀和描述
2. **完成后**：创建 Pull Request，确保分支名称符合规范
3. **合并后**：删除已合并的功能分支，保持仓库整洁
