from app.services.document_service import DocumentService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiLLM
from app.database.conversation_repository import ConversationRepository
from app.rag.reranker import ReRanker
from app.rag.context_compressor import ContextCompressor


class RAGService:

    def __init__(self):

        self.document_service = DocumentService()
        self.prompt_builder = PromptBuilder()
        self.llm = GeminiLLM()
        self.repository = ConversationRepository()
        self.reranker = ReRanker()
        self.compressor = ContextCompressor()

    def ask(self, session_id: str, question: str):

        history = self.repository.get_history(session_id)

        retrieved_docs = self.document_service.search(question)

        # Re-rank
        retrieved_docs = self.reranker.rerank(
            question,
            retrieved_docs
        )

        # Compress Context
        retrieved_docs = self.compressor.compress(
            question,
            retrieved_docs
        )

        prompt = self.prompt_builder.build(
            question,
            retrieved_docs,
            history
        )

        answer = self.llm.generate(prompt)

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

        history = self.repository.get_history(session_id)

        retrieved_docs = self.document_service.search(question)

        # Re-rank
        retrieved_docs = self.reranker.rerank(
            question,
            retrieved_docs
        )

        # Compress Context
        retrieved_docs = self.compressor.compress(
            question,
            retrieved_docs
        )

        prompt = self.prompt_builder.build(
            question,
            retrieved_docs,
            history
        )

        full_answer = ""

        for chunk in self.llm.stream(prompt):

            full_answer += chunk
            yield chunk

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