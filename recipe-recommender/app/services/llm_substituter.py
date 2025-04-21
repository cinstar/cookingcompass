# app/services/llm_substituter.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def suggest_diet_substitutes(ingredients: list[str], diet: str) -> list[str]:
    prompt = (
        f"Given the following ingredients:\n{', '.join(ingredients)}\n"
        f"Replace or remove any items to make this dish suitable for a {diet} diet.\n"
        f"List the updated ingredients only."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )

    return [line.strip() for line in response.choices[0].message.content.splitlines() if line.strip()]
