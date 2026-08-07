import google.generativeai as genai
import os
import textwrap

EMBEDDING_MODEL = "models/gemini-embedding-001"
GENERATION_MODEL = "gemini-3.6-flash"

def configure_gemini() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to backend/.env before using AI features.")
    genai.configure(api_key=api_key)

def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """Splits a long text into smaller chunks."""
    return [
        chunk.strip()
        for chunk in textwrap.wrap(text, width=chunk_size, break_long_words=False, replace_whitespace=False)
        if chunk.strip()
    ]

def get_embedding(text: str, task_type: str = "retrieval_document") -> list[float]:
    """Generates an embedding vector for the given text."""
    configure_gemini()
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
        output_dimensionality=768,
    )
    return result["embedding"]

def get_answer(question: str, context: str) -> str:
    """Uses Gemini to answer a question based on retrieved context."""
    configure_gemini()
    prompt = f"""
    You are an intelligent document analyzer. Use the following pieces of retrieved context from a document to answer the question. 
    If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = genai.GenerativeModel(GENERATION_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()
