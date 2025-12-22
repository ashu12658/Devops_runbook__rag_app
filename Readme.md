🚀 DevOps Runbook RAG Agent

A production-focused Retrieval Augmented Generation (RAG) application that helps engineers troubleshoot DevOps and infrastructure issues using internal runbooks (PDFs).

The system generates strictly context-grounded answers from runbooks, reducing hallucinations and making it suitable for real-world DevOps and SRE workflows.

🔗 Live Demo

https://devops-runbook-rag-application-48vs.onrender.com/docs

🧠 Problem Statement

In real DevOps environments:

Runbooks exist as long PDFs

Manual searching during incidents is slow

Generic AI tools may guess or hallucinate

Production systems require documented, reliable answers

This project turns static DevOps runbooks into a safe, queryable AI troubleshooting assistant.

✅ What This Project Solves

🔍 Instant semantic search across DevOps runbook PDFs

📄 Answers only from approved documentation

🛑 Prevents unsupported or guessed responses

🧩 Step-by-step troubleshooting guidance

⚙️ Production-aligned DevOps support tool

🧩 Architecture Overview

User sends a query

FastAPI /ask endpoint receives the request

Vector similarity search over runbook embeddings

Relevant runbook chunks are retrieved

LLM generates a response strictly from retrieved context

Fallback message if the answer is not found

🛠️ Tech Stack

Backend: FastAPI

LLM: Groq (ChatGroq)

Framework: LangChain

Embeddings: sentence-transformers/all-MiniLM-L6-v2

Vector Store: In-memory vector store

Document Loader: PyPDFLoader

Environment Management: python-dotenv

📂 Project Structure
.
├── app.py
├── data/
│   └── devops_troubleshoot.pdf
├── requirements.txt
├── .env
└── README.md

⚙️ How It Works

Loads DevOps runbook PDFs at application startup

Splits documents into manageable chunks

Generates embeddings for semantic search

Retrieves relevant runbook sections

Generates answers strictly from retrieved content

🔐 Safety & Reliability

❌ No external knowledge usage

❌ No guessing or unsupported answers

✅ Strict context-based responses

✅ Clear fallback if answer is not in the runbook

Example fallback:

"This issue is not covered in the current runbook."

🔌 API Endpoints
Health Check
GET /


Response:

{ "status": "running" }

Ask a Question
POST /ask


Request:

{ "query": "server is slow" }


Response (example):

{
  "question": "server is too slow",
  "answer": "See Chapter 2: Why Is the Server So Slow?... (runbook-based response)"
}

🧠 Prompt Engineering Strategy

Senior DevOps / SRE tone

Step-by-step troubleshooting format

Actionable remediation steps

Explicit instruction to avoid external knowledge

Fallback when context is missing

⚙️ Run Locally
git clone https://github.com/ashu12658/Devops_runbook__rag_app.git
cd Devops_runbook__rag_app
pip install -r requirements.txt


Create .env file:

GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingfacehub_api_key_here


Run the server:

uvicorn app:app --reload

📈 Resume Highlights

Built a DevOps Runbook RAG Agent for production troubleshooting

Implemented hallucination-controlled AI using strict context grounding

Designed FastAPI backend with PDF ingestion and vector search

Deployed a production-ready RAG application on Render

🔮 Future Enhancements

Multi-runbook (multi-PDF) support

Source citations for answers

Incident severity-based responses

Supervisor agent for incident routing

Docker & Kubernetes deployment

🏁 Conclusion

This project demonstrates practical Agentic AI applied to DevOps, focusing on safety, reliability, and production readiness rather than generic chatbots.
