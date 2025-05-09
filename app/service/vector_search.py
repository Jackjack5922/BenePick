import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

FAISS_DIR = "./embedding/faiss_index"
model = SentenceTransformer("jhgan/ko-sbert-sts")

def semantic_search(query: str, top_k: int = 5):
    """
    쿼리 기반 의미 유사 혜택 검색
    """
    # ✅ 함수 내에서 인덱스 로딩 (지연 로딩)
    index = faiss.read_index(os.path.join(FAISS_DIR, "index.faiss"))
    with open(os.path.join(FAISS_DIR, "index.pkl"), "rb") as f:
        metadata = pickle.load(f)

    query_vec = model.encode([query])
    scores, indices = index.search(np.array(query_vec), top_k)

    results = []
    for i in indices[0]:
        results.append(metadata[i])
    return results
