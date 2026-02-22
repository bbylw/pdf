#!/usr/bin/env python3
"""Generate a premium, professional PDF report with a modern visual system."""

from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


@dataclass(frozen=True)
class Palette:
    """Design tokens for a refined dark report aesthetic."""

    bg: colors.Color = colors.HexColor("#0B1020")
    panel: colors.Color = colors.HexColor("#121A2F")
    panel_alt: colors.Color = colors.HexColor("#18213B")
    border: colors.Color = colors.HexColor("#2A3559")
    text_primary: colors.Color = colors.HexColor("#E8ECF8")
    text_secondary: colors.Color = colors.HexColor("#A6B1CE")
    accent: colors.Color = colors.HexColor("#6EE7F9")
    accent_soft: colors.Color = colors.HexColor("#1E5D78")
    positive: colors.Color = colors.HexColor("#34D399")


def rounded_panel(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill: colors.Color, stroke: colors.Color) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius=10, fill=1, stroke=1)


def draw_paragraph(c: canvas.Canvas, text: str, style: ParagraphStyle, x: float, y: float, w: float, h: float) -> None:
    paragraph = Paragraph(text, style)
    paragraph.wrapOn(c, w, h)
    paragraph.drawOn(c, x, y)


def add_page_background(c: canvas.Canvas, page_w: float, page_h: float, palette: Palette) -> None:
    c.setFillColor(palette.bg)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Ambient gradient-like circles for subtle depth.
    c.setFillColor(colors.Color(0.2, 0.45, 0.65, alpha=0.12))
    c.circle(page_w - 40 * mm, page_h - 35 * mm, 42 * mm, fill=1, stroke=0)
    c.setFillColor(colors.Color(0.4, 0.8, 0.9, alpha=0.09))
    c.circle(35 * mm, 30 * mm, 30 * mm, fill=1, stroke=0)


def draw_metric_card(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    value: str,
    delta: str,
    styles: dict[str, ParagraphStyle],
    palette: Palette,
) -> None:
    rounded_panel(c, x, y, w, h, palette.panel, palette.border)

    draw_paragraph(c, label, styles["small"], x + 10, y + h - 22, w - 20, 16)
    draw_paragraph(c, f"<b>{value}</b>", styles["metric"], x + 10, y + h - 54, w - 20, 34)

    c.setFillColor(palette.accent_soft)
    c.roundRect(x + 10, y + 10, 48, 18, radius=8, fill=1, stroke=0)
    draw_paragraph(c, f"<b>{delta}</b>", styles["chip"], x + 16, y + 13, 42, 12)


def generate_report(output_path: str, company_name: str, report_month: str) -> None:
    page_w, page_h = A4
    c = canvas.Canvas(output_path, pagesize=A4)
    palette = Palette()
    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=30,
        leading=36,
        textColor=palette.text_primary,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=palette.text_secondary,
    )
    section = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=palette.text_primary,
    )
    small = ParagraphStyle("Small", parent=styles["Normal"], fontName="Helvetica", fontSize=8, textColor=palette.text_secondary)
    metric = ParagraphStyle("Metric", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=18, textColor=palette.text_primary)
    chip = ParagraphStyle("Chip", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, textColor=palette.accent)
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=palette.text_secondary,
    )

    style_map = {"small": small, "metric": metric, "chip": chip}

    # Page 1: Executive overview
    add_page_background(c, page_w, page_h, palette)

    rounded_panel(c, 18 * mm, page_h - 52 * mm, page_w - 36 * mm, 32 * mm, palette.panel_alt, palette.border)
    draw_paragraph(c, f"<b>{company_name}</b> — Executive Intelligence Report", title, 24 * mm, page_h - 44 * mm, page_w - 48 * mm, 26 * mm)
    draw_paragraph(
        c,
        f"Prepared for leadership • Period: {report_month} • Generated: {dt.date.today().isoformat()}",
        subtitle,
        24 * mm,
        page_h - 52 * mm,
        page_w - 48 * mm,
        10 * mm,
    )

    card_y = page_h - 90 * mm
    card_w = (page_w - 48 * mm) / 3
    draw_metric_card(c, 18 * mm, card_y, card_w, 28 * mm, "Revenue", "$4.28M", "+12.4%", style_map, palette)
    draw_metric_card(c, 18 * mm + card_w + 6 * mm, card_y, card_w, 28 * mm, "Gross Margin", "63.8%", "+2.1%", style_map, palette)
    draw_metric_card(c, 18 * mm + 2 * (card_w + 6 * mm), card_y, card_w, 28 * mm, "NPS", "72", "+5 pts", style_map, palette)

    # Insights panel
    rounded_panel(c, 18 * mm, 28 * mm, page_w - 36 * mm, page_h - 130 * mm, palette.panel, palette.border)
    draw_paragraph(c, "<b>Strategic Highlights</b>", section, 24 * mm, page_h - 126 * mm, 70 * mm, 10 * mm)
    insight_html = (
        "<b>1.</b> Pipeline quality improved due to tighter qualification workflows.<br/><br/>"
        "<b>2.</b> Regional expansion contributed 31% of net-new growth this month.<br/><br/>"
        "<b>3.</b> Onboarding cycle reduced by 18%, improving activation conversion and retention.<br/><br/>"
        "<b>4.</b> Recommend increasing enterprise ABM budget by 8% next quarter."
    )
    draw_paragraph(c, insight_html, body, 24 * mm, 48 * mm, page_w - 48 * mm, page_h - 160 * mm)

    c.showPage()

    # Page 2: KPI bars
    add_page_background(c, page_w, page_h, palette)
    draw_paragraph(c, "<b>KPI Performance Matrix</b>", title, 18 * mm, page_h - 34 * mm, page_w - 36 * mm, 24 * mm)
    draw_paragraph(c, "Target attainment across strategic objectives", subtitle, 18 * mm, page_h - 42 * mm, page_w - 36 * mm, 10 * mm)

    rounded_panel(c, 18 * mm, 20 * mm, page_w - 36 * mm, page_h - 72 * mm, palette.panel, palette.border)

    kpis = [
        ("Enterprise Pipeline", 0.84),
        ("Product Adoption", 0.68),
        ("Retention Expansion", 0.77),
        ("Support SLA Compliance", 0.92),
        ("Partner Channel Activation", 0.58),
    ]

    top = page_h - 72 * mm
    bar_x = 50 * mm
    bar_w = page_w - 86 * mm
    for i, (name, score) in enumerate(kpis):
        y = top - i * 28 * mm
        draw_paragraph(c, name, subtitle, 24 * mm, y + 6, 24 * mm, 12)

        c.setFillColor(palette.panel_alt)
        c.roundRect(bar_x, y + 4, bar_w, 8, radius=4, fill=1, stroke=0)

        fill_w = bar_w * score
        c.setFillColor(palette.accent)
        c.roundRect(bar_x, y + 4, fill_w, 8, radius=4, fill=1, stroke=0)

        draw_paragraph(c, f"<b>{int(score * 100)}%</b>", subtitle, bar_x + bar_w + 4, y + 6, 24, 12)

    draw_paragraph(
        c,
        "<b>Note:</b> Values are normalized against quarterly targets and seasonality adjustments.",
        body,
        24 * mm,
        26 * mm,
        page_w - 48 * mm,
        20,
    )

    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a premium multi-page PDF report")
    parser.add_argument("-o", "--output", default="premium_report.pdf", help="Output PDF path")
    parser.add_argument("--company", default="Northstar Dynamics", help="Company name")
    parser.add_argument("--month", default=dt.date.today().strftime("%B %Y"), help="Reporting month")
    args = parser.parse_args()

    generate_report(args.output, args.company, args.month)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
