from openai import OpenAI
import os
import json


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
너는 번역기다.

입력으로 dict의 list가 들어온다.

각 dict의 script 값을 검사해서:

- 한글이면 영어로 번역
- 이미 영어면 그대로 유지

speaker 값은 절대 수정하지 마라.

반드시 입력과 동일한 JSON 형태만 반환해라.
"""


def translate_sentences(sentences):
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
                sentences,
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

    return json.loads(content)