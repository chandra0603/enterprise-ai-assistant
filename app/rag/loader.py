from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:

    def load(self, pdf_path: str):
        """
        Load a PDF and return LangChain Document objects.
        """

        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"{pdf_path} not found")

        loader = PyPDFLoader(pdf_path)

        documents = loader.load()

        return documents