from fastapi import FastAPI
from app.router.rag_router import router as rag_router

app=FastAPI()

app.include_router(rag_router)