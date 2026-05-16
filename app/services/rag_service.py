import os
import uuid
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .embedding_service import embedding_model
from langchain_chroma import Chroma

UPLOAD_DIR="temp_uploads"

os.makedirs(UPLOAD_DIR,exist_ok=True)

# UPLOADING PDF
async def process_pdf(file:UploadFile):
    if not file.filename.endswith(".pdf"):
        return{
            "error":"Only pdf files allowed"
        }
    unique_filename=f"{uuid.uuid4()}.pdf"
    file_path=os.path.join(UPLOAD_DIR,unique_filename)

    try:
        with open(file_path,"wb") as buffer:
            content=await file.read()
            buffer.write(content)

        #Loading docs
        loader=PyPDFLoader(file_path)
        documents=loader.load()

        #Chunking docs
        chunks=chunk_texts(documents)

        #Store in Chroma
        vector_store=Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="chroma_db",
            collection_name="research_paper"
        )
        preview_text=(documents[0].page_content[:500])

        return {
            "message":"PDF Uploaded successfully.",
            "total_pages":len(documents),
            "total_chuks":len(chunks)
        }
    except Exception as e:
        return {
            "error":str(e)
        }
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# CHUNKING DOCUMENTS
def chunk_texts(doc):
    splitter=RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=160,
            separators=[
                "\n\n",
                "\n",
                ".",
                " ",
                ""
            ]
        )
    chunks=splitter.split_documents(doc)

    return chunks
