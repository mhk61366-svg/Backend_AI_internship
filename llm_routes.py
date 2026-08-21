import os
import json
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from openai import RateLimitError
from llm_schema import LLM_Request, LLM_Response
from llm_client import call_model

router = APIRouter()

def extract_json(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("no JSON object found in model output")
    return json.loads(match.group(0))

@router.post("/llm", response_model=LLM_Response)
def triage_classifier(body: LLM_Request):
    if os.environ.get("LLM_ENABLED", "true").lower() == "false":
        return LLM_Response(category="other", urgency="low", confidence=0.0,
                             reason="LLM disabled via kill switch")

    if os.environ.get("LLM_STUB") == "1":
        return LLM_Response(category="other", urgency="low", confidence=0.5,
                             reason="stub response, no model called")

    try:
        raw = call_model(body.text)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="rate limited by provider, try again shortly")

    try:
        result = LLM_Response.model_validate(extract_json(raw))
        return result
    except (ValidationError, ValueError, json.JSONDecodeError) as e:
        repair_note = (
            f"Your previous answer was rejected for this reason: {e}. "
            f"Your previous answer was: {raw}. Return only corrected JSON matching the schema."
        )
        try:
            raw2 = call_model(body.text, repair_note=repair_note, repaired=True)
        except RateLimitError:
            raise HTTPException(status_code=429, detail="rate limited by provider during repair retry")
        try:
            result2 = LLM_Response.model_validate(extract_json(raw2))
            return result2
        except (ValidationError, ValueError, json.JSONDecodeError) as e2:
            Path("logs").mkdir(exist_ok=True)
            with open("logs/quarantine.jsonl", "a") as f:
                f.write(json.dumps({"input": body.text, "raw": raw2, "error": str(e2)}) + "\n")
            raise HTTPException(status_code=422, detail="model could not produce valid output")