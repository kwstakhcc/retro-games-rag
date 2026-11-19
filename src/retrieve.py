import numpy

from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

def retrieval(knowledge_base: list[dict], model: TfidfVectorizer | SentenceTransformer,
              embeddings: csr_matrix | numpy.ndarray,
              k: int, query: str) -> list[dict]:
    
    if isinstance(model, TfidfVectorizer):
        query_vector = model.transform([query])
    elif isinstance(model, SentenceTransformer):
        query_vector = model.encode([query])
    else:
        raise TypeError(f"Expected TfidfVectorizer or SentenceTransformer instance, got {type(model).__name__}")

    similarity_scores = cosine_similarity(embeddings, query_vector).ravel()

    """If the number of retrieved chunks specified by the user is larger than the number of available chunks
       in the knowledge base, update k to retrieve all of them."""
    k = min(k, len(similarity_scores))

    top_k_indices = numpy.argsort(similarity_scores)[::-1][:k]

    """For debugging, one could return a list with pairs of the form:
       (knowledge_base[idx], similarity_scores[idx]) for idx in top_k_indices"""
    return [knowledge_base[idx] for idx in top_k_indices]
