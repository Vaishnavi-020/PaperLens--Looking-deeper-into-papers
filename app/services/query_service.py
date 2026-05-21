from .embedding_service import embedding_model
from app.schema.query_schema import QueryRequest
from langchain_chroma import Chroma
from app.services.llm_service import generate_answer

def ask_query(query:QueryRequest):
    #Store in Chroma
    vector_store=Chroma(
        embedding_function=embedding_model,
        persist_directory="chroma_db",
        collection_name="research_paper"
    )

    retriever=vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k":10,
                        "fetch_k":20,
                        "lambda_mult": 0.5}
    )

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
    filtered_results=filtered_results[:3]
    # print(filtered_results)
    context="\n\n".join([doc.page_content for doc in filtered_results])
    response= generate_answer(
        question=query,
        context=context
    )
    # response=[]
    # for result in filtered_results:
    #     response.append({"content":result.page_content,
    #                      "page":result.metadata.get("page",'Unknown')})

    return response
        