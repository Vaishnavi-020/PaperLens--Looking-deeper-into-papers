from fastapi import APIRouter
from app.services.query_service import ask_query
from app.schema.query_schema import QueryRequest

router=APIRouter(prefix="/chat",tags=["Chat"])

@router.post("/")
def ask_question(query:QueryRequest):
    result=ask_query(query.question)
    return {
        "query":query,
        "results":result
    }
