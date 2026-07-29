from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

service = DocumentService()

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Document uploaded successfully.",
        "filename": file.filename,
        "path": str(file_path)
    }


@router.get("/")
def list_documents():

    files = [
        file.name
        for file in UPLOAD_DIR.iterdir()
        if file.is_file()
    ]

    return {
        "documents": files
    }


@router.get("/{filename}")
def read_document(filename: str):

    documents = service.load_document(filename)

    return {
        "pages": len(documents),
        "preview": documents[0].page_content[:500]
    }


@router.get("/{filename}/chunks")
def get_chunks(filename: str):

    chunks = service.chunk_document(filename)

    return {
        "total_chunks": len(chunks),
        "first_chunk": chunks[0].page_content,
        "metadata": chunks[0].metadata
    }


@router.post("/{filename}/embeddings")
def create_embeddings(filename: str):

    total = service.create_embeddings(filename)

    return {
        "message": "Embeddings created successfully.",
        "chunks": total
    }