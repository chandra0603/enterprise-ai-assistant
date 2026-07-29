import os

from langchain_community.vectorstores import FAISS

from app.rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.index_path = "vector_db"

        self.embeddings = EmbeddingModel().get_embedding()

        self.db = None

    def create(self, documents):

        self.db = FAISS.from_documents(
            documents,
            self.embeddings
        )

        self.db.save_local(self.index_path)

    def load(self):

        if not os.path.exists(self.index_path):
            return None

        self.db = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        return self.db

    def get(self):

        if self.db is None:
            self.load()

        return self.db