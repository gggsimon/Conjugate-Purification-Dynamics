# CPD项目文档索引

## 📚 快速导航

### 核心理论
- [README.md](../README.md) - 项目主页，理论概述与快速开始
- [CPD理论草案](../paper/CPD_Theory_Draft.md) - 完整学术论文（Markdown版）
- [CPD理论草案PDF](../paper/CPD_Theory_Draft.pdf) - 完整学术论文（PDF版）

### 实验与数据
- [实验复现指南](reproduce_guide.md) - 详细复现步骤
- [Qwen3B实验结果](../experiment_data/qwen3b_results.md) - 3B模型完整实验报告
- [实验数据目录](../experiment_data/) - 原始JSON数据文件

### 应用拓展
- [华为揭榜方案](../proposals/huawei_chaspark_pathfinding_20260520.md) - 多目标寻径算法方案

### 代码文档
- [core_gdi_calc.py](../code/core_gdi_calc.py) - GDI核心计算模块
- [ollama_local_test.py](../code/ollama_local_test.py) - 本地Ollama实验脚本
- [commercial_api_scan.py](../code/commercial_api_scan.py) - 商用API扫描脚本
- [result_plot.py](../code/result_plot.py) - 结果可视化脚本

---

## 🎯 不同读者的阅读路径

### 初次接触CPD
1. 阅读 [README.md](../README.md) 的"理论一句话"和"摘要"
2. 查看 [核心理论](#核心理论) 部分的公式
3. 浏览 [实验进展](#实验进展) 的图表
4. 深入阅读 [CPD理论草案](../paper/CPD_Theory_Draft.md)

### 想要复现实验
1. 阅读 [实验复现指南](reproduce_guide.md)
2. 准备环境（Ollama + Python依赖）
3. 运行 [ollama_local_test.py](../code/ollama_local_test.py)
4. 使用 [result_plot.py](../code/result_plot.py) 可视化结果

### 学术研究者
1. 精读 [CPD理论草案](../paper/CPD_Theory_Draft.md)
2. 查看 [实验数据](../experiment_data/) 的原始JSON
3. 阅读 [Qwen3B实验结果](../experiment_data/qwen3b_results.md)
4. 检查 [当前实验局限性](../README.md#当前实验局限性)

### 工程师/应用开发者
1. 阅读 [README.md](../README.md) 的核心理论部分
2. 查看 [华为揭榜方案](../proposals/huawei_chaspark_pathfinding_20260520.md)
3. 研究 [core_gdi_calc.py](../code/core_gdi_calc.py) 的实现
4. 参考代码进行适配开发

---

## 📊 文档状态

| 文档 | 状态 | 最后更新 |
|------|------|----------|
| README.md | ✅ 完整 | 2026-05-20 |
| CPD理论草案 | ✅ 完整 | 2026-05-19 |
| 实验复现指南 | ✅ 完整 | 2026-05-19 |
| 华为揭榜方案 | ✅ 完整 | 2026-05-20 |
| Qwen3B实验报告 | ✅ 完整 | 2026-05-19 |

---

## 🔗 外部链接

- **GitHub仓库**: https://github.com/gggsimon/Conjugate-Purification-Dynamics
- **华为黄大年茶思屋**: https://www.huawei.com/cn/...

---

*最后更新：2026年5月20日*
