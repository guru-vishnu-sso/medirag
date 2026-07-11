import faiss
import numpy as np


def create_faiss_index(embeddings):
    """
    Create FAISS index.
    """

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_index(index, query_embedding, k=3):
    """
    Search top-k similar vectors.
    """

    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, k)

    return indices[0]