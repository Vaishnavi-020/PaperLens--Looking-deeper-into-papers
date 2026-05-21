from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(model="deepseek-ai/DeepSeek-V4-Pro",
                        task="Text-generation",
                        huggingfacehub_api_token=os.getenv("HUGGINGFACE_ACCESS_TOKEN"))

model=ChatHuggingFace(llm=llm)

prompt=PromptTemplate(
    template = """
You are an expert research assistant.

Use ONLY the provided context to answer.

Guidelines:
- For "why" questions, explain the reasoning clearly.
- For summary requests, summarize the relevant section.
- If information exists across multiple chunks,
combine them into one coherent answer.
- If the answer is not present, say:
"I could not find this in the paper."

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=['question','context']
)

parser=StrOutputParser()

chain= prompt | model | parser

def generate_answer(question:str, context:str):
    response=chain.invoke({"question":question,
                           "context":context})
    
    return response