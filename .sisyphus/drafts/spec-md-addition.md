# Draft: Add SPEC.md to Project

## Request Summary
User wants to add a SPEC.md file to the project, inspired by the augmentcode tweet about spec-driven development for AI coding agents.

## Research Findings

### What is SPEC.md?
Based on Addy Osmani's blog post and GitHub's analysis of 2,500+ agent configs:

**SPEC.md vs AGENTS.md:**
- **AGENTS.md**: Tells AI agent "how to work" (commands, workflow, code style)
- **SPEC.md**: Tells AI agent "what to build" (vision, features, requirements, success criteria)

### Six Core Areas (from GitHub study):
1. **Commands** - Executable commands with full flags
2. **Testing** - Test framework, coverage expectations, test locations
3. **Project Structure** - Where source, tests, docs live
4. **Code Style** - Naming, formatting, examples
5. **Git Workflow** - Branch naming, commit format, PR requirements
6. **Boundaries** - Three-tier system: Always/Ask First/Never

### Three-Tier Boundary System:
- ✅ **Always do**: Actions agent takes without asking
- ⚠️ **Ask first**: Actions requiring human approval
- 🚫 **Never do**: Hard stops

## Current Project Context

**Project Type**: AI Research Template (Python)
**Existing Files**: AGENTS.md (comprehensive), ARCHITECTURE.md, PLAN.md, README.md

**Tech Stack**:
- Package manager: uv
- Python: 3.12+
- Lint/Format: ruff
- Type check: mypy
- Test: pytest

## Open Questions
- Should SPEC.md focus on the template itself or how to use the template for research?
- What is the primary "product vision" for this template?
- Any specific constraints or boundaries not covered in AGENTS.md?
- Should SPEC.md be machine-readable (YAML/JSON sections) or human-readable (pure Markdown)?

## Decisions Made

1. **Focus**: 模板自身规范
   - 描述这个模板项目本身的开发规范
   - 包含维护标准、贡献指南
   - 而非描述如何使用模板进行研究

2. **Format**: 与 AGENTS.md 风格一致
   - 保持相似的结构和风格
   - 纯 Markdown，编号章节
   - 清晰的标题层次

3. **Vision Section**: 简短版本
   - 一段话描述核心目的
   - 不需要详细的背景、目标用户等

4. **Code Examples**: 不包含
   - 只用文字描述风格
   - 不包含实际代码片段

5. **Boundary System**: 包含三层边界
   - ✅ Always do
   - ⚠️ Ask first
   - 🚫 Never do

## Scope Boundaries

### INCLUDE:
- 新建 SPEC.md 文件
- 项目愿景（简短）
- 与 AGENTS.md 风格一致的结构
- 三层边界系统
- 创建新 branch 进行开发

### EXCLUDE:
- 代码示例
- 详细的项目背景描述
- 修改现有文件（除非必要）
