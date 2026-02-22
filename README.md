# PDF Skill

An Amp agent skill for high-quality PDF creation, form filling, and manipulation — using an **HTML-first, print-first** workflow.

## Overview

This skill teaches Amp to produce premium, publication-grade PDFs by first designing pixel-perfect print-ready web pages, then rendering them to PDF via Playwright/Chromium. It also provides a complete toolkit for PDF form filling (both fillable and non-fillable forms), extraction, and manipulation.

## When to Use

| Scenario | Approach |
|---|---|
| 精美 / 品牌感 / 演示级 / 杂志风 / 报告风 PDF | **HTML → PDF**（默认） |
| 封面、目录、章节页、卡片、图表、复杂表格 | **HTML → PDF** |
| 快速迭代视觉风格或多次改版 | **HTML → PDF** |
| 极简纯文本 PDF / 坐标绘制 | ReportLab |
| 填写 PDF 表单 | 表单填写脚本 |
| PDF 合并 / 拆分 / 提取 | pypdf / pdfplumber |

## Core Workflow

```
1. Content Layering  →  Cover / TOC / Body / Appendix
2. Page Skeleton     →  Unified header/footer, margins, grid
3. Design Tokens     →  Colors, fonts, spacing (4/8pt system)
4. Print-safe CSS    →  @page, break-*, print-color-adjust
5. Data-driven HTML  →  Template / Jinja rendering
6. Playwright Export  →  page.pdf(print_background=True)
7. QA Checklist      →  Pagination, truncation, alignment, color
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
