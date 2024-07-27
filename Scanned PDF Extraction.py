from google.cloud import vision
import io

def extract_text_with_vision(input_pdf_path, output_text_path):
    # Initialize Vision API client
    client = vision.ImageAnnotatorClient()

    # Read the document content
    with io.open(input_pdf_path, 'rb') as document:
        content = document.read()
    
    # Construct the request
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    
    # Extract text
    text = response.full_text_annotation.text

    # Save extracted text to a file
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Text extracted and saved to {output_text_path}")

def main():
    input_pdf_path = 'Demo_File.pdf'
    output_text_path = 'extracted_text.txt'
    
    extract_text_with_vision(input_pdf_path, output_text_path)

if __name__ == '__main__':
    main()
                   
