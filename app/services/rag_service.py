from app.services.document_service import DocumentService
from app.prompt.prompt_builder import PromptBuilder
from app.llm.gemini import GeminiLLM
from app.database.conversation_repository import ConversationRepository


class RAGService:

    def __init__(self):
        self.document_service = DocumentService()
        self.llm = GeminiLLM()
        self.memory = ConversationRepository()

    def ask(self, session_id: str, question: str):

        # Get previous conversation
        history = self.memory.get_history(session_id)

        # Retrieve relevant documents
        retrieved_docs = self.document_service.search(question)

        # Build prompt
        prompt = PromptBuilder.build(
            question=question,
            documents=retrieved_docs,
            history=history
        )

        # Generate answer
        answer = self.llm.generate(prompt)

        # Save conversation
        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question
        )

        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )

        # Return response
        return {
            "answer": answer,
            "sources": [
                {
                    "page": doc.metadata.get("page"),
                    "score": float(score),
                    "content": doc.page_content
                }
                for doc, score in retrieved_docs
            ]
        }
        
    
    def stream(self, session_id: str, question: str):

        # Get previous conversation
        history = self.memory.get_history(session_id)

        # Retrieve relevant documents
        retrieved_docs = self.document_service.search(question)

        # Build prompt
        prompt = PromptBuilder.build(
            question=question,
            documents=retrieved_docs,
            history=history
        )

        # Collect streamed response
        answer = ""

        for chunk in self.llm.stream(prompt):
            answer += chunk
            yield chunk

        # Save conversation after streaming completes
        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question
        )

        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )