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

    # Process document
    result = service.upload(str(file_path))

    return {
        "message": result["message"],
        "filename": file.filename,
        "path": str(file_path),
        "parent_chunks": result["parent_chunks"],
        "child_chunks": result["child_chunks"]
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
    
@router.delete("/{filename}")
def delete_document(filename: str):

    return service.delete(filename)

@router.put("/update")
async def update_document(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return service.update(str(file_path))