import streamlit as st
from zipfile import ZipFile
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import base64
#------- OCR ------------
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError

@st.cache_data
def images_to_txt(file_bytes, language):
    images = pdf2image.convert_from_bytes(file_bytes)
    all_text = []
    for i in images:
        pil_im = i
        text = pytesseract.image_to_string(pil_im, lang=language)
        all_text.append(text)
    return all_text, len(all_text)

@st.cache_data
def convert_pdf_to_txt_pages(file_bytes):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    size = 0
    c = 0
    file_pages = PDFPage.get_pages(io.BytesIO(file_bytes))
    nbPages = len(list(file_pages))
    for page in PDFPage.get_pages(io.BytesIO(file_bytes)):
        interpreter.process_page(page)
        t = retstr.getvalue()
        if c == 0:
            texts.append(t)
        else:
            texts.append(t[size:])
        c = c + 1
        size = len(t)
    device.close()
    retstr.close()
    return texts, nbPages

@st.cache_data
def convert_pdf_to_txt_file(file_bytes):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    file_pages = PDFPage.get_pages(io.BytesIO(file_bytes))
    nbPages = len(list(file_pages))
    for page in PDFPage.get_pages(io.BytesIO(file_bytes)):
        interpreter.process_page(page)
    t = retstr.getvalue()
    device.close()
    retstr.close()
    return t, nbPages

@st.cache_data
def save_pages(pages):
    files = []
    for page in range(len(pages)):
        filename = "page_" + str(page) + ".txt"
        with open("./file_pages/" + filename, 'w', encoding="utf-8") as file:
            file.write(pages[page])
            files.append(file.name)
    zipPath = './file_pages/pdf_to_txt.zip'
    zipObj = ZipFile(zipPath, 'w')
    for f in files:
        zipObj.write(f)
    zipObj.close()
    return zipPath

def displayPDF(file):
    base64_pdf = base64.b64encode(file).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit interface
st.title("PDF Text Extractor")

uploaded_file = st.file_uploader("Choose a scanned PDF file", type=["pdf"])

if uploaded_file is not None:
    language = st.selectbox("Choose the OCR language", ["eng", "kan", "deu", "fra", "spa", "ita"])
    
    text_option = st.selectbox("Choose the extraction method", ["Extract text from images (OCR)", "Extract text from PDF"])

    if st.button("Extract Text"):
        if text_option == "Extract text from images (OCR)":
            texts, nbPages = images_to_txt(uploaded_file.read(), language)
            st.write(f"Extracted text from {nbPages} pages.")
            for text in texts:
                st.write(text)
        else:
            texts, nbPages = convert_pdf_to_txt_pages(uploaded_file.read())
            st.write(f"Extracted text from {nbPages} pages.")
            for text in texts:
                st.write(text)

    if st.button("Convert PDF to text file"):
        text, nbPages = convert_pdf_to_txt_file(uploaded_file.read())
        st.write(f"Extracted text from {nbPages} pages.")
        st.download_button(label="Download text file", data=text, file_name="extracted_text.txt")

    if st.button("Save pages as text files and create zip"):
        texts, nbPages = convert_pdf_to_txt_pages(uploaded_file.read())
        zip_path = save_pages(texts)
        with open(zip_path, 'rb') as f:
            st.download_button(label="Download zip file", data=f, file_name="pdf_to_txt.zip")

    if st.button("Display PDF"):
        displayPDF(uploaded_file.read())
