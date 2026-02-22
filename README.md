# PDF Skill

An Amp agent skill for high-quality PDF creation, form filling, and manipulation — using an **HTML-first, print-first** workflow.

## Overview

This skill teaches Amp to produce premium, publication-grade PDFs by first designing pixel-perfect print-ready web pages, then rendering them to PDF via Playwright/Chromium. It also provides a complete toolkit for PDF form filling (both fillable and non-fillable forms), extraction, and manipulation.

## When to Use

- **HTML → PDF (default)**: Premium / brand / presentation / magazine / report style; covers, TOC, chapter pages, cards, charts, complex tables; rapid visual iteration.
- **ReportLab**: Minimal plain-text PDF or coordinate-based drawing.
- **Form filling scripts**: Fill PDF forms (fillable or non-fillable).
- **pypdf / pdfplumber**: Merge, split, extract PDFs.

## Core Workflow

```
1. Content Layering   →  Cover / TOC / Body / Appendix
2. Page Skeleton      →  Unified header/footer, margins, grid
3. Design Tokens      →  Colors, fonts, spacing (4/8pt system)
4. Print-safe CSS     →  @page, break-*, print-color-adjust
5. Data-driven HTML   →  Template / Jinja rendering
6. Playwright Export  →  page.pdf(print_background=True)
7. QA Checklist       →  Pagination, truncation, alignment, color
```

## Scripts

All scripts are located in the `scripts/` directory:

| Script | Description |
|---|---|
| `create_premium_pdf.py` | Generate multi-page premium HTML and export to PDF |
| `convert_pdf_to_images.py` | Convert PDF pages to PNG images |
| `check_fillable_fields.py` | Check if a PDF has fillable form fields |
| `extract_form_field_info.py` | Extract fillable field metadata to JSON |
| `fill_fillable_fields.py` | Fill fillable PDF form fields from JSON |
| `extract_form_structure.py` | Extract text labels, lines, checkboxes from non-fillable PDFs |
| `check_bounding_boxes.py` | Validate bounding boxes before filling |
| `fill_pdf_form_with_annotations.py` | Fill non-fillable PDFs via text annotations |
| `create_validation_image.py` | Create validation overlay images |

### Quick Start — Premium PDF

```bash
python scripts/create_premium_pdf.py \
  --company "Northstar Dynamics" \
  --month "March 2026" \
  --html report.html \
  --output report.pdf
```

Use `--html-only` to preview the HTML layout before exporting to PDF.

### Quick Start — Form Filling

```bash
# 1. Check if the PDF has fillable fields
python scripts/check_fillable_fields.py form.pdf

# 2a. Fillable → extract fields, fill, and export
python scripts/extract_form_field_info.py form.pdf fields.json
python scripts/fill_fillable_fields.py form.pdf field_values.json output.pdf

# 2b. Non-fillable → extract structure, annotate, and export
python scripts/extract_form_structure.py form.pdf structure.json
python scripts/fill_pdf_form_with_annotations.py form.pdf fields.json output.pdf

# 3. Verify output
python scripts/convert_pdf_to_images.py output.pdf verify/
```

## Design Principles

- **Print-first**: Design for fixed page sizes (A4/Letter), not infinite scroll.
- **Design tokens**: Unified colors, typography, and spacing across all pages.
- **Explicit pagination**: Section breaks, avoid element splitting, segmented long tables.
- **Browser validation**: Always verify in print preview before exporting.
- **Preserve HTML**: Keep the HTML source alongside the PDF for easy iteration.

## Default CSS Baseline

```css
:root {
  --bg: #f6f8fb;
  --surface: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --brand: #2563eb;
  --radius: 12px;
}

@page { size: A4; margin: 14mm; }

html, body {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page { break-after: page; }
.card, .table-block, .chart-block { break-inside: avoid; }
```

## Dependencies

| Task | Library |
|---|---|
| HTML → PDF export | Playwright (Chromium) |
| Edit / merge / split / metadata | pypdf |
| Text & table extraction | pdfplumber |
| OCR | pytesseract + pdf2image |

## File Structure

```
pdf/
├── SKILL.md          # Skill definition & instructions
├── reference.md      # Design reference & Playwright export baseline
├── forms.md          # Form filling workflow (fillable & non-fillable)
├── LICENSE.txt       # License
├── README.md         # This file
└── scripts/
    ├── create_premium_pdf.py
    ├── convert_pdf_to_images.py
    ├── check_fillable_fields.py
    ├── extract_form_field_info.py
    ├── extract_form_structure.py
    ├── fill_fillable_fields.py
    ├── fill_pdf_form_with_annotations.py
    ├── check_bounding_boxes.py
    └── create_validation_image.py
```

## License

© 2025 Anthropic, PBC. All rights reserved. See [LICENSE.txt](LICENSE.txt) for details.

---

# PDF 技能

一个用于高质量 PDF 创建、表单填写和文档处理的 Amp 智能体技能——采用 **HTML 优先、打印优先** 的工作流。

## 概述

本技能让 Amp 通过先设计像素级精准的可打印网页，再经由 Playwright/Chromium 渲染为 PDF，从而生成出版级精美 PDF。同时提供完整的 PDF 表单填写（支持可填写和不可填写表单）、提取和处理工具集。

## 使用场景

- **HTML → PDF（默认）**：精美 / 品牌感 / 演示级 / 杂志风 / 报告风；封面、目录、章节页、卡片、图表、复杂表格；快速迭代视觉风格或多次改版。
- **ReportLab**：极简纯文本 PDF 或坐标绘制。
- **表单填写脚本**：填写 PDF 表单（可填写或不可填写）。
- **pypdf / pdfplumber**：合并、拆分、提取 PDF。

## 核心工作流

```
1. 内容分层    →  封面 / 目录 / 正文章节 / 附录
2. 页面骨架    →  统一页眉页脚、页边距、栅格
3. 设计令牌    →  颜色、字体、间距（4/8pt 体系）
4. 打印安全样式 →  @page、break-*、print-color-adjust
5. 数据驱动渲染 →  模板 / Jinja / 字符串模板
6. Playwright 导出 →  page.pdf(print_background=True)
7. 质量验收    →  分页、截断、对齐、色彩、可读性
```

## 脚本工具

所有脚本位于 `scripts/` 目录下：

| 脚本 | 描述 |
|---|---|
| `create_premium_pdf.py` | 生成多页精美 HTML 并导出 PDF |
| `convert_pdf_to_images.py` | 将 PDF 页面转换为 PNG 图片 |
| `check_fillable_fields.py` | 检查 PDF 是否含有可填写表单字段 |
| `extract_form_field_info.py` | 提取可填写字段元数据为 JSON |
| `fill_fillable_fields.py` | 根据 JSON 填写可填写表单字段 |
| `extract_form_structure.py` | 从不可填写 PDF 中提取文本标签、线条、复选框 |
| `check_bounding_boxes.py` | 填写前验证边界框 |
| `fill_pdf_form_with_annotations.py` | 通过文本注释填写不可填写 PDF |
| `create_validation_image.py` | 创建验证叠加图像 |

### 快速上手 — 精美 PDF

```bash
python scripts/create_premium_pdf.py \
  --company "Northstar Dynamics" \
  --month "March 2026" \
  --html report.html \
  --output report.pdf
```

使用 `--html-only` 可先预览 HTML 排版效果，再导出 PDF。

### 快速上手 — 表单填写

```bash
# 1. 检查 PDF 是否有可填写字段
python scripts/check_fillable_fields.py form.pdf

# 2a. 可填写 → 提取字段、填写、导出
python scripts/extract_form_field_info.py form.pdf fields.json
python scripts/fill_fillable_fields.py form.pdf field_values.json output.pdf

# 2b. 不可填写 → 提取结构、注释填写、导出
python scripts/extract_form_structure.py form.pdf structure.json
python scripts/fill_pdf_form_with_annotations.py form.pdf fields.json output.pdf

# 3. 验证输出
python scripts/convert_pdf_to_images.py output.pdf verify/
```

## 设计原则

- **打印优先**：以固定页面尺寸（A4/Letter）为设计基准，而非无限滚动页面。
- **设计令牌**：所有页面统一颜色、字体和间距。
- **显式分页**：章节换页、避免元素拆分、长表格分段。
- **浏览器验证**：导出前始终在打印预览中验证。
- **保留 HTML**：保存 HTML 源文件，便于后续视觉迭代。

## 默认 CSS 基线

```css
:root {
  --bg: #f6f8fb;
  --surface: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --brand: #2563eb;
  --radius: 12px;
}

@page { size: A4; margin: 14mm; }

html, body {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page { break-after: page; }
.card, .table-block, .chart-block { break-inside: avoid; }
```

## 依赖库

| 任务 | 库 |
|---|---|
| HTML → PDF 导出 | Playwright (Chromium) |
| 编辑 / 合并 / 拆分 / 元数据 | pypdf |
| 文本与表格提取 | pdfplumber |
| OCR 识别 | pytesseract + pdf2image |

## 目录结构

```
pdf/
├── SKILL.md          # 技能定义与指令
├── reference.md      # 设计参考与 Playwright 导出基线
├── forms.md          # 表单填写工作流（可填写与不可填写）
├── LICENSE.txt       # 许可证
├── README.md         # 本文件
└── scripts/
    ├── create_premium_pdf.py
    ├── convert_pdf_to_images.py
    ├── check_fillable_fields.py
    ├── extract_form_field_info.py
    ├── extract_form_structure.py
    ├── fill_fillable_fields.py
    ├── fill_pdf_form_with_annotations.py
    ├── check_bounding_boxes.py
    └── create_validation_image.py
```

## 许可证

© 2025 Anthropic, PBC. 保留所有权利。详见 [LICENSE.txt](LICENSE.txt)。
