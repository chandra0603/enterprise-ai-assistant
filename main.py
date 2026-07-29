from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.documents import router as document_router
from app.api.chat import router as chat_router



app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    version="1.0"
)

app.include_router(health_router)
app.include_router(document_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Knowledge Assistant"
    }