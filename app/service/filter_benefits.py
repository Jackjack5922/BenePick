import pandas as pd
import json
from typing import Dict, Any, List

# ✅ JSON 파일 로드 함수
def load_service_data(json_path: str) -> pd.DataFrame:
    """
    JSON 파일을 로드하여 pandas DataFrame으로 반환합니다.

    Args:
        json_path (str): 병합된 혜택 JSON 파일 경로

    Returns:
        pd.DataFrame: 혜택 목록 DataFrame
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# ✅ 사용자 조건 기반 필터링 함수
def filter_services_by_user_input(
    df: pd.DataFrame,
    user_input: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    사용자 입력 정보를 기반으로 조건에 부합하는 혜택을 필터링합니다.

    Args:
        df (pd.DataFrame): 혜택 목록 DataFrame
        user_input (dict): 사용자 입력 정보 (나이, 성별, 소득구간, 출산여부, 지역)

    Returns:
        List[dict]: 추천 가능한 혜택 리스트
    """
    results = []

    for _, row in df.iterrows():
        조건: Dict[str, bool] = row.get("조건", {})
        연령: Dict[str, Any] = row.get("대상연령", {})
        기관: str = row.get("소관기관명", "")

        # ① 연령 필터
        age_ok = True
        if "나이" in user_input and 연령:
            시작 = 연령.get("시작")
            종료 = 연령.get("종료")
            if 시작 is not None and user_input["나이"] < 시작:
                age_ok = False
            if 종료 is not None and user_input["나이"] > 종료:
                age_ok = False
        if not age_ok:
            continue

        # ② 조건 필터
        조건_매핑 = {
            "성별": user_input.get("성별"),
            "소득구간": user_input.get("소득구간"),
            "출산여부": "출산/입양" if user_input.get("출산여부") else None
        }
        조건_ok = True
        for _, 키 in 조건_매핑.items():
            if 키 and not 조건.get(키, False):
                조건_ok = False
                break
        if not 조건_ok:
            continue

        # ③ 지역 필터
        if "지역" in user_input and user_input["지역"] not in 기관:
            continue

        # ✅ 모든 조건을 통과한 혜택 저장
        results.append({
            "서비스명": row["서비스명"],
            "지원내용": row.get("지원내용", ""),
            "소관기관": 기관,
            "신청방법": row.get("신청방법", ""),
        })

    return results

# ✅ 샘플 실행
if __name__ == "__main__":
    json_path = "./data/combined_service_data_merged.json"  # JSON 위치를 본인 환경에 맞게 수정
    df = load_service_data(json_path)

    # 사용자 입력 예시
    user_input = {
        "나이": 34,
        "성별": "남성",
        "소득구간": "중위소득 76~100%",
        "출산여부": True,
        "지역": "경상남도 김해시"
    }

    # 필터링 수행
    results = filter_services_by_user_input(df, user_input)

    # 출력
    print("✅ 추천 가능한 혜택 수:", len(results))
    for r in results:
        print(f"- {r['서비스명']}: {r['지원내용']}")
