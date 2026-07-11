import os
import fitz  # PyMuPDF

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF and return its path.
    """
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def extract_text_from_pdf(file_path):
    """
    Extract text page by page.
    Returns a list of dictionaries:
    [
        {"page": 1, "text": "..."},
        {"page": 2, "text": "..."},
        ...
    ]
    """

    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        page_text = page.get_text()

        pages.append({
            "page": page_number,
            "text": page_text
        })

    document.close()

    return pages