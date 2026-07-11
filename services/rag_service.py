from services.pdf_service import extract_text_from_pdf
from services.chunk_service import chunk_text
from services.embedding_service import generate_embeddings
from services.faiss_service import create_faiss_index
from services.search_service import retrieve_chunks
from services.gemini_service import ask_gemini


def process_pdf(file_path):

    pages = extract_text_from_pdf(file_path)

    chunks = chunk_text(pages)

    embeddings = generate_embeddings(chunks)

    index = create_faiss_index(embeddings)

    return pages, chunks, embeddings, index


def answer_question(
        question,
        index,
        chunks,
        language="English"
):

    retrieved_chunks = retrieve_chunks(
        question,
        index,
        chunks,
        top_k=3
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    answer = ask_gemini(
        question,
        context,
        language
    )

    return {
        "answer": answer,
        "chunks": retrieved_chunks
    }