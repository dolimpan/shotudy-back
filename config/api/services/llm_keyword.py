from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
주어진 텍스트에서 가장 핵심적인 단어 1개만 추출하세요.

[규칙]
- 반드시 단어 1개만
- 설명 금지
- 조사/불필요한 단어 제외
- 반드시 JSON만 출력하세요
- 다른 텍스트 절대 포함 금지 

[출력]
{"keyword": "단어"}
"""

def extract_keyword(text):
    if not text:
        return {"error": "empty text"}

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            response_format={"type": "json_object"}
        )

        data = json.loads(response.choices[0].message.content)

        if "keyword" not in data:
            return {"error": "키워드 없음", "raw": data}

        return data

    except Exception as e:
        return {"error": str(e)}