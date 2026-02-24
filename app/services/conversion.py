from pathlib import Path
import zipfile

from pdf2image import convert_from_path
from PIL import Image


def png_to_pdf(src_path: str) -> str:
    pdf_path = src_path.rsplit(".", 1)[0] + ".pdf"
    Image.open(src_path).convert("RGB").save(pdf_path, "PDF")
    return pdf_path


def pdf_to_png_zip(src_path: str, out_dir: Path, poppler_path: str | None) -> tuple[Path, list[Path]]:
    base_name = Path(src_path).stem
    out_dir.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(src_path, poppler_path=poppler_path)
    png_paths: list[Path] = []
    for idx, page in enumerate(pages, start=1):
        png_path = out_dir / f"{base_name}_{idx}.png"
        page.save(png_path, "PNG")
        png_paths.append(png_path)

    zip_path = out_dir.parent / f"{base_name}_png.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for p in png_paths:
            zipf.write(p, arcname=p.name)

    return zip_path, png_paths
