import PyPDF2

def extract_text_from_pdf(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip() if text else "No readable text found."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
