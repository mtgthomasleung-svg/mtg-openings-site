from __future__ import annotations

import argparse
from pathlib import Path

import fitz


DEFAULT_DPI = 300


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PDF into one or more high-resolution PNG files."
    )
    parser.add_argument("pdf", type=Path, help="Path to the source PDF.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to write PNG files to. Defaults to the PDF's folder.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"Render resolution in DPI. Default: {DEFAULT_DPI}.",
    )
    return parser.parse_args()


def build_output_path(output_dir: Path, pdf_path: Path, page_count: int, page_index: int) -> Path:
    if page_count == 1:
        return output_dir / f"{pdf_path.stem}.png"
    return output_dir / f"{pdf_path.stem}-page-{page_index + 1:02d}.png"


def convert_pdf_to_png(pdf_path: Path, output_dir: Path, dpi: int) -> list[Path]:
    if dpi <= 0:
        raise ValueError("DPI must be a positive integer.")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    scale = dpi / 72
    created_files: list[Path] = []

    with fitz.open(pdf_path) as document:
        if document.page_count == 0:
            raise ValueError("The PDF has no pages.")

        for page_index, page in enumerate(document):
            # PDF coordinates are based on 72 DPI, so scaling raises output resolution.
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            output_path = build_output_path(output_dir, pdf_path, document.page_count, page_index)
            pixmap.save(output_path)
            created_files.append(output_path)

    return created_files


def main() -> None:
    args = parse_args()
    pdf_path = args.pdf.resolve()
    output_dir = (args.output_dir or pdf_path.parent).resolve()

    created_files = convert_pdf_to_png(pdf_path, output_dir, args.dpi)
    for created_file in created_files:
        print(f"Created {created_file}")


if __name__ == "__main__":
    main()
