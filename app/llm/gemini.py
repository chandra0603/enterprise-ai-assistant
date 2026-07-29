from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


class GeminiLLM:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

    def generate(self, prompt: str) -> str:

        response = self.llm.invoke(prompt)

        # New versions return a list of content blocks
        if isinstance(response.content, list):
            text = ""

            for part in response.content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text += part.get("text", "")

            return text

        return response.content