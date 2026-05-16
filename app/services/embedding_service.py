from langchain_huggingface import HuggingFaceEmbeddings
import os
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()


embedding_model=HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2"
        )