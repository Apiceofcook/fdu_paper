# 论文写作快速入门

## 🎯 开始写作

您的论文结构已经建立完成！现在可以开始撰写内容了。

---

## 📂 当前目录结构

```
mypaper/
│
├── 📄 mythesis.tex              ← 主文档（入口文件）
├── 📄 mythesis.bib              ← 参考文献库
├── 📄 mythesis.pdf              ← 编译生成的PDF
│
├── 📖 README.md                 ← 详细使用说明
├── 📖 STRUCTURE.md              ← 文档结构说明
├── 📖 QUICKSTART.md             ← 本文件：快速入门
│
├── 📁 chapters/                 ← 章节目录
│   ├── chapter1.tex            ← 第一章：绪论
│   ├── chapter2.tex            ← 第二章：相关工作
│   ├── chapter3.tex            ← 第三章：视觉数据构造框架
│   ├── chapter4.tex            ← 第四章：GUI
│   ├── chapter5.tex            ← 第五章：世界知识
│   └── chapter6.tex            ← 第六章：结论
│
├── 📁 figures/                  ← 图片目录
│   ├── chapter1/               ← 第一章的图片
│   ├── chapter2/               ← 第二章的图片
│   ├── chapter3/               ← 第三章的图片
│   ├── chapter4/               ← 第四章的图片
│   ├── chapter5/               ← 第五章的图片
│   └── chapter6/               ← 第六章的图片
│
└── 📁 test-*.tex                ← 模板示例文件（可删除）
```

---

## ✅ 三步开始写作

### 第一步：修改论文基本信息

编辑 `mythesis.tex`，找到 `\fdusetup` 部分，修改以下信息：

```latex
info = {
  title = {多模态视觉数据合成研究},              % ← 修改中文标题
  title* = {Multimodal Visual Data Synthesis},   % ← 修改英文标题
  author = {郑国栋},                             % ← 修改作者姓名
  author* = {Guodong Zheng},                     % ← 修改作者拼音
  supervisor = {黄萱菁\quad 教授},                % ← 修改导师
  major = {物理学},                              % ← 修改专业
  department = {凝聚态物理系},                    % ← 修改院系
  student-id = {14307110000},                    % ← 修改学号
  keywords = {关键词1, 关键词2, 关键词3},         % ← 修改关键词
  keywords* = {Keyword1, Keyword2, Keyword3},    % ← 修改英文关键词
  clc = {O414.1/65}                              % ← 修改中图分类号
}
```

### 第二步：撰写摘要

在 `mythesis.tex` 中找到摘要部分，填写内容：

```latex
% 中文摘要
\begin{abstract}
在此处撰写您的中文摘要（300-500字）
\end{abstract}

% 英文摘要
\begin{abstract*}
Write your English abstract here (200-400 words)
\end{abstract*}
```

### 第三步：开始写正文

打开 `chapters/chapter1.tex`，开始撰写第一章：

```latex
% 第一章：绪论
\chapter{绪论}

\section{研究背景}

在此撰写研究背景...

\section{研究动机}

在此撰写研究动机...
```

依次完成各章节的撰写。

---

## 🖊️ 常用 LaTeX 语法

### 1. 章节标题

```latex
\chapter{第一章标题}      % 章
\section{第一节标题}       % 节
\subsection{小节标题}      % 小节
\subsubsection{子小节}     % 子小节
```

### 2. 插入图片

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/chapter1/example.png}
  \caption{图片标题}
  \label{fig:example}
\end{figure}

% 在正文中引用
如图~\ref{fig:example} 所示...
```

### 3. 插入表格

```latex
\begin{table}[htbp]
  \centering
  \caption{表格标题}
  \label{tab:example}
  \begin{tabular}{ccc}
    \toprule
    列1 & 列2 & 列3 \\
    \midrule
    数据1 & 数据2 & 数据3 \\
    \bottomrule
  \end{tabular}
\end{table}

% 在正文中引用
如表~\ref{tab:example} 所示...
```

### 4. 数学公式

```latex
% 行内公式
这是一个行内公式 $E = mc^2$

% 行间公式（无编号）
\[
  f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx
\]

% 行间公式（有编号）
\begin{equation}
  \label{eq:example}
  y = ax + b
\end{equation}

% 在正文中引用
由式~\eqref{eq:example} 可知...
```

### 5. 列表

```latex
% 无序列表
\begin{itemize}
  \item 第一项
  \item 第二项
  \item 第三项
\end{itemize}

% 有序列表
\begin{enumerate}
  \item 第一项
  \item 第二项
  \item 第三项
\end{enumerate}
```

### 6. 引用参考文献

```latex
% 在 mythesis.bib 中添加文献条目，然后在正文中引用：
这是一个引用\cite{reference-key}。
```

---

## 🔨 编译论文

### 在终端中编译

```bash
# 进入论文目录
cd /Users/minimax/Documents/finalpaper/fdu_paper/mypaper

# 完整编译流程（推荐）
xelatex mythesis.tex
bibtex mythesis
xelatex mythesis.tex
xelatex mythesis.tex

# 或使用 latexmk 自动编译
latexmk -xelatex mythesis.tex
```

### 在 VSCode 中编译

如果使用 VSCode + LaTeX Workshop 插件：

1. 打开 `mythesis.tex`
2. 点击右上角的 ▶️ 按钮
3. 或使用快捷键：`Cmd + Option + B`（macOS）

---

## 📝 写作建议

### 1. 按章节顺序写作
建议按照 1→2→3→4→5→6 的顺序完成各章，保持逻辑连贯。

### 2. 频繁编译
每写完一小节就编译一次，及时发现问题。

### 3. 使用交叉引用
- 图：`\label{fig:xxx}` → `\ref{fig:xxx}`
- 表：`\label{tab:xxx}` → `\ref{tab:xxx}`
- 公式：`\label{eq:xxx}` → `\eqref{eq:xxx}`
- 章节：`\label{sec:xxx}` → `\ref{sec:xxx}`

### 4. 图片管理
将图片按章节放入对应的 `figures/chapterX/` 目录。

### 5. 版本控制
使用 Git 管理版本：

```bash
cd /Users/minimax/Documents/finalpaper/fdu_paper/mypaper
git init
git add mythesis.tex chapters/ mythesis.bib
git commit -m "初始化论文结构"

# 每次重要修改后提交
git add .
git commit -m "完成第一章"
```

### 6. 定期备份
每天将论文备份到云盘或 GitHub。

---

## 📚 参考资源

| 资源 | 链接/位置 |
|------|-----------|
| **详细使用说明** | `README.md` |
| **结构说明文档** | `STRUCTURE.md` |
| **模板文档（中文）** | [fduthesis.pdf](http://mirrors.ctan.org/macros/latex/contrib/fduthesis/fduthesis.pdf) |
| **LaTeX 入门教程** | [lshort-zh-cn](http://mirrors.ctan.org/info/lshort/chinese/lshort-zh-cn.pdf) |
| **GitHub 仓库** | [stone-zeng/fduthesis](https://github.com/stone-zeng/fduthesis) |

---

## 🐛 遇到问题？

### 常见问题速查

| 问题 | 解决方法 |
|------|---------|
| 编译出错 | 查看 `.log` 文件，搜索 `Error` |
| 找不到图片 | 检查图片路径是否正确 |
| 参考文献不显示 | 确保运行了 `bibtex mythesis` |
| 中文显示异常 | 检查文件是否为 UTF-8 编码 |
| 目录没更新 | 编译两次以上 |

### 获取帮助

1. 查看 `README.md` 详细说明
2. 查看 `STRUCTURE.md` 了解文档结构
3. 访问 [GitHub Issues](https://github.com/stone-zeng/fduthesis/issues)
4. 搜索 [TeX StackExchange](https://tex.stackexchange.com/)

---

## ✨ 下一步

现在您可以：

1. ✏️ 打开 `mythesis.tex`，修改论文基本信息
2. 📖 打开 `chapters/chapter1.tex`，开始写第一章
3. 🖼️ 准备图片，放入 `figures/` 目录
4. 📚 整理参考文献，添加到 `mythesis.bib`
5. 🔨 随时编译，查看效果

---

**祝您写作顺利！🎓**

如有问题，请查阅 `README.md` 或相关文档。

---

*创建时间：2026年1月*

