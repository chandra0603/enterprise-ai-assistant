from app.rag.loader import PDFLoader
from app.rag.parent_chunker import ParentChunker
from app.rag.child_chunker import ChildChunker
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.rag.keyword_search import KeywordSearch
from app.rag.hybrid_retriever import HybridRetriever
from app.rag.query_expander import QueryExpander
from app.storage.metadata_store import MetadataStore


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

        # Metadata Store
        self.metadata_store = MetadataStore()

        # Load saved metadata if available
        self.parent_documents, self.documents = self.metadata_store.load()
        self.vector_store.load()

    def upload(self, file_path: str):

        print("=" * 60)
        print("STEP 1 - upload() started")

        documents = self.loader.load(file_path)
        print("STEP 2 - PDF loaded:", len(documents))

        parents = self.parent_chunker.split(documents)
        print("STEP 3 - Parent chunks:", len(parents))

        children = []

        parent_id = 0

        for parent in parents:

            parent.metadata["parent_id"] = parent_id

            self.parent_documents[parent_id] = parent

            child_chunks = self.child_chunker.split([parent])

            print(f"Parent {parent_id}: {len(child_chunks)} child chunks")

            for child in child_chunks:

                child.metadata["parent_id"] = parent_id
                children.append(child)

            parent_id += 1

        print("STEP 4 - Total child chunks:", len(children))

        print("STEP 5 - Creating FAISS")
        self.vector_store.create(children)
        print("STEP 6 - FAISS created")

        self.documents = children

        print("STEP 7 - Saving metadata")
        self.metadata_store.save(
            self.parent_documents,
            self.documents
        )

        print("STEP 8 - Metadata saved")
        print("=" * 60)

        return {
            "message": "Document uploaded successfully",
            "parent_chunks": len(parents),
            "child_chunks": len(children)
        }

    def search(self, question: str, k=None):

        if k is None:
            k = 3

        # Expand query
        queries = self.query_expander.expand(question)

        semantic_results = []
        keyword_results = []

        # Retrieve using all expanded queries
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

        # Hybrid Search
        hybrid = self.hybrid_retriever.merge(
            semantic_results,
            keyword_results,
            top_k=k
        )

        # Convert child chunks back to parent chunks
        parent_results = []
        added = set()

        for doc, score in hybrid:

            parent_id = doc.metadata.get("parent_id")

            if parent_id is None:
                continue

            if parent_id not in added:

                parent = self.parent_documents.get(parent_id)

                if parent is not None:
                    parent_results.append((parent, score))
                    added.add(parent_id)

        return parent_results