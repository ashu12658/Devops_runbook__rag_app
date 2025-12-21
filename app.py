from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore

# -------------------------------------------------------------------
# ENV + APP
# -------------------------------------------------------------------

load_dotenv()

app = FastAPI(
    title="DevOps RAG Agent",
    description="FastAPI-based RAG system for DevOps troubleshooting",
    version="1.0.0",
)

# -------------------------------------------------------------------
# LLM & EMBEDDINGS (loaded once)
# -------------------------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

vector_store = None

# -------------------------------------------------------------------
# LOAD RAG PIPELINE AT STARTUP
# -------------------------------------------------------------------

@app.on_event("startup")
def load_rag_pipeline():
    global vector_store

    try:
        loader = PyPDFLoader("data/devops_troubleshoot.pdf")
        documents = loader.load()

        for i, doc in enumerate(documents):
            doc.metadata["source"] = "devops_troubleshoot"
            doc.metadata["answer_id"] = i + 1

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        splits = splitter.split_documents(documents)

        vector_store = InMemoryVectorStore(embedding=embeddings)
        vector_store.add_documents(splits)

        print("✅ DevOps RAG vector store initialized")

    except Exception as e:
        print("❌ Failed to initialize RAG pipeline:", str(e))
        raise e

# -------------------------------------------------------------------
# REQUEST SCHEMA
# -------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str

# -------------------------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "running"}

# -------------------------------------------------------------------
# RAG QUERY ENDPOINT
# -------------------------------------------------------------------

@app.post("/ask")
def ask_rag(request: QueryRequest):
    if not vector_store:
        raise HTTPException(status_code=500, detail="Vector store not initialized")

    similar_docs = vector_store.similarity_search(
        query=request.query,
        k=2
    )

    if not similar_docs:
        return {
            "question": request.query,
            "answer": "No relevant context found in the knowledge base."
        }

    context = "\n\n".join(
        f"(Page {doc.metadata.get('page', 'N/A')})\n{doc.page_content}"
        for doc in similar_docs
    )

    prompt = f"""
    You are a senior DevOps SRE assistant.

    Your job is to help engineers troubleshoot production issues using an internal DevOps runbook.

    STRICT RULES:
    - Answer ONLY from the provided context.
    - If the answer is not clearly present in the context, say:
      "This issue is not covered in the current runbook."
    - Do NOT use outside knowledge.
    - Do NOT guess.

    RESPONSE STYLE:
    - Be concise and technical
    - Use bullet points or numbered steps
    - Focus on actionable troubleshooting steps
    - Mention checks, commands, or validations if present in the context

    CONTEXT (Runbook Extract):
    {context}

    USER QUESTION:
    {request.query}

    FINAL ANSWER:
    """

    response = llm.invoke(prompt)

    return {
        "question": request.query,
        "answer": response.content if hasattr(response, "content") else str(response)
    }
