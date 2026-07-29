from app.config.settings import settings
from app.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.vector_store = VectorStore()

    def search(self, question, k=None):

        if k is None:
            k = settings.TOP_K

        vector_db = self.vector_store.load()

        return vector_db.similarity_search_with_score(
            question,
            k=k
        )