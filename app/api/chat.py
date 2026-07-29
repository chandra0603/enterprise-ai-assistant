from fastapi import APIRouter

from app.schemas.chat import SearchRequest
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

document_service = DocumentService()
rag_service = RAGService()


@router.post("/search")
def search(request: SearchRequest):

    docs = document_service.search(request.question)

    return {
        "results": [
            {
                "page": doc.metadata.get("page"),
                "score": float(score),
                "content": doc.page_content
            }
            for doc, score in docs
        ]
    }


@router.post("/ask")
def ask(request: SearchRequest):

    return rag_service.ask(
        session_id=request.session_id,
        question=request.question
    )
    
@router.post("/stream")
def stream(request: SearchRequest):

    return StreamingResponse(
        rag_service.stream(
            session_id=request.session_id,
            question=request.question
        ),
        media_type="text/plain"
    )