import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import numpy as np

# Ensure that Tesseract OCR is installed and added to PATH
# Example path: 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding
    _, binary_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary_img

def extract_text_from_image(image):
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    # Convert PDF to a list of images
    pages = convert_from_path(pdf_path)
    
    full_text = ""
    for page_number, page in enumerate(pages):
        # Preprocess the image (optional)
        # page = preprocess_image(np.array(page))
        
        # Extract text from the image
        text = extract_text_from_image(page)
        full_text += f"Page {page_number + 1}:\n{text}\n\n"
    
    return full_text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    input_pdf_path = 'VTU Demo 2.pdf'
    output_text_file = 'extracted_text.txt'
    
    # Extract text from the scanned PDF
    extracted_text = extract_text_from_pdf(input_pdf_path)
    
    # Save the extracted text to a file
    save_text_to_file(extracted_text, output_text_file)
    
    print(f"Text extracted and saved to {output_text_file}")

if __name__ == '__main__':
    main()
