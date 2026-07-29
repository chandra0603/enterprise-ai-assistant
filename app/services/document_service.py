from app.rag.loader import PDFLoader
from app.rag.parent_chunker import ParentChunker
from app.rag.child_chunker import ChildChunker
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.keyword_search import KeywordSearch
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.query_expander import QueryExpander


class DocumentService:

    def __init__(self):

        self.loader = PDFLoader()

        self.parent_chunker = ParentChunker()
        self.child_chunker = ChildChunker()

        self.vector_store = VectorStore()
        self.retriever = Retriever()

        self.keyword_search = KeywordSearch()
        self.hybrid_retriever = HybridRetriever()
        self.query_expander = QueryExpander()

        # Parent Documents
        self.parent_documents = {}

        # Child Documents
        self.documents = []

    def upload(self, file_path: str):

        documents = self.loader.load(file_path)

        parents = self.parent_chunker.split(documents)

        children = []

        parent_id = 0

        for parent in parents:

            parent.metadata["parent_id"] = parent_id

            self.parent_documents[parent_id] = parent

            child_chunks = self.child_chunker.split([parent])

            for child in child_chunks:

                child.metadata["parent_id"] = parent_id

                children.append(child)

            parent_id += 1

        self.vector_store.create(children)

        self.documents = children

        return {
            "message": "Document uploaded successfully",
            "parent_chunks": len(parents),
            "child_chunks": len(children)
        }

    def search(self, question: str, k=None):

        if k is None:
            k = 3

        queries = self.query_expander.expand(question)

        semantic_results = []
        keyword_results = []

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

        hybrid = self.hybrid_retriever.merge(
            semantic_results,
            keyword_results,
            top_k=k
        )

        parent_results = []

        added = set()

        for doc, score in hybrid:

            parent_id = doc.metadata["parent_id"]

            if parent_id not in added:

                added.add(parent_id)

                parent_results.append(
                    (
                        self.parent_documents[parent_id],
                        score
                    )
                )

        return parent_results