from app.repositories.conversation_repository import ConversationRepository
from app.services.document_service import DocumentService
from app.services.llm_service import LLMService
from app.rag.prompt_builder import PromptBuilder


class ChatService:

    def __init__(self):

        self.document_service = DocumentService()
        self.llm_service = LLMService()
        self.repository = ConversationRepository()

    def chat(self, session_id: str, question: str):

        # Load previous conversation
        history = self.repository.get_messages(session_id)

        # Retrieve relevant documents
        documents = self.document_service.search(question)

        # Build prompt
        prompt = PromptBuilder.build(
            question=question,
            documents=documents,
            history=history
        )

        # Generate answer
        answer = self.llm_service.generate(prompt)

        # Save conversation
        self.repository.save_message(
            session_id=session_id,
            role="user",
            content=question
        )

        self.repository.save_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )

        return {
            "answer": answer
        }