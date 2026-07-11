from services.embedding_service import generate_embeddings
from services.faiss_service import search_index


def retrieve_chunks(question, index, chunks, top_k=3):
    """
    Retrieve the most relevant chunks.
    """

    # Create embedding for the user's question
    question_embedding = generate_embeddings(
        [{"page": 0, "text": question}]
    )

    # Search FAISS
    indices = search_index(
        index,
        question_embedding[0],
        top_k
    )

    # Return chunk dictionaries
    retrieved_chunks = [chunks[i] for i in indices]

    return retrieved_chunks