import random
import time
import os
import json
from pathlib import Path
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError, AuthenticationError

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    timeout=30.0,
    max_retries=0,
)

PROMPT = Path("prompts/triage-v1.md").read_text()

def call_model(user_text: str, repair_note: str | None = None, repaired: bool = False) -> str:
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": user_text},
    ]
    if repair_note:
        messages.append({"role": "user", "content": repair_note})

    start = time.time()
    res = call_with_backoff(lambda: client.chat.completions.create(
        model=os.environ["LLM_MODEL"],
        messages=messages,
        temperature=0.2,
    ))
    duration_ms = int((time.time() - start) * 1000)

    log_cost(
        model=os.environ["LLM_MODEL"],
        usage=res.usage,
        duration_ms=duration_ms,
        repaired=repaired,
    )

    return res.choices[0].message.content

def call_with_backoff(fn, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return fn()
        except (RateLimitError, APIConnectionError, APITimeoutError):
            if attempt == max_attempts - 1:
                raise
            time.sleep((2 ** attempt) + random.uniform(0, 0.5))
        except AuthenticationError:
            raise   # never retry a bad key

def log_cost(model, usage, duration_ms, repaired):
    Path("logs").mkdir(exist_ok=True)
    with open("logs/cost.jsonl", "a") as f:
        f.write(json.dumps({
            "prompt_version": "triage-v1",
            "model": model,
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "duration_ms": duration_ms,
            "repaired": repaired,
        }) + "\n")