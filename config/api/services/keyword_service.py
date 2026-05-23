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
입력된 문장에서 가장 핵심이라고 생각되는 한 단어를 추출하세요


[출력]
JSON 배열만 출력:
[
  {"word": "..."}
]
"""

def export_word(text):
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