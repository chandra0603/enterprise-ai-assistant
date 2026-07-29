from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:

    def load(self, pdf_path: str):

        """
        Load a PDF and return LangChain Document objects.
        """

        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        loader = PyPDFLoader(str(pdf_file))

        documents = loader.load()

        print(f"Loaded {len(documents)} pages from {pdf_file.name}")

        return documents