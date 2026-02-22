# PDF 参考（面向“精美打印稿”的 HTML-first）

## 1) 核心原则

- 先做“打印页面设计”，再做 PDF；不是普通网页截图。
- 先锁定页尺寸、页边距、分页规则，再填内容。
- 统一设计令牌（颜色、字号、间距）提升成品一致性。

## 2) 打印样式最小模板

```css
@page {
  size: A4;
  margin: 14mm;
}

html, body {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page { break-after: page; }
.card, .table-block, .chart-block { break-inside: avoid; }
```

## 3) 让 PDF 更“高级”的网页策略

- 封面页与正文页使用不同布局节奏（封面可更大胆）。
- 正文控制每页信息密度：保留留白，避免堆满。
- 卡片统一圆角/边框/阴影强度，减少杂乱感。
- 表格采用“标题 + 注释 + 单位”三段式，提升专业感。

## 4) Playwright 导出基线

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

## 5) 与现有脚本配合

`pdf/scripts/create_premium_pdf.py`：

- 可快速生成多页精美 HTML。
- 默认支持转换到 PDF。
- `--html-only` 可用于先看版式、再导出。

## 6) 常见失败模式（避免）

- 只做屏幕端样式，未检查打印分页。
- 长表格直接跨页导致表头丢失。
- 字号和间距缺乏统一规则，页面“拼贴感”重。
- PDF 中背景色丢失（忘记 `print_background=True`）。
