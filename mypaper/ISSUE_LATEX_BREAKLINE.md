# LaTeX 英文长串溢出问题记录

> 日期：2026-05-26
> 状态：待修复

## 问题描述

PDF 渲染后某些段落（尤其是中文摘要、第 5 章正文）出现明显的右边距溢出（Overfull \hbox），原因是连续的英文术语使用 `/` 连接，但 LaTeX 默认不在 `/` 处断行，导致整个长串作为一个不可断的单元被压在行尾，超出文本框宽度。

典型例子：

- `RecQA/KnowQA/FinalQA`
- `Calc/Impress/Writer`
- `Activated/Interactable/Filled`
- `LibreOffice/Calc/Impress/Writer`
- `perception/understanding/reasoning`

## 问题影响位置统计

通过全文扫描发现，以下 5 类长串共出现 15 次，全部需要处理：

| 长串 | 出现次数 | 主要位置 |
|---|---|---|
| `Calc/Impress/Writer` | 6 | chapter1.tex, chapter3.tex, chapter6.tex, mythesis.tex 中英文摘要 |
| `RecQA/KnowQA/FinalQA` | 5 | chapter1.tex, chapter5.tex, chapter3.tex, mythesis.tex |
| `Activated/Interactable/Filled` | 2 | chapter4.tex（§3.2 核心方法概览 + §标注规范） |
| `LibreOffice/Calc/Impress/Writer` | 1 | chapter6.tex 主要成果与创新点 |
| `perception/understanding/reasoning` | 1 | mythesis.tex 英文摘要 |

文件路径相关的 `figures/chapterX/xxx` 不计入（出现在 `\includegraphics` 命令内，不参与正文排版断行）。

## 根本原因

LaTeX 的断行算法在以下字符处允许自动断行：

- 空格（普通断行点）
- 连字符 `-`（特别是英文单词内的）
- `\allowbreak` / `\linebreak` 显式标记
- `\slash` 命令（区别于普通 `/`）

但**普通 `/` 字符不允许断行**，整段 `RecQA/KnowQA/FinalQA` 被当作 20 字符的不可分单元，常常被推到下一行导致前一行右边距大量空白，或被强行压缩导致溢出。

## 修复方案

### 方案 A：在每个 `/` 后插入 `\allowbreak`（推荐）

不改变视觉效果，仅告诉 LaTeX 在该处允许折行：

```latex
RecQA/\allowbreak KnowQA/\allowbreak FinalQA
Calc/\allowbreak Impress/\allowbreak Writer
Activated/\allowbreak Interactable/\allowbreak Filled
LibreOffice/\allowbreak Calc/\allowbreak Impress/\allowbreak Writer
perception/\allowbreak understanding/\allowbreak reasoning
```

优点：

- 视觉效果完全不变
- 仅在确实需要时才断行
- LaTeX 标准命令，兼容性好

缺点：

- 源码稍微长一些

### 方案 B：使用 `\slash` 替代 `/`

`\slash` 是 LaTeX 命令，效果等同 `/` 但允许在其后断行。

```latex
RecQA\slash KnowQA\slash FinalQA
```

优点：

- 源码相对干净

缺点：

- `\slash` 后面紧跟字母会被 LaTeX 误判为命令名，需要 `\slash{}KnowQA` 或 `\slash KnowQA`（带空格）
- 在中文环境下与 `/` 的视觉效果可能有细微差异

### 方案 C：自定义宏一次性处理

```latex
\newcommand{\sla}{/\allowbreak}
```

然后用 `RecQA\sla KnowQA\sla FinalQA` 替代。

优点：

- 源码最短

缺点：

- 引入额外宏，后人接手时需要看 preamble 才能理解

## 建议执行方案

**推荐方案 A（`\allowbreak`）**，理由：

1. 视觉效果零变化，PDF 中 `/` 显示完全一致
2. LaTeX 标准命令，无需 preamble 改动
3. 仅在行宽紧张时触发断行，行宽充裕时与原来表现一致

## 待修改文件清单

- [ ] `mythesis.tex`（中英文摘要：约 5 处）
- [ ] `chapters/chapter1.tex`（绪论：约 3 处）
- [ ] `chapters/chapter3.tex`（第 5 章 Auto-Evol：约 3 处）
- [ ] `chapters/chapter4.tex`（第 3 章 GUI：2 处 `Activated/Interactable/Filled`）
- [ ] `chapters/chapter5.tex`（第 4 章世界知识：1 处 `RecQA/KnowQA/FinalQA`）
- [ ] `chapters/chapter6.tex`（结论：约 2 处）

## 验收标准

修复后重新编译，检查：

1. 编译日志 `mythesis.log` 中 `Overfull \hbox` 警告数量明显下降
2. PDF 中所有出现这 5 类长串的段落右边距整齐
3. 视觉上 `/` 显示与原版完全一致

## 修复脚本草案

可用 Python 脚本批量替换：

```python
substitutions = [
    ('RecQA/KnowQA/FinalQA', 'RecQA/\\allowbreak KnowQA/\\allowbreak FinalQA'),
    ('Calc/Impress/Writer', 'Calc/\\allowbreak Impress/\\allowbreak Writer'),
    ('Activated/Interactable/Filled', 'Activated/\\allowbreak Interactable/\\allowbreak Filled'),
    ('LibreOffice/Calc/Impress/Writer', 'LibreOffice/\\allowbreak Calc/\\allowbreak Impress/\\allowbreak Writer'),
    ('perception/understanding/reasoning', 'perception/\\allowbreak understanding/\\allowbreak reasoning'),
]
```

注意替换顺序：先长后短（避免 `LibreOffice/Calc/Impress/Writer` 被先短串吃掉）。

## 备注

如果未来还出现新的长串（如 `Calc/Impress/Writer/VSCode/Chrome`），也应同步加入处理列表。
