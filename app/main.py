from fastapi import FastAPI
from app.router.rag_router import router as rag_router
from app.router.chat_route import router as chat_router
from app.model.base import Base
from app.database import engine
from app.model.chat_model import ChatHistory

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(rag_router)
app.include_router(chat_router)