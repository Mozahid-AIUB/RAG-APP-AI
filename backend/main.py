import os
import shutil
import pandas as pd
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

app = FastAPI(title="Excel RAG Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store the vector store and LLM
vector_store = None
qa_chain = None

# Initialize Embeddings (Local)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

class QueryRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    global vector_store, qa_chain
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel or CSV file.")

    try:
        # Save uploaded file temporarily
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load Excel or CSV using pandas
        df = pd.read_csv(temp_file) if file.filename.endswith('.csv') else pd.read_excel(temp_file)
        os.remove(temp_file) # Clean up
        
        # Convert each row into a document
        documents = []
        for index, row in df.iterrows():
            # Combine column names and values for better context
            content = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            documents.append(Document(page_content=content, metadata={"row": index}))
            
        # Split documents if they are too large (though usually rows are small)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = text_splitter.split_documents(documents)
        
        # Create Vector Store
        vector_store = FAISS.from_documents(split_docs, embeddings)
        
        # Initialize LLM via OpenRouter
        llm = ChatOpenAI(
            model="deepseek/deepseek-chat",
            temperature=0,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )
        
        # Create QA Chain
        prompt_template = """Use the following pieces of context from the uploaded Excel file to answer the question at the end. 
Keep the answer concise and professional. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}
Helpful Answer:"""
        
        QA_PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            chain_type_kwargs={"prompt": QA_PROMPT}
        )
        
        return {"message": f"Successfully processed {len(documents)} rows from {file.filename}."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_excel(request: QueryRequest):
    global qa_chain
    
    if qa_chain is None:
        raise HTTPException(status_code=400, detail="Please upload an Excel file first.")
    
    try:
        response = qa_chain.invoke(request.query)
        return {"answer": response["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
