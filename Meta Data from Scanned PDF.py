import fitz

# Define the path to the scanned PDF
pdf_path = "demo.pdf"

# Function to extract metadata from PDF
def extract_metadata(pdf_path):
    # Open the PDF
    document = fitz.open(pdf_path)
    
    # Get metadata
    metadata = document.metadata
    
    # Print metadata
    for key, value in metadata.items():
        print(f"{key}: {value}")

# Extract and display metadata
extract_metadata(pdf_path)
