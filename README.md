# 📌 Benepick: 정부 혜택 추천 서비스

**Benepick**은 사용자 조건(나이, 소득, 지역 등)을 기반으로 공공데이터에서 정부 지원금·혜택 정보를 필터링하고, LLM + 벡터 검색(RAG)을 통해 자연어 질의에 응답하는 **AI 기반 추천 앱**입니다.

---

## 🧩 프로젝트 구조

C:.
│ .env
│ .gitignore
│ build_faiss.py # FAISS 벡터 인덱스 생성
│ run_pipeline.py # 데이터 수집 및 처리 실행
│ README.md
│ requirements.txt
│
├─app # FastAPI 앱
│ │ main.py # 앱 실행 엔트리포인트
│ │ router.py # API 라우터
│ │ init.py
│ ├─models/ # 입력 데이터 모델 정의
│ │ └─user_input.py
│ ├─service/ # 비즈니스 로직 (필터, LLM 응답, 벡터 검색)
│ │ ├─filter_benefits.py
│ │ ├─llm_response.py
│ │ └─vector_search.py
│ └─pycache/
│
├─data/ # 수집된 JSON 데이터
│ combined_service_data.json
│ combined_service_data_merged.json
│ serviceDetail_all.json
│ supportConditions_all.json
│ supportConditions_model.json
│
├─data_pipeline/gov/ # 공공데이터 수집/전처리 파이프라인
│ gov24_api_fetcher.py
│ gov24_data_pipeline.py
│ support_model_crawler.py
│
└─embedding/faiss_index/ # FAISS 인덱스 저장
index.faiss
index.pkl

yaml
복사
편집

---

## ⚙️ 설치 및 실행 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
2. 데이터 수집 및 전처리
bash
복사
편집
python run_pipeline.py
data_pipeline/gov/ 모듈들이 실행되어 혜택 데이터를 수집 및 병합합니다.

3. 벡터 인덱스 생성
bash
복사
편집
python build_faiss.py
혜택 텍스트 데이터가 임베딩되어 FAISS 인덱스로 저장됩니다.

4. FastAPI 앱 실행
bash
복사
편집
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs에서 Swagger UI 확인 가능

🧠 시스템 아키텍처
css
복사
편집
[공공데이터 API] ──▶ [데이터 파이프라인] ──▶ [혜택 JSON 저장]
                                               │
                                               ▼
                                        [FAISS 인덱스 생성]
                                               │
                  ┌────────────────────────────┘
                  ▼
[사용자 입력] ──▶ [조건 기반 필터링] ──▶ [RAG 벡터 검색 + LLM 응답]
조건 필터링: 나이, 지역, 소득 등 조건 기반 혜택 필터링

RAG 구조: ko-SBERT 임베딩 + FAISS 벡터 검색 + GPT 모델 응답

LLM 응답 생성: 유사 문서 기반 자연어 질의 대응

📦 주요 기술 스택
분야	기술
백엔드	FastAPI
임베딩	intfloat/multilingual-e5-base, ko-SBERT
벡터 검색	FAISS
LLM	OpenAI GPT (또는 Upstage Solar)
데이터 수집	공공데이터포털 API, Selenium 크롤링
문서 저장	JSON 기반 정제 데이터

✨ 향후 개선 방향
민간 혜택 추가 (카드사, 통신사 등)

사용자 조건 자동 추출 (OCR / 챗봇 인터페이스)

다국어 지원

벡터 검색 성능 최적화 (Hybrid Search 등)

🙋‍♂️ 개발자
전종훈 (Jackjack5922)

Github

yaml
복사
편집

---

필요하면 `.env 예시`, API 응답 샘플, 또는 Swagger 사용법도 확장해서 넣어드릴 수 있습니다. 더 추가할 내용 있을까