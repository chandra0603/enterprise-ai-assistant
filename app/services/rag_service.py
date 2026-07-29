from app.services.document_service import DocumentService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiLLM


class RAGService:

    def __init__(self):
        self.document_service = DocumentService()
        self.llm = GeminiLLM()

    def ask(self, question: str):

        # Retrieve relevant documents
        docs = self.document_service.search(question)

        # Build prompt
        prompt = PromptBuilder.build(question, docs)

        # Generate answer
        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": [
            {
                "page": doc.metadata.get("page"),
                "score": float(score),
                "content": doc.page_content
            }
            for doc, score in docs
        ]
    }