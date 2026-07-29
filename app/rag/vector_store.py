from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.embedding = EmbeddingModel().get_embedding()

        self.index_path = Path("data/faiss")

        self.index_path.mkdir(parents=True, exist_ok=True)

    def create(self, chunks):

        db = FAISS.from_documents(
            documents=chunks,
            embedding=self.embedding
        )

        db.save_local(str(self.index_path))

        return db

    def load(self):

        return FAISS.load_local(
            str(self.index_path),
            self.embedding,
            allow_dangerous_deserialization=True
        )