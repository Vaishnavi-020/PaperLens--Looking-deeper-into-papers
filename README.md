## PaperLens - AI-Powered Research Paper Assistant

PaperLens is a Retrieval-Augmented Generation (RAG) based application that helps users interact with research papers through natural language conversations. Instead of manually searching through lengthy academic documents, users can upload a research paper and ask questions to instantly retrieve relevant information and insights.

---

## Features

- Upload research papers in PDF format
- Ask natural language questions about the document
- Context-aware responses using RAG architecture
- Semantic document retrieval for accurate answers
- Session-wise chat history storage
- Faster exploration of complex research papers

---

## Tech Stack

### Backend

- Python

### AI & NLP

- LangChain
- Groq API
- Embedding Models
- RAG

### Vector Database 

- ChromaDB

### Data Processing

- PyPDF
- Text Chunking
- Embedding Generation

---

## How it works

1. User uploads a research paper.
2. The document is extracted and split into smaller chunks.
3. Embeddings are generated for each chunk.
4. Chunks are stored in a vector database.
5. When a user asks a question:
- Relevant chunks are retrieved using semantic similarity search.
- Retrieved context is provided to the LLM.
- The model generates a grounded and context-aware response.

---

## Challenge: Improving Retrieval Quality in the RAG Pipeline

One of the biggest challenges while building the Research Paper Q&A system was ensuring that the retriever returned the most relevant chunks from uploaded PDFs.

Initially, despite successful PDF ingestion and embedding generation, the retriever often returned irrelevant content such as tables, figure captions, visualization sections, and even acknowledgement text instead of the passages that directly answered the user's query. In some cases, highly similar chunks were retrieved multiple times, reducing the diversity and usefulness of the context provided to the LLM.

To address this, I experimented with different chunking strategies and overlap sizes. I analyzed retrieved chunks manually, tuned MMR (Max Marginal Relevance) retrieval parameters, improved chunk boundaries to preserve semantic meaning, and filtered noisy PDF content. These iterations significantly improved retrieval accuracy and resulted in more relevant and context-rich responses from the system.

---

## Future Improvements

- Automatic paper summarization
- Multi-document querying

---

## Author

Vaishnavi Sinha