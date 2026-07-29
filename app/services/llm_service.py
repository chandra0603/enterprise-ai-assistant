from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


class LLMService:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    def generate(self, prompt: str) -> str:

        response = self.llm.invoke(prompt)

        return response.content