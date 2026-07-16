#Enterprise RAG Chatbot with Role-Based Access Control

An enterprise-grade Retrieval Augmented Generation (RAG) chatbot that enables employees to securely interact with organizational knowledge using Large Language Models (LLMs).
The chatbot retrieves information from domain-specific company documents stored in a vector database while enforcing **Role-Based Access Control (RBAC)**, ensuring users can only access information relevant to their department.

---

## Features

### 🔍 Retrieval Augmented Generation (RAG)
- Retrieves relevant documents using semantic search
- Generates context-aware responses using Groq-hosted LLMs
- Uses Qdrant as the vector database for efficient similarity search
---
### 🔐 Role-Based Access Control (RBAC)
Supports five organizational domains:
- HR
- Finance
- Marketing
- Engineering
- General
Users can only retrieve documents belonging to their assigned department.
Example:

- HR users cannot access Finance reports.
- Marketing users cannot access payroll information.
- General users can only query general company documents.
---

### 🛡️ Guardrails
The chatbot validates every incoming query before retrieval.
Implemented guardrails include:
- Role-based authorization
- Out-of-domain question detection
- Unsafe query detection
---

### 💬 Conversational Interface

Built using **Streamlit**, providing:

- Interactive chatbot UI
- Team selection
- Chat history
- Secure document querying

---

### 📄 Multi-format Document Support

Supports loading and indexing:

- PDF
- Markdown (.md)
- CSV

Documents are automatically:

- Loaded
- Chunked
- Embedded
- Stored in Qdrant

---

### 📊 Evaluation using RAGAS

The project includes an evaluation pipeline using **RAGAS** for:

- Synthetic test set generation
- Ground truth generation
- RAG evaluation

---

## 🏗️ Project Architecture

```
                User
                  │
                  ▼
           Streamlit Frontend
                  │
                  ▼
        Access Control Layer
      (RBAC + Guardrails)
                  │
                  ▼
          Query Validation
                  │
                  ▼
          Embedding Generation
                  │
                  ▼
              Qdrant Search
                  │
                  ▼
      Retrieved Context Chunks
                  │
                  ▼
            Groq LLM (Llama)
                  │
                  ▼
          Context-Aware Answer
```

---

## 🛠️ Tech Stack

Core framework: LangChain 
Vector Database: Qdrant 
Frontend: Streamlit 
LLM: GPT-OSS or Llama (groq) 
Cloud: Streamlit Community Cloud
Evaluation and Monitoring: Ragas

---

## 📂 Project Structure

```
chat-bot-rag-streamlit/
│
├── UI/
│   ├── login.py
│   └── chat.py
│
├── rag/
│   ├── embedding_manager.py
│   ├── file_manage.py
│   ├── retrieval.py
│   ├── vector_store.py
│   └── rag_pipeline.py
│
├── evaluation/
│   ├── test_data.py
│   └── evaluate.py
│
├── data/
│   ├── engineering/
│   ├── finance/
│   ├── general/
│   ├── HR/
│   ├── marketing/
│   └── qdrant_db2/
│
├── access_control.py
├── main.py
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
cd chat-bot-rag-streamlit
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

For Streamlit Cloud deployment, configure the same key in **Secrets**.

---

## ▶️ Run the Application

```bash
streamlit run main.py
```

---

## 📈 Evaluation (Work in Progress)

The project is currently being integrated with **RAGAS** for systematic evaluation of the RAG pipeline.

The planned evaluation workflow includes:

- Synthetic test set generation
- Ground truth generation
- Retrieval evaluation
- Answer quality evaluation
- Continuous evaluation before deployment

> **Status:** 🚧 Evaluation pipeline is currently under development and will be integrated in a future update.

---

## 🎯 Future Improvements

- Azure deployment
- Cost monitoring
- LangSmith tracing
- Hybrid Search (BM25 + Dense Retrieval)
- Cross-encoder reranking
- Conversation memory
- Conversation summarization for long chats
- Multi-turn evaluation
- CI/CD evaluation pipeline
- Improved frontend
- Memory-based querying
---

## 👩‍💻 Author

**Sowjanya G**

Final Year B.Tech Student  
National Institute of Technology Tiruchirappalli
