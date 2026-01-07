import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from llm_client import translate_text
from schemas import TranslateRequest, TranslateResponse

load_dotenv(Path(__file__).resolve().parent / ".env")

logger = logging.getLogger(__name__)

app = FastAPI(title="AI Translation Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"ok": True}


@app.post("/translate", response_model=TranslateResponse)
async def translate(payload: TranslateRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text cannot be empty")

    try:
        translation, keywords = await translate_text(text)
    except RuntimeError as exc:
        logger.exception("Translation parsing failed")
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:  # pragma: no cover - safety net
        logger.exception("Unexpected translation error")
        raise HTTPException(status_code=500, detail="Translation failed")

    return TranslateResponse(translation=translation, keywords=keywords)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
