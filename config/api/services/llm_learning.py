from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
주어진 단어를 기반으로 학습 콘텐츠를 생성하세요.

[요구사항]
- 반드시 JSON 형식으로만 응답
- 설명 문장 금지
- 모든 필드를 반드시 포함
- 각 배열은 최소 2개 이상 요소 포함

[출력 형식]
{
  "word": "...",
  "meaning": "...",
  "synonyms": ["...", "..."],
  "antonyms": ["...", "..."],
  "confusing_words": ["...", "..."],
  "examples": ["...", "..."]
}
"""

def generate_learning_content(keyword):
    if not keyword:
        return {"error": "invalid keyword"}

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.7,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"단어: {keyword}"}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {"error": str(e)}