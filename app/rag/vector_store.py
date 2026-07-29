import os

from langchain_community.vectorstores import FAISS

from app.rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.index_path = "vector_db"

        self.embeddings = EmbeddingModel().get_embedding()

        self.db = None

    def create(self, documents):

        if os.path.exists(self.index_path):

            print("Existing FAISS found.")

            self.load()

            if self.db is None:
                raise RuntimeError("Failed to load existing FAISS index.")

            print(f"Adding {len(documents)} new chunks...")

            self.db.add_documents(documents)

        else:

            print("Creating new FAISS index...")

            self.db = FAISS.from_documents(
                documents,
                self.embeddings
            )

        self.db.save_local(self.index_path)

        print("FAISS saved successfully.")

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
    
    def rebuild(self, documents):

        print("Rebuilding FAISS index...")

        self.db = FAISS.from_documents(
            documents,
            self.embeddings
        )

        self.db.save_local(self.index_path)

        print("FAISS rebuilt successfully.")