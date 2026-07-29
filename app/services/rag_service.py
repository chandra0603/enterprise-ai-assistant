from app.services.document_service import DocumentService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiLLM
from app.database.conversation_repository import ConversationRepository
from app.rag.reranker import ReRanker


class RAGService:

    def __init__(self):

        self.document_service = DocumentService()
        self.prompt_builder = PromptBuilder()
        self.llm = GeminiLLM()
        self.repository = ConversationRepository()
        self.reranker = ReRanker()

    def ask(self, session_id: str, question: str):

        # Get conversation history
        history = self.repository.get_history(session_id)

        # Retrieve documents
        retrieved_docs = self.document_service.search(question)

        # Re-rank documents
        retrieved_docs = self.reranker.rerank(
            question,
            retrieved_docs
        )

        # Build prompt
        prompt = self.prompt_builder.build(
            question,
            retrieved_docs,
            history
        )

        # Generate answer
        answer = self.llm.generate(prompt)

        # Save conversation
        self.repository.add_message(
            session_id,
            "user",
            question
        )

        self.repository.add_message(
            session_id,
            "assistant",
            answer
        )

        # Return response
        return {
            "answer": answer,
            "sources": [
                {
                    "page": doc.metadata.get("page"),
                    "score": float(score)
                }
                for doc, score in retrieved_docs
            ]
        }

    def stream(self, session_id: str, question: str):

        # Get conversation history
        history = self.repository.get_history(session_id)

        # Retrieve documents
        retrieved_docs = self.document_service.search(question)

        # Re-rank documents
        retrieved_docs = self.reranker.rerank(
            question,
            retrieved_docs
        )

        # Build prompt
        prompt = self.prompt_builder.build(
            question,
            retrieved_docs,
            history
        )

        full_answer = ""

        # Stream response
        for chunk in self.llm.stream(prompt):

            full_answer += chunk

            yield chunk

        # Save conversation
        self.repository.add_message(
            session_id,
            "user",
            question
        )

        self.repository.add_message(
            session_id,
            "assistant",
            full_answer
        )