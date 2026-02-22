---
name: pdf
description: Use this skill for PDF tasks including extraction/form filling and especially high-end PDF creation via an HTML-first, print-first workflow (design premium paged web layouts, validate print pagination, then render with Chromium/Playwright).
---

# PDF Skill (HTML-first, print-first)

当用户要“精美/高级感/可商用展示”的 PDF 时，默认走 **HTML→PDF**，不是先写 ReportLab。

## Trigger: 什么时候必须用 HTML-first

满足任一条件就用 HTML-first：

- 要求“精美、品牌感、演示级、杂志风、报告风”。
- 有封面、目录、章节页、卡片、图表、复杂表格。
- 需要快速迭代视觉风格或多次改版。

仅在用户明确要求“极简文本 PDF”或“纯坐标绘制”时，才退回 ReportLab-first。

## Non-negotiables（生成精美 PDF 的硬约束）

1. **先产出可打印网页**（A4/A3/Letter 目标页）。
2. **使用设计令牌（design tokens）**统一颜色、字号、间距、圆角、阴影。
3. **显式分页策略**：章节换页、模块防拆、长表分段。
4. **导出前在浏览器打印语义验证**（不是只看普通屏幕视图）。
5. **保留 HTML 成品**，便于后续视觉迭代。

## 推荐工作流（默认执行顺序）

1. **内容分层**：封面 / 目录 / 正文章节 / 附录。
2. **建立页面骨架**：统一 header/footer、页边距、栅格。
3. **定义 tokens**：
   - 颜色：主色/强调色/中性色/语义色
   - 字体：标题、正文、数据字体
   - 间距：4/8pt 体系
4. **实现 print-safe CSS**：`@page`、`break-*`、`print-color-adjust`。
5. **数据驱动渲染 HTML**（模板/Jinja/字符串模板均可）。
6. **Playwright 导出 PDF**（`print_background=True`）。
7. **QA 清单验收**（分页、截断、对齐、色彩、可读性）。

## PDF 专用网页设计规范（重点）

> 目标不是“普通网页好看”，而是“打印后每页都好看”。

### 1) 页面与网格

- 使用固定打印尺寸（如 A4）思维设计，而非无限滚动页面。
- 每页维持一致的纵向节奏（标题区、内容区、页脚区）。
- 常用版式：
  - 封面：大标题 + 副标题 + 品牌区
  - 内容页：`2-column`（主内容 + 侧栏）
  - 数据页：卡片栅格 + 图表 + 说明块

### 2) 字体与层级

- 标题层级不超过 4 级（H1/H2/H3/body）。
- 正文建议 10.5–12pt，行高 1.4–1.6。
- 同一页最多 2 种字体家族，避免“网页感过重”。

### 3) 视觉精致度（Premium signals）

- 使用轻微层次：细边框、低强度阴影、柔和背景分区。
- 保持大留白，不把页面塞满。
- 图表/表格的标题、注释、单位必须风格一致。

### 4) 打印兼容

- 必设：
  - `@page { size: A4; margin: ... }`
  - `print-color-adjust: exact`
- 对卡片、表格、图块设置 `break-inside: avoid`。
- 长表格按页切分，避免跨页断头断尾。

## 默认 CSS/结构基线（可直接复用）

```css
:root {
  --bg: #f6f8fb;
  --surface: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --brand: #2563eb;
  --radius: 12px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
}

@page { size: A4; margin: 14mm; }

html, body {
  margin: 0;
  padding: 0;
  color: var(--text);
  background: var(--bg);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page {
  break-after: page;
  min-height: calc(297mm - 28mm);
}

.card, .table-block, .chart-block { break-inside: avoid; }
```

## 导出实现优先级

- **首选**：Playwright Chromium（`page.pdf()`）。
- 参数基线：`format='A4'`、`print_background=True`、与 `@page` 一致的 margin。
- 若浏览器运行时不可用：先 `--html-only` 输出 HTML，再补导出。

## Bundled script

优先复用：`pdf/scripts/create_premium_pdf.py`

- 生成多页高质量 HTML。
- 支持 HTML→PDF 导出。
- 支持 `--html-only` 先调样式。

示例：

```bash
python pdf/scripts/create_premium_pdf.py \
  --company "Northstar Dynamics" \
  --month "March 2026" \
  --html report.html \
  --output report.pdf
```

## 其他任务工具选择

- 编辑/合并/拆分/元数据：`pypdf`
- 文本表格提取：`pdfplumber`
- OCR：`pytesseract` + `pdf2image`

## 交付前质量门禁（必须逐项检查）

- 无文本截断、无关键元素被切页。
- 每页视觉重心稳定，页间风格一致。
- 标题、图例、表头、单位格式一致。
- 品牌色与背景色在 PDF 中正确保留。
- 同时保存 HTML 与 PDF，便于下一轮优化。
