from fastapi import APIRouter,Depends
from app.services.query_service import ask_query
from app.schema.query_schema import QueryRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.chat_model import ChatHistory

router=APIRouter(prefix="/chat",tags=["Chat"])

@router.post("/")
def ask_question(query:QueryRequest,db:Session=Depends(get_db)):
    result=ask_query(query,db)
    return {
        "query":query,
        "results":result
    }

@router.get("/history/{session_id}")
def get_chat_history(session_id:str,db:Session=Depends(get_db)):
    history=db.query(ChatHistory).filter(ChatHistory.session_id==session_id).all()
    return history