# 论文文档结构说明

## 📂 文件组织结构

```
mypaper/
├── mythesis.tex                  # 主文档（入口文件）
├── mythesis.bib                  # 参考文献数据库
├── README.md                     # 使用说明文档
├── STRUCTURE.md                  # 本文件：结构说明
│
├── chapters/                     # 章节目录
│   ├── chapter1.tex             # 第一章：绪论
│   ├── chapter2.tex             # 第二章：相关工作
│   ├── chapter3.tex             # 第三章：视觉数据构造框架
│   ├── chapter4.tex             # 第四章：GUI
│   ├── chapter5.tex             # 第五章：世界知识
│   └── chapter6.tex             # 第六章：结论
│
├── figures/                      # 图片目录（建议创建）
│   ├── chapter1/
│   ├── chapter2/
│   └── ...
│
└── tables/                       # 表格目录（可选）
    └── ...
```

---

## 📖 主文档结构（mythesis.tex）

主文档 `mythesis.tex` 采用模块化组织，包含以下几个部分：

### 1. 文档类和宏包导入
```latex
\documentclass[twoside]{fduthesis}
% 导入必要的宏包
```

### 2. 论文信息配置（\fdusetup）
```latex
\fdusetup{
  style = { ... },    % 样式设置
  info = { ... }      % 论文元信息
}
```

**包含的信息：**
- 中英文标题
- 作者姓名（中英文）
- 导师姓名
- 专业、院系
- 学号
- 关键词（中英文）
- 中图分类号
- 密级等

### 3. 自定义命令和宏定义
根据需要添加自定义命令

### 4. 正文部分

#### 4.1 前置部分 (\frontmatter)
- **目录** (`\tableofcontents`)
- **插图目录** (`\listoffigures`)
- **表格目录** (`\listoftables`)
- **中文摘要** (`\begin{abstract}...\end{abstract}`)
- **英文摘要** (`\begin{abstract*}...\end{abstract*}`)
- **符号说明** (`\begin{notation}...\end{notation}`)

#### 4.2 主体部分 (\mainmatter)
通过 `\input` 命令引入各章节文件：

```latex
\mainmatter

% 第一章：绪论
\input{chapters/chapter1}

% 第二章：相关工作
\input{chapters/chapter2}

% 第三章：视觉数据构造框架
\input{chapters/chapter3}

% 第四章：GUI
\input{chapters/chapter4}

% 第五章：世界知识
\input{chapters/chapter5}

% 第六章：结论
\input{chapters/chapter6}
```

#### 4.3 后置部分 (\backmatter)
- **参考文献** (`\printbibliography` 或 `\bibliography{mythesis}`)

---

## 📝 各章节文件说明

### Chapter 1: 绪论 (chapter1.tex)
**内容结构：**
- 研究背景
- 研究动机
- 研究目标
- 主要贡献
- 论文组织结构

**作用：** 介绍研究的背景、意义和论文的整体框架

---

### Chapter 2: 相关工作 (chapter2.tex)
**内容结构：**
- 多模态学习
- 视觉数据生成
- 数据合成方法
- 本章小结

**作用：** 综述相关领域的研究现状

---

### Chapter 3: 视觉数据构造框架 (chapter3.tex)
**内容结构：**
- 问题定义
- 构造框架
  - 数据表示
  - 构造流程
- 关键技术
- 本章小结

**作用：** 提出核心方法和理论框架

---

### Chapter 4: GUI (chapter4.tex)
**内容结构：**
- GUI数据特点
- GUI合成方法
  - 布局生成
  - 组件设计
- 实验与评估
  - 实验设置
  - 结果分析
- 本章小结

**作用：** 具体应用场景一：图形用户界面合成

---

### Chapter 5: 世界知识 (chapter5.tex)
**内容结构：**
- 世界知识的定义与作用
- 知识表示方法
- 知识融合策略
  - 知识提取
  - 知识整合
- 实验验证
- 本章小结

**作用：** 具体应用场景二：世界知识融合

---

### Chapter 6: 结论 (chapter6.tex)
**内容结构：**
- 研究总结
- 主要成果
- 创新点
- 不足与展望
  - 研究不足
  - 未来工作

**作用：** 总结全文，展望未来研究方向

---

## 🔧 编译方法

### 方法一：完整编译流程
```bash
cd /Users/minimax/Documents/finalpaper/fdu_paper/mypaper

# 使用 XeLaTeX 编译（推荐）
xelatex mythesis.tex
bibtex mythesis
xelatex mythesis.tex
xelatex mythesis.tex
```

### 方法二：使用 latexmk 自动编译
```bash
latexmk -xelatex mythesis.tex
```

### 方法三：清理临时文件后重新编译
```bash
# 清理临时文件
latexmk -c mythesis.tex
# 或手动删除
rm -f mythesis.aux mythesis.bbl mythesis.blg mythesis.log mythesis.out \
      mythesis.toc mythesis.lof mythesis.lot mythesis.thm

# 重新编译
xelatex mythesis.tex
bibtex mythesis.tex
xelatex mythesis.tex
xelatex mythesis.tex
```

---

## ✍️ 写作流程建议

### 第一步：完善论文元信息
编辑 `mythesis.tex` 中的 `\fdusetup` 部分，确保所有信息准确无误。

### 第二步：撰写摘要
- 在 `mythesis.tex` 中填写中英文摘要
- 摘要应简明扼要，包含研究目的、方法、结果和结论

### 第三步：更新符号说明
根据论文中实际使用的数学符号和缩写，修改 `\begin{notation}` 部分。

### 第四步：按章节顺序撰写内容
1. 建议从第一章开始，按顺序完成各章
2. 每完成一章，及时编译检查格式
3. 在各章节文件中直接编写内容

### 第五步：添加图表
- 将图片文件放入 `figures/` 目录
- 在章节文件中使用 `\includegraphics` 插入图片
- 使用 `\caption` 和 `\label` 添加标题和标签

### 第六步：添加参考文献
- 在 `mythesis.bib` 中添加参考文献条目
- 在正文中使用 `\cite{}` 引用
- 编译时确保运行 bibtex

### 第七步：全文校对
- 检查目录、图表目录是否完整
- 检查交叉引用是否正确
- 检查参考文献格式
- 检查页眉页脚

---

## 📌 重要提示

### 1. 文件编码
所有 `.tex` 和 `.bib` 文件必须使用 **UTF-8** 编码。

### 2. 文件命名
- 避免使用中文和特殊字符
- 使用小写字母和连字符
- 图片文件建议使用描述性名称

### 3. 图片格式
- 矢量图：优先使用 PDF 或 EPS 格式
- 位图：使用 PNG 格式（不推荐 JPG）
- 分辨率：至少 300 DPI

### 4. 版本控制
建议使用 Git 管理论文版本：
```bash
git init
git add mythesis.tex chapters/ mythesis.bib
git commit -m "论文初始结构"
```

### 5. 定期备份
- 每天备份工作进度
- 使用云盘同步（iCloud、OneDrive等）
- 保留重要版本的副本

### 6. 编译频率
- 建议每写完一小节就编译一次
- 及早发现和修复错误
- 避免积累大量未调试的代码

---

## 🎯 当前配置总结

| 项目 | 配置 |
|------|------|
| **论文标题** | 多模态视觉数据合成研究 |
| **作者** | 郑国栋 (Guodong Zheng) |
| **导师** | 黄萱菁 教授 |
| **专业** | 物理学 |
| **院系** | 凝聚态物理系 |
| **英文字体** | Times |
| **中文字体** | Fandol |
| **参考文献后端** | BibTeX |
| **参考文献样式** | numerical (数字式) |
| **文档类** | fduthesis (双面打印) |

---

## 📚 相关文档

- **使用说明**：`README.md`
- **模板文档**：[fduthesis.pdf](http://mirrors.ctan.org/macros/latex/contrib/fduthesis/fduthesis.pdf)
- **GitHub**：[https://github.com/stone-zeng/fduthesis](https://github.com/stone-zeng/fduthesis)

---

## ❓ 常见问题

### Q1: 如何修改章节标题？
直接编辑对应的章节文件（如 `chapters/chapter1.tex`），修改 `\chapter{...}` 中的内容。

### Q2: 如何添加新章节？
1. 创建新的章节文件（如 `chapters/chapter7.tex`）
2. 在 `mythesis.tex` 的 `\mainmatter` 部分添加 `\input{chapters/chapter7}`

### Q3: 如何在章节间添加附录？
在 `\backmatter` 之前添加：
```latex
\appendix
\input{chapters/appendixA}
```

### Q4: 编译时报错找不到章节文件？
检查：
1. 文件路径是否正确
2. 文件是否存在于 `chapters/` 目录
3. 文件名是否拼写正确

### Q5: 目录没有更新？
需要编译两次以上：
```bash
xelatex mythesis.tex  # 第一次
xelatex mythesis.tex  # 第二次（更新目录）
```

---

**最后更新：2026年1月**

祝论文写作顺利！📝

