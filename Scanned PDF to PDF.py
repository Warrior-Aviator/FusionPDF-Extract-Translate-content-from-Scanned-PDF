import subprocess
import os

def convert_scanned_pdf_to_searchable(input_pdf_path, output_pdf_path):
    try:
        # Run ocrmypdf to convert scanned PDF to searchable PDF
        subprocess.run(['ocrmypdf', '--force-ocr', input_pdf_path, output_pdf_path], check=True)
        print(f"Searchable PDF created successfully: {output_pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating searchable PDF: {e}")

def main():
    input_pdf_path = 'VTU Demo 2.pdf'
    output_pdf_path = 'searchable_document.pdf'
    
    # Convert the scanned PDF to a searchable PDF
    convert_scanned_pdf_to_searchable(input_pdf_path, output_pdf_path)

if __name__ == '__main__':
    main()
