from fastapi import APIRouter

from app.schemas.chat import SearchRequest
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

service = DocumentService()
service = RAGService()


@router.post("/search")
def search(request: SearchRequest):

    docs = service.search(request.question)

    return {
        "results": [
            {
                "page": doc.metadata.get("page"),
                "content": doc.page_content
            }
            for doc in docs
        ]
    }
    
@router.post("/ask")
def ask(request: SearchRequest):

    return service.ask(request.question)