# PDF 工具集

一个面向 **PDF 表单处理** 与 **高质量 PDF 生成（HTML-first）** 的实用脚本仓库。

目前仓库主要覆盖两类场景：

- **表单填写工作流**：自动检测可填写字段、提取字段结构、批量填充表单。
- **高级报告生成工作流**：先生成可打印 HTML，再导出带设计感的 PDF。

---

## 目录结构

```text
.
├── README.md
└── pdf
    ├── forms.md                  # 表单填写完整操作手册
    ├── reference.md              # HTML-first 设计与导出参考
    ├── scripts
    │   ├── check_fillable_fields.py
    │   ├── extract_form_field_info.py
    │   ├── fill_fillable_fields.py
    │   ├── extract_form_structure.py
    │   ├── fill_pdf_form_with_annotations.py
    │   ├── check_bounding_boxes.py
    │   ├── create_validation_image.py
    │   ├── convert_pdf_to_images.py
    │   └── create_premium_pdf.py
    └── LICENSE.txt
```

---

## 环境准备

建议使用 Python 3.10+。

安装常用依赖：

```bash
pip install pypdf pdf2image pdfplumber pillow playwright
playwright install chromium
```

> 说明：
>
> - `pdf2image` 依赖系统层的 Poppler。
> - `create_premium_pdf.py` 导出 PDF 时依赖 Playwright + Chromium；如果仅输出 HTML 可不安装浏览器。

---

## 快速开始

### 1) 判断 PDF 是否可填写

```bash
python pdf/scripts/check_fillable_fields.py input.pdf
```

- 如果输出可填写（fillable），走“可填写字段”流程。
- 否则走“非可填写字段（注释写入）”流程。

详细步骤见：`pdf/forms.md`。

---

## 可填写字段流程（Fillable Fields）

### 步骤 A：提取字段信息

```bash
python pdf/scripts/extract_form_field_info.py input.pdf field_info.json
```

`field_info.json` 会包含每个字段的：

- `field_id`
- `page`
- `type`（如 text / checkbox / radio_group / choice）
- 对应选项值（checkbox/radio/choice）

### 步骤 B：准备要填入的值

按脚本要求创建 `field_values.json`。

### 步骤 C：批量写入字段

```bash
python pdf/scripts/fill_fillable_fields.py input.pdf field_values.json output.pdf
```

脚本会校验字段 ID、页码及选项合法性，并在错误时给出提示。

---

## 非可填写字段流程（Non-fillable Fields）

### 方式 A（推荐）：基于结构提取

```bash
python pdf/scripts/extract_form_structure.py input.pdf form_structure.json
```

用于提取：

- 文本标签
- 水平线（行边界）
- 复选框位置

随后根据坐标生成字段描述并进行注释写入。

### 方式 B：注释写入

```bash
python pdf/scripts/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```

---

## 坐标/边界辅助工具

### 将 PDF 转图片（便于人工核对）

```bash
python pdf/scripts/convert_pdf_to_images.py input.pdf out_images
```

### 检查字段框是否重叠或过小

```bash
python pdf/scripts/check_bounding_boxes.py fields.json
```

### 生成标注预览图（红框 entry / 蓝框 label）

```bash
python pdf/scripts/create_validation_image.py 1 fields.json page_1.png validation_page_1.png
```

---

## 高级 PDF 生成（HTML-first）

`pdf/scripts/create_premium_pdf.py` 提供一个“可打印网页 → PDF”的标准范例，适合生成报告类文档。

### 生成 HTML + PDF

```bash
python pdf/scripts/create_premium_pdf.py \
  --company "Northstar Dynamics" \
  --month "March 2026" \
  --html report.html \
  --output report.pdf
```

### 仅生成 HTML（先调样式）

```bash
python pdf/scripts/create_premium_pdf.py \
  --company "Northstar Dynamics" \
  --month "March 2026" \
  --html report.html \
  --html-only
```

更多设计与打印规范请参考：`pdf/reference.md`。

---

## 建议工作方式

- 先按 `pdf/forms.md` 的顺序执行，避免遗漏关键步骤。
- 对非 fillable PDF，优先尝试 `extract_form_structure.py`，再退回人工视觉估计。
- 对“展示级”PDF，优先 HTML-first 工作流，保留 HTML 便于后续视觉迭代。

---

## 许可

仓库包含 `pdf/LICENSE.txt`，请在使用前确认许可条款。
