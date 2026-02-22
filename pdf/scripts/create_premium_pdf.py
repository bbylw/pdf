#!/usr/bin/env python3
"""Generate a premium multi-page HTML report and optionally convert it to PDF.

Workflow:
1) Render branded HTML/CSS designed for paged PDF output.
2) Optionally convert HTML -> PDF via Playwright (Chromium).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from string import Template

HTML_TEMPLATE = Template(
    """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>${company} Executive Report</title>
  <style>
    :root {
      --bg: #0b1020;
      --panel: #121a2f;
      --panel-alt: #18213b;
      --border: #2a3559;
      --text: #e8ecf8;
      --muted: #a6b1ce;
      --accent: #6ee7f9;
      --accent-soft: #1e5d78;
      --good: #34d399;
    }

    @page {
      size: A4;
      margin: 14mm;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, "Segoe UI", Roboto, Arial, sans-serif;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .page {
      width: 100%;
      min-height: calc(297mm - 28mm);
      padding: 8mm;
      position: relative;
      background:
        radial-gradient(circle at 88% 8%, rgba(64, 156, 202, 0.16), transparent 26%),
        radial-gradient(circle at 12% 90%, rgba(110, 231, 249, 0.08), transparent 28%),
        var(--bg);
      page-break-after: always;
    }
    .page:last-child { page-break-after: auto; }

    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px;
    }

    .hero {
      background: linear-gradient(140deg, var(--panel-alt), #111a32);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 14px;
    }

    h1 {
      margin: 0;
      font-size: 26px;
      line-height: 1.2;
      letter-spacing: 0.2px;
    }

    .sub {
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted);
    }

    .grid {
      margin-top: 14px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }

    .metric-value {
      margin-top: 10px;
      font-size: 24px;
      font-weight: 700;
    }

    .chip {
      margin-top: 10px;
      display: inline-block;
      border-radius: 999px;
      background: rgba(30, 93, 120, 0.45);
      color: var(--accent);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
    }

    .muted { color: var(--muted); font-size: 12px; }

    .section-title {
      margin: 0 0 10px;
      font-size: 16px;
      font-weight: 700;
    }

    ol {
      margin: 0;
      padding-left: 20px;
    }
    li {
      margin-bottom: 12px;
      color: var(--muted);
      line-height: 1.5;
      font-size: 13px;
    }

    .kpi-list { margin-top: 8px; }
    .kpi-item { margin: 14px 0; }

    .kpi-head {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
    }

    .bar {
      width: 100%;
      height: 12px;
      border-radius: 999px;
      background: #1a2442;
      border: 1px solid var(--border);
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, #43d7eb, #6ee7f9);
    }

    .note {
      margin-top: 20px;
      font-size: 12px;
      color: var(--muted);
    }
  </style>
</head>
<body>
  <section class="page">
    <div class="hero">
      <h1>${company} — Executive Intelligence Report</h1>
      <div class="sub">Prepared for leadership • Period: ${month} • Generated: ${generated_date}</div>
    </div>

    <div class="grid">
      <article class="panel">
        <div class="muted">Revenue</div>
        <div class="metric-value">$$4.28M</div>
        <span class="chip">+12.4%</span>
      </article>
      <article class="panel">
        <div class="muted">Gross Margin</div>
        <div class="metric-value">63.8%</div>
        <span class="chip">+2.1%</span>
      </article>
      <article class="panel">
        <div class="muted">NPS</div>
        <div class="metric-value">72</div>
        <span class="chip">+5 pts</span>
      </article>
    </div>

    <div class="panel" style="margin-top:14px;">
      <h2 class="section-title">Strategic Highlights</h2>
      <ol>
        <li>Pipeline quality improved due to tighter qualification workflows.</li>
        <li>Regional expansion contributed 31% of net-new growth this month.</li>
        <li>Onboarding cycle reduced by 18%, improving activation conversion and retention.</li>
        <li>Recommend increasing enterprise ABM budget by 8% next quarter.</li>
      </ol>
    </div>
  </section>

  <section class="page">
    <div class="hero">
      <h1>KPI Performance Matrix</h1>
      <div class="sub">Target attainment across strategic objectives</div>
    </div>

    <div class="panel kpi-list">
      ${kpi_rows}
      <p class="note"><strong>Note:</strong> Values are normalized against quarterly targets and seasonality adjustments.</p>
    </div>
  </section>
</body>
</html>
"""
)


def make_kpi_rows(kpis: list[tuple[str, float]]) -> str:
    rows = []
    for label, score in kpis:
        percent = int(round(score * 100))
        rows.append(
            "\n".join(
                [
                    '<div class="kpi-item">',
                    f'  <div class="kpi-head"><span>{label}</span><strong>{percent}%</strong></div>',
                    '  <div class="bar">',
                    f'    <div class="bar-fill" style="width:{percent}%;"></div>',
                    "  </div>",
                    "</div>",
                ]
            )
        )
    return "\n".join(rows)


def write_html(output_html: Path, company: str, month: str) -> None:
    kpis = [
        ("Enterprise Pipeline", 0.84),
        ("Product Adoption", 0.68),
        ("Retention Expansion", 0.77),
        ("Support SLA Compliance", 0.92),
        ("Partner Channel Activation", 0.58),
    ]
    html = HTML_TEMPLATE.substitute(
        company=company,
        month=month,
        generated_date=dt.date.today().isoformat(),
        kpi_rows=make_kpi_rows(kpis),
    )
    output_html.write_text(html, encoding="utf-8")


async def html_to_pdf_playwright(input_html: Path, output_pdf: Path) -> None:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(input_html.resolve().as_uri(), wait_until="networkidle")
        await page.pdf(
            path=str(output_pdf),
            format="A4",
            print_background=True,
            margin={"top": "14mm", "right": "14mm", "bottom": "14mm", "left": "14mm"},
        )
        await browser.close()


def convert_html_to_pdf(input_html: Path, output_pdf: Path) -> None:
    try:
        import asyncio

        asyncio.run(html_to_pdf_playwright(input_html, output_pdf))
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Playwright is not installed. Run `pip install playwright && playwright install chromium`, "
            "or use --html-only to export just the HTML."
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Create premium report with HTML-first PDF workflow")
    parser.add_argument("-o", "--output", default="premium_report.pdf", help="Output PDF path")
    parser.add_argument("--html", default="premium_report.html", help="Intermediate HTML output path")
    parser.add_argument("--company", default="Northstar Dynamics", help="Company name")
    parser.add_argument("--month", default=dt.date.today().strftime("%B %Y"), help="Reporting month")
    parser.add_argument("--html-only", action="store_true", help="Generate HTML only, skip PDF conversion")
    parser.add_argument("--dump-manifest", help="Optional JSON manifest output with generated files")
    args = parser.parse_args()

    output_html = Path(args.html)
    output_pdf = Path(args.output)

    write_html(output_html, args.company, args.month)

    generated = {"html": str(output_html)}
    if not args.html_only:
        convert_html_to_pdf(output_html, output_pdf)
        generated["pdf"] = str(output_pdf)

    if args.dump_manifest:
        Path(args.dump_manifest).write_text(json.dumps(generated, ensure_ascii=False, indent=2), encoding="utf-8")

    if "pdf" in generated:
        print(f"Created HTML: {generated['html']}\nCreated PDF: {generated['pdf']}")
    else:
        print(f"Created HTML only: {generated['html']}")


if __name__ == "__main__":
    main()
