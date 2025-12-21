# 🚀 DevOps Runbook RAG Agent

A production-focused **Retrieval Augmented Generation (RAG)** application that helps engineers troubleshoot DevOps and infrastructure issues using **internal runbooks (PDFs)**.

This system answers **strictly from documented runbooks**, ensuring **zero hallucination**, making it safe for real-world DevOps and SRE workflows.

---

## 🧠 Problem Statement

In real DevOps environments:

- Runbooks exist as long PDFs or documents
- Searching manually during incidents is slow
- Generic AI chatbots may hallucinate solutions
- Production systems require accurate, documented answers

This project converts static DevOps runbooks into a **safe, queryable AI troubleshooting assistant**.

---

## ✅ What This Project Solves

- 🔍 Instant search across DevOps troubleshooting PDFs  
- 📄 Answers only from approved internal runbooks  
- 🛑 Prevents hallucinated responses  
- 🧩 Step-by-step troubleshooting guidance  
- ⚙️ Production-aligned DevOps support tool  

---

## 🧩 Architecture Overview

User Query
↓
FastAPI API (/ask)
↓
Vector Similarity Search
↓
Relevant Runbook Chunks
↓
LLM (Context-Grounded Answer)
↓
Structured Troubleshooting Response



---

## 🛠️ Tech Stack

- **Backend**: FastAPI  
- **LLM**: Groq (ChatGroq)  
- **Framework**: LangChain  
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2  
- **Vector Store**: In-Memory Vector Store  
- **Document Loader**: PyPDFLoader  
- **Env Management**: python-dotenv  

---

## 📂 Project Structure

.
├── app.py
├── data/
│ └── devops_troubleshoot.pdf
├── requirements.txt
├── .env
└── README.md


---

## ⚙️ How It Works

1. Loads DevOps runbook PDFs at application startup  
2. Splits documents into manageable chunks  
3. Generates embeddings for semantic search  
4. Retrieves relevant runbook sections using vector similarity  
5. LLM generates answers **only from retrieved context**

---

## 🔐 Safety & Reliability

This system is designed for production use:

- ❌ No external knowledge usage  
- ❌ No guessing or hallucination  
- ✅ Strictly context-based answers  
- ✅ Explicit fallback if answer not found  

Example fallback:
> *"This issue is not covered in the current runbook."*

---

## 🔌 API Endpoints

### Health Check

```http
GET /
{
  "status": "running"
}

POST /ask
{
  "query": "Kubernetes pod is in CrashLoopBackOff state"
}
{
  "question": "Kubernetes pod is in CrashLoopBackOff state",
  "answer": "Step-by-step troubleshooting based on runbook context"
}

🧠 Prompt Engineering

The system uses runbook-style prompt engineering:

Senior DevOps / SRE tone

Step-by-step troubleshooting format

Actionable resolution steps

Strict grounding to provided context

This ensures production-grade, reliable responses.

git clone https://github.com/your-username/devops-runbook-rag-agent.git
cd Rag_app
pip install -r requirements.txt
GROQ_API_KEY=your_groq_api_key_here

uvicorn app:app --reload

Server will run at:http://127.0.0.1:8000

📈 Resume Highlights

Built a DevOps Runbook RAG Agent for production troubleshooting

Implemented zero-hallucination AI using strict context grounding

Designed FastAPI backend with PDF ingestion & vector search

Applied prompt engineering for SRE-grade responses

🔮 Future Enhancements

Multi-runbook (multi-PDF) support

Source citations for answers

Incident severity-based responses

Supervisor agent for incident routing

Docker & Kubernetes deployment

👨‍💻 Ideal Use Cases

DevOps Engineers

SRE Teams

Internal IT Support Tools

Incident Response Systems

Enterprise AI Assistants

🏁 Conclusion

This project demonstrates real-world Agentic AI applied to DevOps, focusing on safety, reliability, and production readiness rather than generic chatbots.