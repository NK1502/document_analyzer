# 🤖 AI Document Analyzer (RAG System)

A full-stack Retrieval-Augmented Generation (RAG) web application that allows users to upload PDF documents and ask questions in real-time. Built with **FastAPI**, **Next.js 16**, **Google Gemini AI**, **Pinecone Vector Database**, **Docker**, **Render**, and **GitHub Actions**.

---

## 🌟 Key Features

- 📄 **PDF Text Extraction & Chunking**: Parses uploaded PDFs and splits text into optimal vector chunks.
- 🎯 **Document-Isolated RAG**: Each document is assigned a unique ID (`document_id`) so queries are strictly scoped to the active document.
- ⚡ **Vector Search**: Uses Pinecone Serverless Vector Database for high-speed cosine similarity retrieval.
- 🧠 **LLM Grounding**: Powered by Google Gemini (`gemini-embedding-001` & `gemini-3.6-flash`) to generate contextual answers with source references.
- 🎨 **Modern Dark UI**: Next.js 16 App Router UI built with Tailwind CSS, Framer Motion animations, and custom scrollbars.
- 🐳 **Docker & Docker Compose**: Fully containerized backend and frontend services.
- 🔄 **Automated CI/CD & Deploy**: GitHub Actions pipeline to build, push images to Docker Hub, and trigger automatic deployments on Render.

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
 | (gemini-embedding-001)|    |  (768-dim, Cosine Match) |
 +-----------------------+    +--------------------------+
```

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 16 (App Router), React 19, Tailwind CSS v4, Lucide Icons, Framer Motion |
| **Backend** | Python 3.10+, FastAPI, PyPDF2, Uvicorn |
| **AI / LLM** | Google Gemini API (`models/gemini-embedding-001` & `gemini-3.6-flash`) |
| **Vector Database** | Pinecone Serverless DB |
| **DevOps & Cloud** | Docker, Docker Compose, GitHub Actions CI/CD, Render Deployment |

---

## 🚀 Quick Start (Local Development)

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

You can spin up the entire application stack (Frontend + Backend) locally with a single command:

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

---

## 🔄 GitHub Actions CI/CD & Render Deployment

The `.github/workflows/deploy.yml` pipeline automatically triggers on `push` to `main` or `master` branch:

1. **Builds & Pushes Images** to Docker Hub:
   - `${DOCKER_USERNAME}/ai-doc-analyzer-backend:latest`
   - `${DOCKER_USERNAME}/ai-doc-analyzer-frontend:latest`
2. **Triggers Automatic Deployments** on Render via Deploy Hooks or Render API.

### 🔑 Required GitHub Secrets

To make the workflow run smoothly, add the following secrets in your GitHub repository (**Settings -> Secrets and variables -> Actions**):

| Secret Name | Description | Required? |
|---|---|---|
| `DOCKER_USERNAME` | Your Docker Hub Username | **Yes** |
| `DOCKER_PASSWORD` | Your Docker Hub Password or Personal Access Token | **Yes** |
| `NEXT_PUBLIC_API_URL` | Your deployed Render Backend URL (e.g. `https://ai-doc-backend.onrender.com`) | **Yes** (For production frontend) |
| `RENDER_BACKEND_DEPLOY_HOOK_URL` | Render Deploy Hook URL for your Backend Web Service | **Optional** (Recommended) |
| `RENDER_FRONTEND_DEPLOY_HOOK_URL` | Render Deploy Hook URL for your Frontend Web Service | **Optional** (Recommended) |
| `RENDER_API_KEY` | Render API Key (Alternative to Deploy Hooks) | **Optional** |
| `RENDER_BACKEND_SERVICE_ID` | Render Service ID for Backend (Alternative) | **Optional** |

### 🌐 Deploying to Render (Step-by-Step)

1. **Create Web Services on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/) -> **New** -> **Web Service**.
   - Connect your GitHub repository (or select **Existing Image** from Docker Hub).
2. **Backend Environment Variables on Render**:
   - `GEMINI_API_KEY`
   - `PINECONE_API_KEY`
3. **Get Deploy Hooks from Render**:
   - On your Render Web Service page -> Settings -> **Deploy Hook** -> Copy the URL.
   - Save it as `RENDER_BACKEND_DEPLOY_HOOK_URL` in GitHub Secrets.
