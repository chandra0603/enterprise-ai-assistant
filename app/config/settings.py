from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

        GEMINI_MODEL = os.getenv("GEMINI_MODEL")
        
        TOP_K = int(os.getenv("TOP_K", 3))

settings = Settings()