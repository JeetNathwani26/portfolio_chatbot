"""One-time utility: extract a text-based resume PDF into resume.txt."""

from pathlib import Path

from pypdf import PdfReader


source = Path("resume.pdf")
destination = Path("resume.txt")
text = "\n".join(page.extract_text() or "" for page in PdfReader(source).pages).strip()

if not text:
    raise RuntimeError("The PDF has no extractable text. Use a text-based PDF.")

destination.write_text(text + "\n", encoding="utf-8")
print(f"Created {destination} from {source}.")
