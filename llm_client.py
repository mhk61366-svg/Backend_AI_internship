import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    timeout=30.0,
    max_retries=0,
)

PROMPT = Path("prompts/triage-v1.md").read_text()

def call_model(user_text: str, repair_note: str | None = None) -> str:
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": user_text},
    ]
    if repair_note:
        messages.append({"role": "user", "content": repair_note})
    res = client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=messages,
        temperature=0.2,
    )
    return res.choices[0].message.content