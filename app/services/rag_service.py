import os
import shutil
import uuid
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .embedding_service import embedding_model
from langchain_chroma import Chroma

UPLOAD_DIR="temp_uploads"

os.makedirs(UPLOAD_DIR,exist_ok=True)

CHROMA_PATH='./chroma_db'

# UPLOADING PDF
async def process_pdf(file:UploadFile):

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("chroma deleted")

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

        retriever=vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k":10,
                           "fetch_k":20,
                           "lambda_mult": 0.5}
        )

        query="How does multi-head attention work?"
        results=retriever.invoke(query)
        filtered_results=[]
        for doc in results:
            text=doc.page_content.lower()
            noise_patterns=[
                "figure",
                "visualization",
                "<pad>",
                "<eos>",
                "layer5"
            ]
            if any(pattern in text for pattern in noise_patterns):
                continue
            if "table" in text and len(text.split())<300:
                continue
            filtered_results.append(doc)
        filtered_results=filtered_results[:5]
            
        for i,doc in enumerate(filtered_results):
            print(f"\n-----Result------{i+1}")
            print(doc.page_content[:600])
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
            chunk_size=1000,
            chunk_overlap=120,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )
    chunks=splitter.split_documents(doc)

    # print(chunks[4].page_content)
    # print("\n")
    # print(chunks[5].page_content)
    # print("\n")
    # print(chunks[6].page_content)
    # print("\n")
    # print(chunks[7].page_content)
    # print("\n")
    # print(chunks[8].page_content)
    # print("\n")

    return chunks
