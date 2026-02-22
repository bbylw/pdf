# PDF 参考（HTML-first）

## 1. 生成精美 PDF 的默认方案

优先采用 **HTML → PDF**：

1. 用 HTML/CSS 做页面结构与视觉设计（多页、组件化、响应式排版）。
2. 通过浏览器内核渲染并检查分页。
3. 使用 Chromium/Playwright 导出 PDF（保留背景色与高级样式）。

这比直接用 ReportLab 逐坐标绘制更适合复杂视觉设计和快速迭代。

---

## 2. 关键 CSS 规范

```css
@page {
  size: A4;
  margin: 14mm;
}

body {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.card, .table-block {
  break-inside: avoid;
}
```

分页控制：

- `page-break-after: always;` / `break-after: page;`
- `break-inside: avoid;`
- 对长表格在 HTML 层做分段（每页固定行数）

---

## 3. Playwright 导出 PDF 示例

```python
from playwright.async_api import async_playwright
import asyncio

async def export_pdf(html_path: str, output_pdf: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{html_path}", wait_until="networkidle")
        await page.pdf(
            path=output_pdf,
            format="A4",
            print_background=True,
            margin={"top": "14mm", "right": "14mm", "bottom": "14mm", "left": "14mm"},
        )
        await browser.close()

asyncio.run(export_pdf("report.html", "report.pdf"))
```

---

## 4. 与现有脚本配合

`pdf/scripts/create_premium_pdf.py` 已采用 HTML-first：

- 输出精美多页 HTML
- 可直接转 PDF
- 可通过 `--html-only` 仅导出 HTML，便于先调样式再生成 PDF

---

## 5. 仍然建议保留的 PDF 工具

- `pypdf`: 合并、拆分、旋转、元数据、页面级处理
- `pdfplumber`: 文本和表格抽取
- `pytesseract` + `pdf2image`: 扫描件 OCR
- `qpdf/poppler-utils`: 修复、检查、批处理
