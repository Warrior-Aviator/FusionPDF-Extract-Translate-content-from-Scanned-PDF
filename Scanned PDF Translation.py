import os
import pdfplumber
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Ensure the path to your font file is correct
noto_sans_kannada_path = "NotoSansKannada-VariableFont_wdth,wght.ttf"

# Check if the font file exists
if not os.path.isfile(noto_sans_kannada_path):
    raise FileNotFoundError(f"The font file was not found: {noto_sans_kannada_path}")

# Define paths
input_pdf_path = "searchable_document.pdf"
output_pdf_path = "translated_document.pdf"

# Register the font
pdfmetrics.registerFont(TTFont('NotoSansKannada', noto_sans_kannada_path))

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def translate_text(text, src_lang='kn', dest_lang='en'):
    translator = Translator()
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

def create_translated_pdf(translated_text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 40)
    text_object.setFont("NotoSansKannada", 12)

    for line in translated_text.split('\n'):
        text_object.textLine(line)
    
    c.drawText(text_object)
    c.showPage()
    c.save()

# Extract text from PDF
text = extract_text_from_pdf(input_pdf_path)

# Translate text from Kannada to English
translated_text = translate_text(text)

# Create a new PDF with the translated text
create_translated_pdf(translated_text, output_pdf_path)

print(f"Translation completed. Translated PDF saved to {output_pdf_path}.")
