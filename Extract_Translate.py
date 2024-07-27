import io
from googletrans import Translator
import pdf2image
import pytesseract
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_text(pdf_path):
    images = pdf2image.convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='kan')
    return text

def translate_text(text, src='kn', dest='en'):
    translator = Translator()
    translated = translator.translate(text, src=src, dest=dest)
    return translated.text

def text_to_pdf(text, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    lines = text.split('\n')
    y = height - 40  # start from top of the page
    for line in lines:
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line)
        y -= 15
    c.save()

def main(pdf_path, output_pdf_path):
    # Extract text from PDF
    kannada_text = pdf_to_text(pdf_path)
    
    # Translate text
    translated_text = translate_text(kannada_text)
    
    # Create a new PDF with the translated text
    text_to_pdf(translated_text, output_pdf_path)
    
    print("Translation completed and saved to:", output_pdf_path)

# Provide the path to your scanned PDF and the output PDF file
pdf_path = 'VTU Translate.pdf'
output_pdf_path = 'Translated.pdf'

main(pdf_path, output_pdf_path)
