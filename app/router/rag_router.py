from fastapi import APIRouter,UploadFile,File
from app.services.rag_service import process_pdf

router=APIRouter(prefix="/rag",tags=["RAG"])

@router.post("/upload")
async def upload_pdf(file:UploadFile=File(...)):
    result=await process_pdf(file)

    return result