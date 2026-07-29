from pathlib import Path

from app.rag.loader import PDFLoader
from app.rag.chunker import DocumentChunker
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever


class DocumentService:

    def __init__(self):
        self.loader = PDFLoader()
        self.chunker = DocumentChunker()
        self.vector_store = VectorStore()
        self.retriever = Retriever()
        
    def load_document(self, filename: str):

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        path = Path("data/documents") / filename

        return self.loader.load(str(path))

    def chunk_document(self, filename: str):

        documents = self.load_document(filename)

        chunks = self.chunker.split(documents)

        return chunks
    
    def create_embeddings(self, filename: str):

        chunks = self.chunk_document(filename)

        self.vector_store.create(chunks)

        return len(chunks)
    
    def search(self, question: str, k=None):

        return self.retriever.search(question, k)
    