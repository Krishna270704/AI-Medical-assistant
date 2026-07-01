import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def extract_text_from_file(file_path):
    """
    Detects file type and extracts text using PyMuPDF (native PDFs) or Tesseract (images/scanned PDFs).
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.pdf':
            return _extract_from_pdf(file_path)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return _extract_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        logger.error(f"Failed to extract text from {file_path}: {str(e)}")
        raise

def _extract_from_image(file_path):
    logger.info(f"Running OCR on image: {file_path}")
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

def _extract_from_pdf(file_path):
    logger.info(f"Extracting text from PDF: {file_path}")
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text()
            text += page_text + "\n"
            
    # If the PDF is scanned, the extracted text will be very short or empty.
    # Fallback to OCR if less than 50 characters were found natively.
    if len(text.strip()) < 50:
        logger.info(f"Native PDF extraction yielded little text. Falling back to OCR for {file_path}")
        text = _ocr_pdf(file_path)
        
    return text.strip()

def _ocr_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for i in range(len(doc)):
            page = doc[i]
            # Render page to an image
            pix = page.get_pixmap(dpi=150)
            img_data = pix.tobytes("png")
            
            # Temporary file approach could be used, or passing directly to PIL
            import io
            image = Image.open(io.BytesIO(img_data))
            text += pytesseract.image_to_string(image) + "\n"
    return text
