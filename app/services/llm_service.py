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
    template='''You are a helpful assistant.
    Answer the given question only from the context provided. 
    If provided context is not enough for the question, just say: "I could not find this in the uploaded paper."
    \n
    Question:
    {question}
    \n
    Context:
    {context}''',
    input_variables=['question','context']
)

parser=StrOutputParser()

chain= prompt | model | parser

def generate_answer(question:str, context:str):
    response=chain.invoke({"question":question,
                           "context":context})
    
    return response