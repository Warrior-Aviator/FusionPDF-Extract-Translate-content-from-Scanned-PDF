import ocrmypdf

def convert_to_searchable_pdf(input_pdf_path, output_pdf_path):
    try:
        ocrmypdf.ocr(input_pdf_path, output_pdf_path, deskew=True)
        print(f"Successfully converted {input_pdf_path} to searchable PDF at {output_pdf_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_pdf_path = "VTU New.pdf"
output_pdf_path = "Searchable_PDF_2.pdf"

convert_to_searchable_pdf(input_pdf_path, output_pdf_path)
