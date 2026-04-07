from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore

load_dotenv()

# -------------------------------------------------------------------
# APP
# -------------------------------------------------------------------

app = FastAPI(
    title="DevOps RAG Agent",
    description="FastAPI-based RAG system for DevOps troubleshooting",
    version="1.0.0",
)

# -------------------------------------------------------------------
# GLOBALS (initialized at startup)
# -------------------------------------------------------------------

embeddings = None
llm = None
vector_store = None

# -------------------------------------------------------------------
# STARTUP: ENV + RAG INIT
# -------------------------------------------------------------------

@app.on_event("startup")
def load_rag_pipeline():
    global embeddings, llm, vector_store

    # ---- ENV VARS (Render injects these) ----
    HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not HF_TOKEN:
        raise RuntimeError("HUGGINGFACEHUB_API_TOKEN not set in Render env")

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set in Render env")

    # ---- EMBEDDINGS (REMOTE, MEMORY SAFE) ----
    embeddings = HuggingFaceEndpointEmbeddings(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=HF_TOKEN,
    )

    # ---- LLM ----
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=GROQ_API_KEY,
    )

    try:
        loader = PyPDFLoader("data/devops_troubleshoot.pdf")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
        )

        splits = splitter.split_documents(documents)

        vector_store = InMemoryVectorStore(embedding=embeddings)
        vector_store.add_documents(splits)

        print("DevOps RAG vector store initialized")

    except Exception as e:
        print("RAG init failed:", str(e))
        raise e

# -------------------------------------------------------------------
# SCHEMA
# -------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str

# -------------------------------------------------------------------
# HEALTH
# -------------------------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "running"}

# -------------------------------------------------------------------
# RAG ENDPOINT
# -------------------------------------------------------------------

@app.post("/ask")
def ask_rag(request: QueryRequest):
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store not initialized")

    docs = vector_store.similarity_search(
        query=request.query,
        k=2,
    )

    if not docs:
        return {
            "question": request.query,
            "answer": "No relevant context found in the knowledge base.",
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a senior DevOps SRE assistant.

RULES:
- Answer ONLY from the context
- If not found, say: "This issue is not covered in the current runbook."

CONTEXT:
{context}

QUESTION:
{request.query}

ANSWER:
"""

    response = llm.invoke(prompt)

    return {
        "question": request.query,
        "answer": response.content,
    }
