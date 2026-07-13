from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str


class LogEntry(BaseModel):
    step: str
    detail: str


class ChatResponse(BaseModel):
    answer: str
    decision: Optional[str] = None
    logs: List[LogEntry]