import pytesseract
from PIL import Image
import io
from pypdf import PdfReader

def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text.strip()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text and page_text.strip():
            text += page_text + "\n"
        else:
            # Note: For scanned PDFs on ARM64 without native rendering, 
            # this would typically need pdf2image + poppler or a native library.
            # We'll skip OCR-per-page for now to ensure the service INSTALLS.
            pass
            
    return text.strip()

def normalize_text(text: str) -> str:
    if not text:
        return ""
    lines = text.splitlines()
    normalized_lines = [" ".join(line.split()) for line in lines if line.strip()]
    return "\n".join(normalized_lines)
