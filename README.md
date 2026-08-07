# 🤖 AI Document Analyzer (RAG System)

A full-stack Retrieval-Augmented Generation (RAG) web application that allows users to upload PDF documents and ask questions in real-time. Built with **FastAPI**, **Next.js 16**, **Google Gemini AI**, **Pinecone Vector Database**, **Docker**, and **GitHub Actions**.

---

## 🌟 Key Features

- 📄 **PDF Text Extraction & Chunking**: Parses uploaded PDFs and splits text into optimal vector chunks.
- 🎯 **Document-Isolated RAG**: Each document is assigned a unique ID (`document_id`) so queries are strictly scoped to the active document.
- ⚡ **Vector Search**: Uses Pinecone Serverless Vector Database for high-speed cosine similarity retrieval.
- 🧠 **LLM Grounding**: Powered by Google Gemini (`text-embedding-004` & `gemini-1.5-flash`) to generate contextual answers with source references.
- 🎨 **Modern Dark UI**: Next.js 16 App Router UI built with Tailwind CSS, Framer Motion animations, and custom scrollbars.
- 🐳 **Docker & Docker Compose**: Fully containerized backend and frontend services.
- 🔄 **DevOps CI/CD**: Automated GitHub Actions workflow to build and push Docker images to Docker Hub on every commit.

---

## 🛠️ Architecture & Tech Stack

```text
           +---------------------------------+
           |   Next.js 16 + Tailwind CSS UI  |
           +---------------------------------+
                            |
                     REST API Calls
                            v
           +---------------------------------+
           |      FastAPI Python Server      |
           +---------------------------------+
              /                           \
   Embeddings & Text              Vector Search & Storage
            v                               v
 +-----------------------+    +--------------------------+
 |   Google Gemini AI    |    |  Pinecone Vector DB      |
 | (embedding-004/flash) |    |  (768-dim, Cosine Match) |
 +-----------------------+    +--------------------------+
```

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 16 (App Router), React 19, Tailwind CSS v4, Lucide Icons, Framer Motion |
| **Backend** | Python 3.10+, FastAPI, PyPDF2, Uvicorn |
| **AI / LLM** | Google Gemini API (`text-embedding-004` & `gemini-1.5-flash`) |
| **Vector Database** | Pinecone Serverless DB |
| **DevOps** | Docker, Docker Compose, GitHub Actions CI/CD |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.10+
- Pinecone API Key ([Get Free Key](https://app.pinecone.io/))
- Google Gemini API Key ([Get Free Key](https://aistudio.google.com/app/apikey))

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive API Documentation will be available at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🐳 Running with Docker Compose

You can spin up the entire application stack (Frontend + Backend) with a single command:

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

---

## 🔄 CI/CD Pipeline (GitHub Actions)

The `.github/workflows/docker-publish.yml` automatically triggers on `push` to `main` branch:
1. Builds the backend Docker container.
2. Authenticates with Docker Hub using repository secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`).
3. Pushes the updated image to Docker Hub.
