import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.router import router


app = FastAPI(
    title="Benepick - 혜택 추천 API",
    description="사용자 입력 기반 정부/민간 혜택 추천 시스템",
    version="0.1"
)

app.include_router(router)