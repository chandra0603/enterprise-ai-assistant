from app.config.settings import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class EmbeddingModel:

    def __init__(self):
        self.embedding = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
        )

    def get_embedding(self):
        return self.embedding