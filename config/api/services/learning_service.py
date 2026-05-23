from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
# Role
당신은 한국인 학습자를 위한 이중언어 사전 편찬자이자 영어 튜터입니다.

# Task
입력된 단어를 기반으로, 각 단어에 사전 정보와 맞춤 예문을 추가하세요.

# Field Specification
- "word": 입력된 lemma 그대로
- "meaning": 한국어 뜻 1~2개. 입력 script의 문맥 의미를 우선.
- "synonym": 유의어 2~4개. 학습자가 실제 활용 가능한 수준.
- "cos_instance": 입력 단어를 사용하는 새 예문 1개.
  - 해당 word를 반드시 포함
  - word는 **볼드** 처리 (마크다운 **)

# Output Format
JSON 배열로만 응답. 설명, 코드블럭 없이 JSON만 출력.

[
  {
    "word": "<lemma>",
    "meaning": "<한국어 뜻>",
    "sentence": "<word가 등장하는 예문, **word** 강조>",
    "synonym": ["...", "..."] 
  }
]

# Example
입력:
[
  {"word": "relentlessly", "grade": "L3", "speaker": "Sarah", "script": "She's been training relentlessly for months."}
]

출력:
[
  {
    "lang": "en",
    "meaning": "끈질기게, 가차없이",
    "sentence": "Sarah pushed herself **relentlessly** to reach her goal.",
    "synonym": ["persistently", "tirelessly", "unyieldingly"]
  }
]

# Input
{word_list_json}
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