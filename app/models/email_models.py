from typing import Literal
from pydantic import BaseModel, Field


Category = Literal["PRODUTIVO", "IMPRODUTIVO"]
Confidence = Literal["ALTA", "MEDIA", "BAIXA"]


class ClassificationResult(BaseModel):
    category: Category
    reason: str = Field(min_length=3)
    suggested_reply: str = Field(min_length=3)
    confidence: Confidence


class ClassificationResponse(BaseModel):
    original_text: str
    normalized_text: str
    result: ClassificationResult
    