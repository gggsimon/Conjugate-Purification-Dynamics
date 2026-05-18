# 复现指南 | Reproduction Guide

本指南帮助研究者在自己的环境中复现共轭净化动力学（CPD）理论的实验。

---

## 环境依赖

### Python 依赖

```bash
pip install numpy matplotlib requests jieba
```

### Ollama（本地无对齐模型实验必需）

**安装 Ollama（macOS）**：

```bash
# 方法1：官网下载（推荐）
open https://ollama.com
# 下载 Ollama.app，拖入 Applications

# 方法2：命令行安装
curl -L https://github.com/ollama/ollama/releases/latest/download/ollama-darwin.zip -o ollama-darwin.zip
unzip ollama-darwin.zip
sudo mv ollama /usr/local/bin/

# 启动 Ollama 服务
ollama serve &
```

**拉取无对齐基础模型**：

```bash
# Qwen2.5-3B Base（无 RLHF，推荐）
ollama pull qwen2.5:3b-base

# 其他可选模型
ollama pull gemma2:2b
ollama pull qwen2.5:7b-base
```

---

## 实验一：商用大模型 API 扫描

### 适用场景
- 快速验证校准公式 `T_effective = 0.8 × T_apparent`
- 无需本地 GPU

### 步骤

1. 修改 `code/commercial_api_scan.py` 中的 `API_URL` 和 `MODEL_NAME`
2. 运行：

```bash
python code/commercial_api_scan.py
```

3. 查看结果：

```bash
cat experiment_data/commercial_api_real.json
python code/result_plot.py
```

### 预期结果

- 表观最优温度出现在 T ≈ 0.85
- 校准后有效温度 ≈ 0.68

---

## 实验二：本地无对齐模型完整扫描（推荐）

### 适用场景
- 验证完整的 A/B 倒 U 型曲线
- 观测 0.68 临界常数的直接证据

### 步骤

1. 确保 Ollama 服务已启动：

```bash
curl http://localhost:11434/api/tags
```

2. 逐温度运行（避免 macOS 超时）：

```bash
python code/ollama_local_test.py --scan
# 按输出的提示，逐条运行每个温度
```

3. 所有温度完成后，绘图：

```bash
python code/result_plot.py
```

### 预期结果

- **Diversity B**：低温低 → 中温抬升 → 高温崩塌（倒 U 型）
- **Specificity A**：低温高 → 中温平稳 → 高温下降
- **GDI**：单峰，峰值精确落在 T = 0.67~0.68

---

## 实验三：中文 Trigram 饱和问题验证

### 目的
验证中文文本的 trigram 多样性结构性饱和问题。

### 步骤

1. 使用中文 Prompt 运行 `ollama_local_test.py`（修改 PROMPT_EN 为中文）
2. 观察 Diversity B 是否长期饱和在 ~1.0
3. 对比英文 Prompt 的结果

### 预期
- 中文：B ≈ 1.0（饱和），无法观测倒 U 型
- 英文：B 随温度正常变化，倒 U 型清晰

---

## 常见问题

### Q1：macOS 上脚本被 SIGTERM 杀死？

**A**：macOS 对长时间运行的进程有限制。解决方案：
- 使用 `--scan` 模式逐温度运行
- 或改用 `nohup python script.py &` 后台运行

### Q2：Ollama 下载速度慢？

**A**：可使用国内镜像或代理：
```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama pull qwen2.5:3b-base
```

### Q3：GDI 曲线不是完美的倒 U 型？

**A**：可能原因：
1. 模型仍有对齐约束（确保使用 `-base` 或 `-instruct` 之前的原始预训练版本）
2. 采样数不够（增加 `N_SAMPLES` 到 15+）
3. 输出长度太短（增加 `MAX_GEN_TOKENS` 到 256+）

---

## 引用

如果您成功复现了实验，请引用：

```bibtex
@misc{daoxuan2026cpd,
  title={共轭净化动力学：大语言模型的普适生成能力守恒律与 0.68 临界常数（初步提案）},
  author={道玄},
  year={2026},
  howpublished={\url{https://github.com/daoxuan/Conjugate-Purification-Dynamics}}
}
```

---

**问题反馈**：请开 GitHub Issue 或在论文评论区留言。
