# 摘要修改方案

> 参考 ShareGPT4V / MMEvol / SynthVLM / AgentInstruct / OSWorld / EvoCUA 等论文摘要风格

## 一、当前问题诊断

| 项 | 当前状态 | 问题 |
|---|---|---|
| 中文摘要 | 6 段 + 4 个 `(1)(2)(3)(4)` 段落小标题（已去粗）| 不像学术摘要，像 PPT 大纲 |
| 英文摘要 | 同上 6 段结构 | 同上 |
| 中文字数 | 639 字 | 偏长（建议 ≤ 500）|
| 英文词数 | 366 词 | 偏长（建议 ≤ 280）|
| 关键词 | 7 个（多模态数据合成、Auto-Evol、数据合成框架、GUI 理解、世界知识推理、GUI CUA、可验证任务合成）| 太多（学位论文一般 3-5 个）|
| CLC 中图分类号 | `O414.1/65`（**O414.1 是物理学非线性物理！与本论文完全无关**）| 必须改对 |

## 二、参考论文风格观察

英文顶会论文摘要普遍特点：
1. **连贯成段**，不用 `(1)(2)(3)` 分点
2. **3 段结构**：背景 1 段 + 方法 1-2 段 + 实验/贡献 1 段
3. **零加粗**（已完成）
4. **数字核心结论紧凑表述**

学位论文中文摘要规范：
- 长度 300-500 字（学位条例规定）
- 结构化但仍保持段落连贯

## 三、推荐修改方案

### A. 中文摘要（约 530 字，3 段连贯叙述）

```
多模态大语言模型近年来快速发展，但其能力提升正越来越受限于训练数据
的质量、对齐度与推理密度。互联网抓取的图文对噪声较大、对齐较弱；人
工标注成本高、长尾覆盖有限；模型在真实任务中暴露出小目标定位不稳、
视觉证据与语言描述绑定松散、推理任务易出现短路映射等结构性误差。
"数据规模优先"的合成范式已遇瓶颈，亟需面向质量与能力维度的系统化
数据生产方法。

本文研究如何以可控、可迭代、可验证的方式生产高质量多模态训练数据，
并沿数据能力光谱的感知端、推理端与综合中段三个代表性位置展开实证。
在感知端面向 GUI 任务，构建以多源融合为核心的数据合成 Pipeline，
结合紧致 bbox、OCR 对齐、控件关系图谱与状态向量等结构化监督，并
配合 AnyRes 高分辨率感知与双阶段混合微调策略，在 Top 200 主流应用
真实分布评测中将 Grounding F1 由 0.324 提升至 0.846、Referring F1
由 0.523 提升至 0.905。在推理端面向世界知识任务，建立 7 大类 40
子类知识类别框架与端到端数据 Pipeline，通过"词条→图片→caption
→相关性过滤→RecQA/KnowQA/FinalQA"链路将分散知识转化为可学习、
可校验的多模态监督，并在 FinalQA 中引入 Think/CoT 过程监督，在
Chinese SimpleVQA 与 SimpleVQA 上取得有竞争力的结果。

在两端工程实践基础上，本文进一步抽象提出 Auto-Evol 多模态数据合成
框架，将以往单步生成升级为包含数据源组织、结构化初始化、原子问题
生成、代理式增强、多维校验与失败回流的闭环系统。为验证框架的可
迁移性，本文将其实例化到光谱综合中段的 GUI 计算机使用智能体（CUA）
场景，依托 OSWorld 评测体系在 LibreOffice 三个 domain 上构建可
验证任务合成系统；通过 900 合成任务、723 成功轨迹与 3 万条单步训练
数据，将 Qwen3-VL-Think 在 OSWorld LibreOffice 三个 domain 上的
overall accuracy 由 40.8% 提升至 61.4%，绝对增益 20.6 个百分点。
所提方法与框架为多模态数据合成在更多任务域的复用与扩展提供了可
参考的工程范式。
```

**优点**：

- 3 段连贯叙述，符合学位论文规范
- 删除 `(1)(2)(3)(4)` 段落小标题
- 仍包含核心叙事（数据能力光谱 + 三位置实证）
- 关键数字一目了然

### B. 英文摘要（约 280 词，3 段连贯）

```
Multimodal large language models (MLLMs) have advanced rapidly in
vision-language understanding, but their capability ceiling is
increasingly constrained by the quality, alignment, and reasoning
density of training data rather than data scale. Web-crawled image-text
pairs are noisy and weakly aligned, manual annotation is expensive and
narrow in long-tail coverage, and models exhibit structural errors
such as unstable small-object localization, loose vision-language
grounding, and shortcut learning. Under this bottleneck, traditional
"scale-first" synthesis paradigms are no longer sufficient.

This thesis investigates how to produce high-quality multimodal training
data in a controllable, iterative, and verifiable manner, organized
along three representative positions on the data capability spectrum:
the perception end, the reasoning end, and the synthetic mid-band.
At the perception end, targeting mobile GUI tasks, we build a
multi-source data synthesis pipeline with structured supervision
(tight bounding boxes, OCR alignment, element relation graphs,
interaction states), combined with AnyRes high-resolution perception
and dual-stage mixed tuning. On a top-200 popular-application
benchmark, this raises Grounding F1 from 0.324 to 0.846 and Referring
F1 from 0.523 to 0.905. At the reasoning end, targeting world-knowledge
tasks, we construct a taxonomy of 7 super-categories and 40
sub-categories with an end-to-end pipeline (entry -> images ->
captions -> relevance filtering -> RecQA/KnowQA/FinalQA), and
introduce Think/CoT process supervision in FinalQA to mitigate
shortcut learning, achieving competitive results on Chinese SimpleVQA
and SimpleVQA.

Generalizing recurring patterns from both ends, we propose Auto-Evol,
a closed-loop multimodal data synthesis framework integrating
structured initialization, atomic-question generation, agent-based
augmentation, multi-dimensional filtering, and feedback rewriting,
organized around the perception/understanding/reasoning capability
axes. To validate transferability, we instantiate Auto-Evol on the
synthetic mid-band -- GUI Computer Use Agent (CUA) tasks -- and build
a verifiable-task synthesis pipeline on three OSWorld LibreOffice
domains. With 900 synthetic tasks, 723 successful trajectories, and
30k single-step training samples, Qwen3-VL-Think achieves an overall
accuracy improvement from 40.8% to 61.4% (+20.6 points). The proposed
methodology and framework provide a reusable engineering paradigm
for multimodal data synthesis across broader task domains.
```

### C. 关键词精简到 5 个

**中文关键词（5 个）**：

```
多模态大模型，数据合成，GUI 智能体，世界知识，闭环框架
```

**英文关键词（5 个）**：

```
Multimodal Large Language Models, Data Synthesis,
GUI Agent, World Knowledge, Closed-Loop Framework
```

> 删除：`Auto-Evol`（自创术语不适合做关键词）、`数据合成框架`（与"数据合成"重复）、`可验证任务合成`（过窄）、`GUI 理解`（合并到 GUI 智能体）、`世界知识推理`（合并到世界知识）。

### D. CLC 中图分类号修正

**当前**：`O414.1/65`（**错误**：O414.1 是物理学/非线性物理）

**推荐改为**：`TP391`（计算机应用：信息处理）

**备选**：

| CLC 分类号 | 含义 | 评估 |
|---|---|---|
| **TP391** | 计算机应用：信息处理 | ⭐ 推荐（最广泛）|
| TP18 | 人工智能理论 | ✓ 也合适 |
| TP391.41 | 计算机图像识别 | ✓ 偏 GUI 视觉 |
| TP391.1 | 计算机自然语言处理 | 偏 NLP |

CLC 是学位论文必填字段，**不能去掉**（fduthesis 模板默认要求）。但可以填得正确。

## 四、待您确认

1. 中文摘要：采用上述 3 段连贯叙述版？
2. 英文摘要：采用上述 3 段连贯叙述版？
3. 关键词：精简到 5 个（多模态大模型 / 数据合成 / GUI 智能体 / 世界知识 / 闭环框架）？
4. CLC：改为 **TP391** 还是 TP18？

确认后我立即修改 mythesis.tex。
