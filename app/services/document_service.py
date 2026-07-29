from app.rag.loader import PDFLoader
from app.rag.chunker import DocumentChunker
from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.keyword_search import KeywordSearch
from app.rag.hybrid_retriever import HybridRetriever


class DocumentService:

    def __init__(self):

        self.loader = PDFLoader()
        self.chunker = DocumentChunker()
        self.embedding = EmbeddingModel()
        self.vector_store = VectorStore()
        self.retriever = Retriever()
        self.keyword_search = KeywordSearch()
        self.hybrid_retriever = HybridRetriever()

        self.documents = []

    def upload(self, file_path: str):

        # Load PDF
        documents = self.loader.load(file_path)

        # Split into chunks
        chunks = self.chunker.split(documents)

        # Create FAISS index
        self.vector_store.create(chunks)

        # Keep chunks in memory for keyword search
        self.documents.extend(chunks)

        return {
            "message": "Document uploaded successfully",
            "chunks": len(chunks)
        }

    def search(self, question: str, k=None):

        semantic_results = self.retriever.search(question, k)

        keyword_results = self.keyword_search.search(
            question,
            self.documents
        )

        return self.hybrid_retriever.merge(
            semantic_results,
            keyword_results,
            top_k=k if k else 3
        )