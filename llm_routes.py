import os
from fastapi import APIRouter, HTTPException
from llm_schema import LLM_Request, LLM_Response
from llm_client import call_model
router = APIRouter()

@router.post("/llm", response_model=LLM_Response)
def triage_classifier(body: LLM_Request):
    if os.environ.get("LLM_STUB") == "1":
        return LLM_Response(
            category="other",
            urgency="low",
            confidence=0.5,
            reason="stub response, no model called",
        )
    raw = call_model(body.text)
    raise HTTPException(status_code=501, detail=f"parsing not wired yet — Stage 3. raw: {raw}")
