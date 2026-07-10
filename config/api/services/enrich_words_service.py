# api/services/enrich_words_service.py

from openai import OpenAI

import os
import json
import re


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
너는 영어 학습용 사전 생성기다.

입력으로 단어 정보 배열이 들어온다.

각 단어에 대해:

- meaning_kr
- meaning_en
- synonym
- custom_example

를 생성해라.

반드시 JSON 배열만 반환해라.

형식:

[
  {
    "sentence_id": 15,
    "word": "amazing",
    "word_grade": "L2",

    "meaning_kr": "놀라운",

    "meaning_en":
      "very surprising and impressive",

    "synonym": [
      {
        "word": "awesome",
        "meaning_kr": "굉장한"
      }
    ],

    "custom_example":
      "This movie is amazing."
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


def enrich_words(
    extracted_words
):

    response = (
        client.chat.completions.create(
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
                        extracted_words,
                        ensure_ascii=False
                    )
                }
            ]
        )
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    result = parse_llm_json(
        content
    )

    return result