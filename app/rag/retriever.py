from app.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.vector_store = VectorStore()

    def search(self, question, k=3):

        db = self.vector_store.get()

        if db is None:
            return []

        return db.similarity_search_with_score(
            question,
            k=k
        )