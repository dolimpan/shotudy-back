from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_text(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an assisant AI that extracts emotion from given sentence. Respond with only one word and json"},
            {"role": "user", "content": f"텍스트: {text}"}
        ],
        response_format={"type": "json_object"}  # 🔥 중요
    )
    return response.choices[0].message.content