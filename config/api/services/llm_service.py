from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
당신은 OCR 결과물을 정제하는 자연어 처리 전문가입니다.

[역할]
OCR로 추출된 텍스트에서 실제 대사만 복원합니다.

[규칙]
- OCR 오류를 문맥에 맞게 교정
- UI/HUD/광고 제거
- 화자별로 분리
- 불명확한 화자는 "unknown"
- 신뢰도 낮은 문장은 제외
- 번역 금지

[출력]
JSON 배열만 출력:
[
  {"speaker": "...", "script": "..."}
]
"""

def analyze_text(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
       temperature=0,
       messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"OCR 텍스트:\n{text}"},
        ]
    )
    content = parse_llm_json(response.choices[0].message.content)
    return content

def parse_llm_json(content):
    content = content.strip()

    # 1️⃣ 코드블럭 제거
    if content.startswith("```"):
        content = content.split("```")[1]

    # 2️⃣ JSON 부분만 추출 (핵심)
    match = re.search(r'\[.*\]', content, re.DOTALL)
    if match:
        content = match.group(0)

    # 3️⃣ 파싱
    return json.loads(content)