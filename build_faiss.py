import os
import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# ✅ 임베딩 모델 로드
model = SentenceTransformer("jhgan/ko-sbert-sts")

# ✅ 혜택 데이터 로드
json_path = "./data/combined_service_data_merged.json"
df = pd.read_json(json_path)

# ✅ 문서(text) 목록 생성
documents = []
metadata = []

for i, row in df.iterrows():
    title = row.get("서비스명", "")
    desc = row.get("지원내용", "")
    text = f"{title}: {desc}".strip()
    if not text or text == ":":
        continue
    documents.append(text)
    metadata.append({
        "서비스명": title,
        "지원내용": desc,
        "소관기관": row.get("소관기관명", ""),
        "신청방법": row.get("신청방법", "")
    })

# ✅ 임베딩 생성
print("🧠 임베딩 생성 중...")
embeddings = model.encode(documents, show_progress_bar=True, convert_to_numpy=True)

# ✅ FAISS 인덱스 생성
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ✅ 저장 경로 생성
save_dir = "./embedding/faiss_index"
os.makedirs(save_dir, exist_ok=True)

# ✅ 인덱스 저장
faiss.write_index(index, os.path.join(save_dir, "index.faiss"))

# ✅ 메타데이터 저장
with open(os.path.join(save_dir, "index.pkl"), "wb") as f:
    pickle.dump(metadata, f)

print("✅ FAISS 인덱스 및 메타데이터 저장 완료")
print(f"총 임베딩 문서 수: {len(documents)}")
