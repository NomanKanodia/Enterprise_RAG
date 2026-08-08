from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.query import router as query_router

app = FastAPI(
    title="Enterprise RAG API",
    description="Enterprise Knowledge Assistant",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(query_router)


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG API is running!"
    }