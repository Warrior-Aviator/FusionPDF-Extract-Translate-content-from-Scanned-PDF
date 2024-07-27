import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Specify the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Extract text using OCR
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        extracted_text += f"Page {page_num + 1}:\n{text}\n\n"
    
    return extracted_text

def create_pdf_with_text(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    text_obj = c.beginText(40, height - 40)
    
    for line in text.split('\n'):
        if text_obj.getY() < 40:
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(40, height - 40)
        text_obj.textLine(line)
    
    c.drawText(text_obj)
    c.save()

# Example usage
pdf_path = "VTU Circular.pdf"
output_path = "output_document1.pdf"

text = extract_text_from_pdf(pdf_path)
create_pdf_with_text(text, output_path)
