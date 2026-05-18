from fastapi import FastAPI
from app.router.rag_router import router as rag_router
from app.router.chat_route import router as chat_router

app=FastAPI()

app.include_router(rag_router)
app.include_router(chat_router)