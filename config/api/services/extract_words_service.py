from openai import OpenAI

import os
import json
import re


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
너는 영어 학습용 단어 추출기다.

입력으로 sentence_id와 영어 문장이 들어온다.

각 문장에서 학습 가치가 있는 단어만 추출해라.

규칙:
- 너무 쉬운 관사/전치사는 제외
- 원형(lemma) 기준 사용
- 중복 단어 제거
- sentence_id 유지
- word_grade는:
  - L1
  - L2
  - L3
  중 하나

반드시 JSON 배열만 반환해라.

형식:

[
  {
    "sentence_id": 15,
    "word": "absolutely",
    "word_grade": "L3"
  }
]
"""


def parse_llm_json(content):

    content = content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]

    match = re.search(
        r'\[.*\]',
        content,
        re.DOTALL
    )

    if match:
        content = match.group(0)

    return json.loads(content)


def extract_words(
    sentence_rows
):

    # -------------------------
    # LLM input 만들기
    # -------------------------

    sentence_payload = []

    for sentence in sentence_rows:

        sentence_payload.append({
            "sentence_id": sentence.id,
            "script": sentence.script
        })

    # -------------------------
    # GPT 호출
    # -------------------------

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        temperature=0,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(
                    sentence_payload,
                    ensure_ascii=False
                )
            }
        ]
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    # -------------------------
    # JSON parsing
    # -------------------------

    result = parse_llm_json(
        content
    )

    return result