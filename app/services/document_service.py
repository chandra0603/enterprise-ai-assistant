from app.rag.loader import PDFLoader
from app.rag.chunker import DocumentChunker
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.keyword_search import KeywordSearch
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.query_expander import QueryExpander


class DocumentService:

    def __init__(self):

        self.loader = PDFLoader()
        self.chunker = DocumentChunker()
        self.vector_store = VectorStore()
        self.retriever = Retriever()
        self.keyword_search = KeywordSearch()
        self.hybrid_retriever = HybridRetriever()
        self.query_expander = QueryExpander()

        # Store uploaded chunks for keyword search
        self.documents = []

    def upload(self, file_path: str):

        # Load PDF
        documents = self.loader.load(file_path)

        # Split into chunks
        chunks = self.chunker.split(documents)

        # Create FAISS Index
        self.vector_store.create(chunks)

        # Store chunks for keyword search
        self.documents.extend(chunks)

        return {
            "message": "Document uploaded successfully",
            "chunks": len(chunks)
        }

    def search(self, question: str, k=None):

        if k is None:
            k = 3

        # Generate multiple search queries
        queries = self.query_expander.expand(question)

        semantic_results = []
        keyword_results = []

        # Search using every generated query
        for query in queries:

            semantic_results.extend(
                self.retriever.search(query, k)
            )

            keyword_results.extend(
                self.keyword_search.search(
                    query,
                    self.documents
                )
            )

        # Merge Semantic + Keyword results
        hybrid_results = self.hybrid_retriever.merge(
            semantic_results,
            keyword_results,
            top_k=k
        )

        return hybrid_results