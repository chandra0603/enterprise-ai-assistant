from app.services.document_service import DocumentService
from app.prompt.prompt_builder import PromptBuilder

service = DocumentService()

docs = service.search("What is Artificial Intelligence?")

prompt = PromptBuilder.build(
    "What is Artificial Intelligence?",
    docs
)

print(prompt)