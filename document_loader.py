from pathlib import Path

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = [".txt", ".md", ".pdf", ".docx"]


def load_documents(folder_path):

    documents = []

    folder = Path(folder_path)

    for file_path in folder.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:

            text = ""

            if file_path.suffix.lower() in [".txt", ".md"]:

                text = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            elif file_path.suffix.lower() == ".pdf":

                reader = PdfReader(str(file_path))

                pages = []

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        pages.append(page_text)

                text = "\n".join(pages)

            elif file_path.suffix.lower() == ".docx":

                doc = Document(str(file_path))

                paragraphs = []

                for paragraph in doc.paragraphs:
                    paragraphs.append(paragraph.text)

                text = "\n".join(paragraphs)

            documents.append(
                {
                    "filename": file_path.name,
                    "text": text
                }
            )

        except Exception as error:

            documents.append(
                {
                    "filename": file_path.name,
                    "text": "",
                    "error": str(error)
                }
            )

    return documents