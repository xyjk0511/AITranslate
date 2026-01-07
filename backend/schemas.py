from pydantic import BaseModel, Field
from typing import List


class TranslateRequest(BaseModel):
    text: str = Field(..., description="Chinese text to translate")


class TranslateResponse(BaseModel):
    translation: str = Field(..., description="English translation")
    keywords: List[str] = Field(..., description="Exactly 3 English keywords")
