---
name: pdf
description: Use this skill for PDF tasks including reading/extracting content, form filling, merging/splitting, OCR, and especially creating polished multi-page PDFs through an HTML-first workflow (build styled paged HTML, validate in browser, then convert HTML to PDF).
---

# PDF Skill (HTML-first)

## Core rule for PDF generation

When a user asks for a **beautiful / premium / presentation-grade / visually polished** PDF:

1. Build a paged HTML document first (`@page`, `page-break-*`, CSS grid/flex, reusable components).
2. Ensure multi-page layout looks correct in browser print preview.
3. Convert that HTML to PDF with a browser engine (Playwright/Chromium preferred).
4. Keep the HTML artifact so it can be edited in later iterations.

Do **not** start with plain ReportLab text flow unless the user explicitly wants a minimal/basic PDF.

## Recommended implementation workflow

1. **Structure content**: title page / sections / appendix and define per-page blocks.
2. **Define design tokens** in CSS (`:root` colors, spacing, typography scale, card radius).
3. **Use print-safe CSS**:
   - `@page { size: A4; margin: ... }`
   - `print-color-adjust: exact`
   - avoid element splits via `break-inside: avoid` for cards/tables/charts.
4. **Render HTML** from template data (Jinja/string template are both fine).
5. **Export PDF** with headless Chromium.
6. **Validate output**: page count, overflow/cutoff, alignment, and readability.

## Default tooling choices

- **Creation / edits / merge / split / metadata**: `pypdf`
- **Table/text extraction**: `pdfplumber`
- **Scanned OCR fallback**: `pytesseract` + `pdf2image`
- **HTML to PDF rendering**: Playwright Chromium (`page.pdf(print_background=True)`)

## Bundled script for premium output

Use `scripts/create_premium_pdf.py` as the starter pipeline:

- Generates a styled, multi-page HTML report.
- Converts HTML → PDF via Playwright unless `--html-only` is set.
- Supports `--company`, `--month`, and output paths.

Example:

```bash
python pdf/scripts/create_premium_pdf.py \
  --company "Northstar Dynamics" \
  --month "March 2026" \
  --html report.html \
  --output report.pdf
```

If Playwright/browser runtime is not available, run with `--html-only` first and install runtime later.

## Form tasks

For fillable forms and annotation overlays, follow `forms.md` and scripts under `scripts/` (field extraction, coordinate checks, filling).

## Quality checklist before delivering generated PDFs

- No clipped text at page boundaries.
- Consistent typography and spacing across pages.
- Chart/table headers repeat or remain clear across page breaks.
- Brand colors preserved in print (`print_background=True`).
- Source HTML and final PDF both saved.
