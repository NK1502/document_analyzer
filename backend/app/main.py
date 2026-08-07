import os
from dotenv import load_dotenv

# Load environment variables FIRST before importing services
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import io
import uuid

# Import our custom services
from app.services.ai_service import chunk_text, get_embedding, get_answer
from app.services.db_service import upsert_vectors, query_vectors

app = FastAPI(title="AI Document Analyzer API")

MAX_UPLOAD_BYTES = 10 * 1024 * 1024

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    document_id: str

def extract_pdf_text(content: bytes) -> tuple[str, int]:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not read this PDF file.") from exc

    extracted_pages = []
    for page_number, page in enumerate(pdf_reader.pages, start=1):
        page_text = page.extract_text() or ""
        if page_text.strip():
            extracted_pages.append(f"[Page {page_number}]\n{page_text.strip()}")

    return "\n\n".join(extracted_pages), len(pdf_reader.pages)

@app.get("/")
def read_root():
    return {"message": "AI Document Analyzer API is running!"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or "document.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDF must be 10MB or smaller.")

    extracted_text, pages_processed = extract_pdf_text(content)
        
    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from this PDF.")

    chunks = chunk_text(extracted_text, chunk_size=800)
    document_id = str(uuid.uuid4())
    
    vectors_to_upsert = []
    
    try:
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk, task_type="retrieval_document")
            chunk_id = f"{document_id}-{i}"
            
            vectors_to_upsert.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": filename,
                    "document_id": document_id,
                    "chunk_index": i,
                },
            })
            
        upsert_vectors(vectors_to_upsert)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    
    return {
        "document_id": document_id,
        "filename": filename,
        "message": f"File processed. {len(chunks)} chunks embedded and saved to database.",
        "chunks_processed": len(chunks),
        "pages_processed": pages_processed,
    }

@app.post("/ask")
async def ask_question(request: AskRequest):
    question = request.question.strip()
    document_id = request.document_id.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")
    if not document_id:
        raise HTTPException(status_code=400, detail="Upload a document before asking questions.")
    
    try:
        question_embedding = get_embedding(question, task_type="retrieval_query")
        
        search_results = query_vectors(question_embedding, document_id=document_id, top_k=3)
        
        if not search_results.matches:
            return {"answer": "No relevant context found in the database. Please upload a document first."}
            
        context = ""
        for match in search_results.matches:
            context += match.metadata.get("text", "") + "\n\n"
            
        answer = get_answer(question, context)
        
        return {
            "answer": answer,
            "sources": sorted({match.metadata.get("source") for match in search_results.matches if match.metadata.get("source")}),
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
