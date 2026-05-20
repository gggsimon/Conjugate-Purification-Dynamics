# Contributing to Conjugate Purification Dynamics

首先，感谢您考虑为 CPD 项目做出贡献！正是像您这样的贡献者让开源社区成为学习、启发和创造的绝佳场所。

## 📋 目录

- [Code of Conduct](#code-of-conduct)
- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [问题报告](#问题报告)

## Code of Conduct

本项目遵循 [Contributor Covenant](CODE_OF_CONDUCT.md) 行为准则。参与本项目即表示您同意遵守其条款。

## 如何贡献

### 报告 Bug

如果您发现了 bug，请先查看 [Issues](../../issues) 确认是否已有人报告。如果没有，请创建一个新的 issue，并包含以下信息：

- 问题的清晰描述
- 复现步骤
- 期望行为与实际行为
- 系统环境（Python 版本、操作系统等）
- 相关代码片段或错误日志

### 建议新功能

我们欢迎新功能建议！请创建一个 issue 并：

- 使用清晰的标题描述功能
- 详细说明该功能的用途和预期行为
- 如果可能，提供使用示例

### 提交代码

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 开发环境设置

### 前置要求

- Python 3.8+
- pip

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/gggsimon/Conjugate-Purification-Dynamics.git
cd Conjugate-Purification-Dynamics

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-cov

# 运行测试
python -m pytest tests/ -v
```

## 提交规范

### Commit Message 格式

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

- **feat**: 新功能
- **fix**: Bug 修复
- **docs**: 文档更新
- **style**: 代码格式调整（不影响功能）
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建过程或辅助工具的变动

#### 示例

```
feat(core): add batch processing support for GDI calculation

- Add batch_calc() function to process multiple texts
- Optimize performance with vectorized operations
- Update documentation with batch usage examples

Closes #123
```

### 代码风格

- 遵循 [PEP 8](https://pep8.org/) Python 代码风格指南
- 使用 4 空格缩进
- 最大行长度 100 字符
- 为所有公共函数添加 docstring

## Pull Request 流程

1. **更新文档**：如果您的更改影响 API 或使用方法，请更新相关文档
2. **添加测试**：为新功能添加测试，确保 bug 修复有对应的回归测试
3. **确保测试通过**：在提交 PR 前运行完整测试套件
4. **更新 CHANGELOG**：在 `CHANGELOG.md` 中记录您的更改
5. **关联 Issue**：如果 PR 解决了某个 issue，请在描述中使用 `Closes #issue_number`

### PR 审查清单

- [ ] 代码符合项目风格规范
- [ ] 所有测试通过
- [ ] 新功能有对应的测试覆盖
- [ ] 文档已更新
- [ ] CHANGELOG 已更新
- [ ] Commit message 符合规范

## 问题报告

### 报告 Bug 的模板

```markdown
**描述 Bug**
清晰简洁地描述 bug 是什么。

**复现步骤**
1. 执行 '...'
2. 输入 '....'
3. 看到错误

**期望行为**
清晰描述您期望发生什么。

**截图**
如果适用，添加截图帮助解释问题。

**环境信息:**
 - OS: [e.g. Windows 10]
 - Python 版本: [e.g. 3.11]
 - 项目版本: [e.g. 0.1.0]

**附加信息**
添加关于问题的任何其他上下文。
```

## 🙏 感谢

再次感谢您的贡献！每一个 PR、issue 和想法都让 CPD 变得更好。

如果您有任何问题，欢迎通过 [Issues](../../issues) 或邮件联系我们。
