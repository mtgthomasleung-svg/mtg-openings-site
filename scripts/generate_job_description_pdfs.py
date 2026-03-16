from __future__ import annotations

import json
import re
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import urlopen

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "src" / "data.ts"


def extract_ts_literal(source: str, export_name: str) -> str:
    marker = f"export const {export_name} ="
    start = source.find(marker)
    if start == -1:
        raise ValueError(f"Could not find export {export_name!r} in {DATA_PATH}")

    index = start + len(marker)
    while index < len(source) and source[index].isspace():
        index += 1

    opening = source[index]
    closing = "}" if opening == "{" else "]" if opening == "[" else ""
    if not closing:
        raise ValueError(f"Unsupported literal for export {export_name!r}")

    depth = 0
    in_string = False
    escape = False

    for pos in range(index, len(source)):
        char = source[pos]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return source[index : pos + 1]

    raise ValueError(f"Could not parse export {export_name!r}")


def ts_literal_to_python(literal: str) -> Any:
    normalized = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', literal)
    normalized = re.sub(r",(\s*[}\]])", r"\1", normalized)
    return json.loads(normalized)


def load_content() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source = DATA_PATH.read_text(encoding="utf-8")
    company_info = ts_literal_to_python(extract_ts_literal(source, "companyInfo"))
    jobs = ts_literal_to_python(extract_ts_literal(source, "jobs"))
    return company_info, jobs


def slug_to_filename(slug: str) -> str:
    return f"{slug}-full-job-description.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "company": ParagraphStyle(
            "Company",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=HexColor("#8A0000"),
            spaceAfter=6,
        ),
        "title": ParagraphStyle(
            "JobTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=HexColor("#111827"),
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=HexColor("#4B5563"),
            spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=HexColor("#8A0000"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=HexColor("#1F2937"),
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            leftIndent=0,
            textColor=HexColor("#1F2937"),
        ),
    }


def build_bullet_list(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(item, style)) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontName="Helvetica",
        bulletFontSize=10,
        spaceBefore=2,
        spaceAfter=6,
    )


def build_logo(logo_source: str) -> Image:
    parsed = urlparse(logo_source)
    if parsed.scheme in {"http", "https"}:
        with urlopen(logo_source) as response:
            logo_data = BytesIO(response.read())
        logo = Image(logo_data)
    else:
        logo = Image(str(Path(logo_source)))

    max_width = 60 * mm
    max_height = 18 * mm
    width_scale = max_width / logo.imageWidth
    height_scale = max_height / logo.imageHeight
    scale = min(width_scale, height_scale, 1)
    logo.drawWidth = logo.imageWidth * scale
    logo.drawHeight = logo.imageHeight * scale
    logo.hAlign = "CENTER"
    return logo


def generate_job_pdf(company_info: dict[str, Any], job: dict[str, Any], styles: dict[str, ParagraphStyle]) -> Path:
    output_path = ROOT / slug_to_filename(job["id"])
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        title=f'{job["title"]} - Full Job Description',
        author=company_info["name"],
    )

    story = [
        build_logo(company_info["logo"]),
        Spacer(1, 6),
        Paragraph(job["title"], styles["title"]),
        Paragraph(" | ".join(job["types"]), styles["meta"]),
        Spacer(1, 6),
        # Paragraph("Role Summary", styles["section"]),
        # Paragraph(
        #     f'This opening is for a <b>{job["title"]}</b> role within {company_info["name"]}. '
        #     "The full responsibilities, requirements, and offer details are listed below.",
        #     styles["body"],
        # ),
        Paragraph("Key Responsibilities", styles["section"]),
        build_bullet_list(job["responsibilities"], styles["bullet"]),
        Paragraph("Requirements", styles["section"]),
        build_bullet_list(job["requirements"], styles["bullet"]),
        Paragraph("What We Offer", styles["section"]),
        build_bullet_list(job["offer"], styles["bullet"]),
        # Paragraph("Additional Information", styles["section"]),
        # Paragraph(company_info["offer"], styles["body"]),
        # Paragraph("Benefits", styles["section"]),
        # Paragraph(company_info["benefits"], styles["body"]),
        Paragraph("How to Apply", styles["section"]),
        Paragraph(
            f'Send your application to <b>{job["applyEmail"]}</b> and mention the role title '
            f'<b>{job["title"]}</b>.',
            styles["body"],
        ),
    ]

    doc.build(story)
    return output_path


def main() -> None:
    company_info, jobs = load_content()
    styles = build_styles()
    created_files = [generate_job_pdf(company_info, job, styles) for job in jobs]
    for created_file in created_files:
        print(f"Created {created_file}")


if __name__ == "__main__":
    main()
