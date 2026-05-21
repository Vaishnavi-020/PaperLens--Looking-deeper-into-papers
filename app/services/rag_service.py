import os
import shutil
import uuid
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .embedding_service import embedding_model
from langchain_chroma import Chroma
import re

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

        sections=split_by_sections(documents)

        #Chunking docs
        chunks=chunk_texts(sections)

        #STORE EMBEDDINGS
        vector_store=Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="chroma_db",
            collection_name="research_paper"
                )
       
        return {
                "message":"PDF Uploaded successfully.",
                "total_pages":len(documents),
                "total_chunks":len(chunks)
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

    # print(chunks[15])
    # print('\n')
    # print(chunks[16])
    # print('\n')
    # print(chunks[17])
    # print('\n')
    # print(chunks[18])
    # print('\n')
    # print(chunks[19])
    # print('\n')
    # print(chunks[20])
    # print('\n')

    return chunks


from langchain_core.documents import Document

def split_by_sections(docs):
    heading_pattern = r"^\d+(\.\d+)?\s+[A-Z].*"

    sections = []
    current_heading = "Unknown"
    current_text = ""

    for doc in docs:
        lines = doc.page_content.split("\n")

        for line in lines:
            line = line.strip()

            if re.match(heading_pattern, line):

                # Save previous section
                if current_text.strip():
                    sections.append(
                        Document(
                            page_content=current_text.strip(),
                            metadata={"heading": current_heading
                                      }
                        )
                    )

                current_heading = line
                current_text = ""

            else:
                current_text += " " + line

    # Save last section
    if current_text.strip():
        sections.append(
            Document(
                page_content=current_text.strip(),
                metadata={"heading": current_heading
                          }
            )
        )

    return sections