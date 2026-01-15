# 复旦大学论文模板使用指南

## 📖 简介

本目录（`mypaper`）是您撰写论文的工作目录，基于 **fduthesis** 模板（复旦大学学位论文 LaTeX 模板）。

- **模板引擎**：支持 XeLaTeX 和 LuaTeX
- **编码**：UTF-8
- **适用范围**：博士/硕士学位论文、本科毕业论文（中英文均可）

⚠️ **重要提示**：本模板未经学校相关部门审核及授权，使用前请务必斟酌。

---

## 📁 目录结构说明

```
mypaper/
├── README.md                      # 本使用说明文档
├── test.tex                       # 主文档（示例文件）
├── test.bib                       # 参考文献数据库
├── test-figure-table.tex         # 图表示例
├── test-footnote.tex             # 脚注示例
├── test-theorem.tex              # 定理环境示例
├── test-en.tex                   # 英文版示例
├── test-biblatex.tex             # BibLaTeX 示例
├── fduthesis-test-toolkit.tex    # 测试工具
└── dtxtest.dtx                   # 文档源文件
```

---

## 🚀 快速开始

### 步骤 1：复制模板文件

建议基于 `test.tex` 创建您自己的论文文件：

```bash
cd /Users/minimax/Documents/finalpaper/fdu_paper/mypaper
cp test.tex mythesis.tex
cp test.bib mythesis.bib
```

### 步骤 2：修改论文信息

编辑 `mythesis.tex`，找到 `\fdusetup` 部分，修改为您的论文信息：

```latex
\fdusetup{
  style = {
    font = times,                  % 英文字体
    cjk-font = fandol,            % 中文字体（可选：fandol, windows, mac等）
    font-size = 5,                % 五号字
    bib-backend = bibtex,         % 文献后端（bibtex 或 biblatex）
    bib-style = numerical,        % 文献样式（numerical 或 author-year）
    bib-resource = {mythesis.bib} % 您的文献库文件
  },
  info = {
    title = {您的论文标题},
    title* = {Your Thesis Title in English},
    author = {您的姓名},
    author* = {Your Name in Pinyin},
    supervisor = {导师姓名\quad 教授},
    major = {您的专业},
    department = {您的院系},
    degree = academic,            % academic(学术学位) 或 professional(专业学位)
    student-id = {您的学号},
    keywords = {关键词1, 关键词2, 关键词3},
    keywords* = {Keyword1, Keyword2, Keyword3},
    clc = {分类号},               % 中图分类号
    secret-level = none,          % 密级（none, i, ii, iii）
  }
}
```

### 步骤 3：编写论文内容

在 `\begin{document}` 和 `\end{document}` 之间编写论文：

```latex
\begin{document}

% 前置部分
\frontmatter
\tableofcontents        % 目录
\listoffigures          % 图目录（可选）
\listoftables           % 表目录（可选）

% 中文摘要
\begin{abstract}
这里写中文摘要内容...
\end{abstract}

% 英文摘要
\begin{abstract*}
Write your English abstract here...
\end{abstract*}

% 符号说明（可选）
\begin{notation}[lp{20em}]
$\alpha$    &  符号说明 \\
$\beta$     &  另一个符号 \\
\end{notation}

% 正文部分
\mainmatter

\chapter{第一章标题}
\section{第一节}
这里是正文内容...

\chapter{第二章标题}
\section{另一节}
更多内容...

% 后置部分（参考文献等）
\backmatter
\printbibliography  % 如果使用 biblatex
% 或
% \bibliography{mythesis}  % 如果使用 bibtex

\end{document}
```

### 步骤 4：编译论文

使用 **XeLaTeX** 编译（推荐）：

```bash
# 完整编译流程（包含参考文献）
xelatex mythesis.tex
bibtex mythesis      # 如果使用 bibtex
# 或
# biber mythesis     # 如果使用 biblatex
xelatex mythesis.tex
xelatex mythesis.tex
```

或使用 **latexmk** 自动编译：

```bash
latexmk -xelatex mythesis.tex
```

---

## 📝 详细配置说明

### 1. 字体设置

```latex
style = {
  font = times,           % 英文字体：times, termes, stix, xits, libertinus 等
  cjk-font = fandol,      % 中文字体：
                          %   - fandol    (开源字体，跨平台)
                          %   - windows   (Windows 系统字体)
                          %   - mac       (macOS 系统字体)
                          %   - noto      (Google Noto 字体)
  font-size = 5,          % 字号：-4(小四) 5(五号)
}
```

### 2. 超链接设置

```latex
style = {
  hyperlink = color,      % 超链接样式：none, color, border
  hyperlink-color = default,  % 颜色方案：default, classic, elegant, material
}
```

### 3. 文献管理

#### 使用 BibTeX（推荐新手）

```latex
style = {
  bib-backend = bibtex,
  bib-style = numerical,     % numerical(数字) 或 author-year(作者-年份)
  bib-resource = {mythesis.bib}
}
```

编译命令：
```bash
xelatex mythesis
bibtex mythesis
xelatex mythesis
xelatex mythesis
```

#### 使用 BibLaTeX（功能更强）

```latex
style = {
  bib-backend = biblatex,
  bib-style = gb7714-2015,  % 符合国标的参考文献样式
  bib-resource = {mythesis.bib}
}
```

编译命令：
```bash
xelatex mythesis
biber mythesis
xelatex mythesis
xelatex mythesis
```

### 4. 参考文献引用

在正文中引用文献：

```latex
\cite{reference-key}        % 基本引用
\citep{reference-key}       % 括号引用（适合数字式）
\citet{reference-key}       % 文本引用（适合作者-年份式）
```

---

## 🖼️ 插入图表

### 插入图片

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/example.png}
  \caption{图片标题}
  \label{fig:example}
\end{figure}

% 在正文中引用
如图~\ref{fig:example} 所示...
```

### 插入表格

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
    数据4 & 数据5 & 数据6 \\
    \bottomrule
  \end{tabular}
\end{table}

% 在正文中引用
如表~\ref{tab:example} 所示...
```

---

## 📚 定理环境

模板内置了多种定理环境：

```latex
\begin{theorem}
  这是一个定理。
\end{theorem}

\begin{lemma}
  这是一个引理。
\end{lemma}

\begin{proof}
  这是证明过程。
\end{proof}

% 其他环境：definition, corollary, proposition, example, remark 等
```

---

## 🔧 常见问题

### Q1: 编译出错，提示找不到字体？

**解决方法**：修改 `cjk-font` 选项
- Windows 系统：`cjk-font = windows`
- macOS 系统：`cjk-font = mac`
- Linux 或跨平台：`cjk-font = fandol`（需安装 fandol 字体）

### Q2: 参考文献不显示或格式不对？

**解决方法**：
1. 确认 `.bib` 文件路径正确
2. 确保执行了完整的编译流程（xelatex → bibtex/biber → xelatex × 2）
3. 检查 `bib-backend` 和 `bib-style` 设置是否匹配

### Q3: 如何修改页边距、行距等格式？

**解决方法**：查阅完整文档
```bash
# 查看详细文档（在父目录或在线查看）
open http://mirrors.ctan.org/macros/latex/contrib/fduthesis/fduthesis.pdf
```

### Q4: 如何生成英文论文？

**解决方法**：使用 `fduthesis-en` 文档类
```latex
\documentclass{fduthesis-en}
```
或参考 `test-en.tex` 示例文件。

### Q5: 编译速度太慢怎么办？

**解决方法**：
- 草稿模式：`\documentclass[draft]{fduthesis}`
- 使用 latexmk 增量编译
- 图片使用较低分辨率的草稿版本

---

## 📖 参考资源

### 官方资源
- **模板文档**（中文）：[fduthesis.pdf](http://mirrors.ctan.org/macros/latex/contrib/fduthesis/fduthesis.pdf)
- **模板文档**（英文）：[fduthesis-en.pdf](http://mirrors.ctan.org/macros/latex/contrib/fduthesis/fduthesis-en.pdf)
- **GitHub 仓库**：[https://github.com/stone-zeng/fduthesis](https://github.com/stone-zeng/fduthesis)
- **Overleaf 模板**：[https://www.overleaf.com/latex/templates/fduthesis](https://www.overleaf.com/latex/templates/fduthesis)

### LaTeX 学习资源
- **一份不太简短的 LaTeX 介绍**：[lshort-zh-cn](http://mirrors.ctan.org/info/lshort/chinese/lshort-zh-cn.pdf)
- **LaTeX Wikibook**：[https://en.wikibooks.org/wiki/LaTeX](https://en.wikibooks.org/wiki/LaTeX)

### 推荐的 LaTeX 编辑器
- **VSCode** + LaTeX Workshop 插件（推荐）
- **TeXstudio**（跨平台）
- **Overleaf**（在线，无需安装）
- **TeXShop**（macOS）

---

## 📋 编写建议

### 1. 文件组织
建议将论文拆分成多个文件：

```
mypaper/
├── mythesis.tex           # 主文档
├── mythesis.bib           # 参考文献
├── chapters/              # 各章节
│   ├── chapter1.tex
│   ├── chapter2.tex
│   └── chapter3.tex
├── figures/               # 图片文件
│   ├── fig1.pdf
│   └── fig2.png
└── tables/                # 表格（可选）
    └── table1.tex
```

在主文档中使用 `\input` 或 `\include` 引入：

```latex
\mainmatter
\include{chapters/chapter1}
\include{chapters/chapter2}
\include{chapters/chapter3}
```

### 2. 版本控制
强烈建议使用 Git 进行版本控制：

```bash
cd /Users/minimax/Documents/finalpaper/fdu_paper/mypaper
git init
git add mythesis.tex mythesis.bib chapters/
git commit -m "Initial commit"
```

### 3. 备份策略
- 定期备份到云盘（iCloud、Google Drive、Dropbox 等）
- 使用 Git + GitHub/GitLab 远程仓库
- 重要节点保存多个版本

### 4. 写作技巧
- 先搭框架，后填内容
- 使用 `\chapter`、`\section`、`\subsection` 建立清晰结构
- 及时添加 `\label` 和使用 `\ref` 交叉引用
- 养成随时编译的习惯，及早发现错误
- 使用注释 `%` 标记待完成部分

---

## ⚠️ 注意事项

1. **格式规范**：使用模板前请务必查阅学校最新的论文格式要求，模板可能需要微调
2. **字体版权**：商业字体（如方正、Adobe 字体）需要购买授权
3. **图片格式**：推荐使用矢量图（PDF、EPS）以获得最佳打印质量
4. **文件命名**：避免使用中文和特殊字符命名文件
5. **编码统一**：所有 `.tex` 和 `.bib` 文件必须使用 UTF-8 编码
6. **定期编译**：不要积累太多内容后才编译，容易出现难以定位的错误

---

## 🆘 获取帮助

- **模板问题**：查看 [GitHub Issues](https://github.com/stone-zeng/fduthesis/issues)
- **LaTeX 语法**：搜索 [TeX StackExchange](https://tex.stackexchange.com/)
- **通用问题**：查阅模板文档 `fduthesis.pdf`

---

## 📄 许可证

本模板遵循 [LaTeX Project Public License](http://www.latex-project.org/lppl.txt) v1.3c 或更高版本。

---

## ✅ 检查清单（提交前）

提交论文前，请确认以下事项：

- [ ] 所有章节内容已完成
- [ ] 摘要（中英文）已撰写
- [ ] 参考文献格式正确且完整
- [ ] 图表编号和引用正确
- [ ] 目录、图目录、表目录已生成
- [ ] 页眉页脚格式正确
- [ ] 封面信息准确无误
- [ ] 全文无编译错误和警告
- [ ] PDF 文件可正常打开和打印
- [ ] 符合学校最新格式要求

---

**祝您顺利完成论文！🎓**

如有问题，请参考上述资源或联系模板作者。

---

*最后更新：2026年1月*

