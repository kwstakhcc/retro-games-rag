import os
import joblib

import numpy

from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

from src.config import PROJECT_DIRECTORY_PATH, MODELS_DIRECTORY_PATH


def get_model(model_id: str, corpus: list[str]) -> TfidfVectorizer | SentenceTransformer:

    os.makedirs(MODELS_DIRECTORY_PATH, exist_ok=True)

    if model_id == 'tfidf':
        tfidf_path = os.path.join(MODELS_DIRECTORY_PATH, f"{model_id}_model.joblib")

        if os.path.isfile(tfidf_path): return joblib.load(tfidf_path)
        else:
            model = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            fitted_model = model.fit(corpus)
            joblib.dump(fitted_model, tfidf_path)

    elif model_id == 'minilm':
        minilm_path = os.path.join(MODELS_DIRECTORY_PATH, f"{model_id}_model")

        if os.path.isdir(minilm_path): return SentenceTransformer(minilm_path)
        else:
            model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            model.save(minilm_path)

    else:
        raise ValueError(f"Unknown model_id: {model_id}")

    return model

def get_embeddings(corpus: list[str], model: TfidfVectorizer | SentenceTransformer) -> csr_matrix | numpy.ndarray:
    if isinstance(model, TfidfVectorizer):
        tfidf_embeddings_path = os.path.join(MODELS_DIRECTORY_PATH, 'tfidf_embeddings.joblib')

        if os.path.isfile(tfidf_embeddings_path): return joblib.load(tfidf_embeddings_path)
        else:
            embeddings = model.transform(corpus)
            joblib.dump(embeddings, tfidf_embeddings_path)

    elif isinstance(model, SentenceTransformer):

        minilm_embeddings_path = os.path.join(MODELS_DIRECTORY_PATH, 'minilm_embeddings.npy')
        
        if os.path.isfile(minilm_embeddings_path): return numpy.load(minilm_embeddings_path)
        else:
            embeddings = model.encode(corpus)
            numpy.save(minilm_embeddings_path, embeddings)
    else:
        raise TypeError(f"Expected TfidfVectorizer or SentenceTransformer instance, got {type(model).__name__}")

    return embeddings

def get_model_and_embeddings(model_id: str, corpus: list[str]) -> tuple[TfidfVectorizer | SentenceTransformer, csr_matrix | numpy.ndarray]:
    model = get_model(model_id, corpus)
    return model, get_embeddings(corpus, model)
