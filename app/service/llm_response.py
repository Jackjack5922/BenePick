import os
from openai import OpenAI
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response_from_benefits(query: str, items: List[dict]) -> str:
    """
    혜택 리스트를 요약해 자연스러운 답변 생성 (GPT)
    """
    joined = "\n".join([f"- {x['서비스명']}: {x['지원내용']}" for x in items])
    prompt = f"""
    사용자가 다음과 같은 질문을 했습니다: "{query}"
    아래는 관련된 정부 혜택입니다:

    {joined}

    위 내용을 바탕으로 자연스럽고 친절한 한국어 문장으로 요약하여 설명해주세요.
    """

    completion = client.chat.completions.create(
        model="gpt-4",  # 또는 gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()
