import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> list[str]:
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file.
        
    Returns:
        A list of strings, where each string represents the text of a single page.
    """
    documents = []
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            if text.strip():
                documents.append(text.strip())
        pdf_document.close()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        
    return documents
