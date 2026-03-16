from __future__ import annotations

import argparse
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOGO = "https://www.mobigator.com/pub/images/header/logo.png"
DEFAULT_OUTPUT = ROOT / "ai-intern-event.pdf"
DEFAULT_URL = "https://mtgthomasleung-svg.github.io/mtg-openings-site/#/jobs/ai-intern"
DEFAULT_TITLE = "AI Intern"
DEFAULT_SUMMARY = (
    "Explore the latest AI tools and technologies while contributing to real business applications."
    "\n\nStudents in all related fields are welcome to apply."
)


@dataclass(frozen=True)
class PosterContent:
    logo_source: str
    title: str
    summary: str
    url: str
    output_path: Path


def parse_args() -> PosterContent:
    parser = argparse.ArgumentParser(
        description="Generate an A4 event PDF with logo, job title, summary, and a QR code."
    )
    parser.add_argument(
        "--logo",
        default=DEFAULT_LOGO,
        help="Path or URL to the logo image.",
    )
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Job title to display.")
    parser.add_argument("--summary", default=DEFAULT_SUMMARY, help="Short job summary.")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL encoded in the QR code.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output PDF path.",
    )
    args = parser.parse_args()
    return PosterContent(
        logo_source=args.logo.strip(),
        title=args.title.strip(),
        summary=args.summary.strip(),
        url=args.url.strip(),
        output_path=args.output,
    )


def make_qr_image(url: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=16,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def pil_to_reader(image: Image.Image) -> ImageReader:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ImageReader(buffer)


def fit_title_font(pdf: canvas.Canvas, title: str, max_width: float) -> int:
    for size in range(30, 17, -1):
        if pdf.stringWidth(title, "Helvetica-Bold", size) <= max_width:
            return size
    return 17


def load_image(source: str) -> Image.Image:
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https"}:
        with urlopen(source) as response:
            return Image.open(BytesIO(response.read())).convert("RGBA")
    return Image.open(Path(source)).convert("RGBA")


def draw_logo(pdf: canvas.Canvas, logo_source: str, page_width: float, top_y: float) -> float:
    with load_image(logo_source) as logo:
        logo_ratio = logo.height / logo.width
        logo_width = min(page_width * 0.42, 240)
        logo_height = logo_width * logo_ratio
        x = (page_width - logo_width) / 2
        y = top_y - logo_height
        pdf.drawImage(
            pil_to_reader(logo),
            x,
            y,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )
    return y


def draw_centered_lines(
    pdf: canvas.Canvas,
    lines: list[str],
    start_y: float,
    font_name: str,
    font_size: int,
    color: tuple[float, float, float],
    leading: float,
) -> float:
    pdf.setFont(font_name, font_size)
    pdf.setFillColorRGB(*color)
    y = start_y
    for line in lines:
        pdf.drawCentredString(A4[0] / 2, y, line)
        y -= leading
    return y


def generate_pdf(content: PosterContent) -> Path:
    output_path = content.output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = A4
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    pdf.setTitle(f"{content.title} Event Poster")

    margin_x = 40
    top_bar_height = 50
    pdf.setFillColorRGB(0.54, 0.0, 0.0)
    pdf.rect(0, page_height - top_bar_height, page_width, top_bar_height, stroke=0, fill=1)

    top_y = page_height - top_bar_height - 36
    bottom_margin = 34

    title_max_width = page_width - (2 * margin_x)
    title_font = fit_title_font(pdf, content.title, title_max_width)

    after_logo_y = draw_logo(pdf, content.logo_source, page_width, top_y) - 56

    pdf.setFillColorRGB(0.27, 0.32, 0.38)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(page_width / 2, after_logo_y, "We are hiring:")

    pdf.setFillColorRGB(0.07, 0.10, 0.15)
    pdf.setFont("Helvetica-Bold", title_font)
    pdf.drawCentredString(page_width / 2, after_logo_y - 36, content.title)

    summary_font = 18
    summary_line_leading = 18
    summary_para_spacing = 16
    summary_width = page_width - (2 * margin_x)

    paragraphs = content.summary.split("\n\n")
    y = after_logo_y - 70
    pdf.setFont("Helvetica", summary_font)
    pdf.setFillColorRGB(0.27, 0.32, 0.38)

    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para:
            continue
        lines = simpleSplit(para, "Helvetica", summary_font, summary_width)
        for line in lines:
            pdf.drawCentredString(page_width / 2, y, line)
            y -= summary_line_leading
        if i < len(paragraphs) - 1:
            y -= summary_para_spacing

    after_summary_y = y

    qr_image = make_qr_image(content.url)
    caption_space = 58
    qr_size = min(page_width - 220, page_height * 0.32, after_summary_y - (bottom_margin + caption_space + 40))
    qr_x = (page_width - qr_size) / 2
    qr_block_bottom = bottom_margin + 150
    qr_y = qr_block_bottom

    if qr_size < 180:
        raise ValueError("Not enough vertical space for the current title/summary layout.")

    pdf.drawImage(
        pil_to_reader(qr_image),
        qr_x,
        qr_y,
        width=qr_size,
        height=qr_size,
        preserveAspectRatio=True,
        mask="auto",
    )

    pdf.setFillColorRGB(0.12, 0.15, 0.19)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(page_width / 2, qr_y - 16, "Scan to view the full job details")

    bottom_bar_height = 30
    pdf.setFillColorRGB(0.54, 0.0, 0.0)
    pdf.rect(0, 0, page_width, bottom_bar_height, stroke=0, fill=1)

    pdf.showPage()
    pdf.save()
    return output_path


def main() -> None:
    content = parse_args()
    output_path = generate_pdf(content)
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()

