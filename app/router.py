from fastapi import APIRouter
from pydantic import BaseModel
from app.models.user_input import UserInput
from app.service.filter_benefits import load_service_data, filter_services_by_user_input
from app.service.vector_search import semantic_search
from app.service.llm_response import generate_response_from_benefits

import os

router = APIRouter()

json_path = os.path.join(os.path.dirname(__file__), "..", "data", "combined_service_data_merged.json")
data = load_service_data(json_path)

class QueryInput(BaseModel):
    query: str

@router.post("/recommend")
def recommend_benefits(user_input: UserInput):
    result = filter_services_by_user_input(data, user_input.dict())
    return {"추천_개수": len(result), "혜택목록": result}

@router.post("/semantic-recommend")
def semantic_recommend(input: QueryInput):
    hits = semantic_search(input.query)
    llm_output = generate_response_from_benefits(input.query, hits)
    return {"검색_결과": hits, "응답": llm_output}
