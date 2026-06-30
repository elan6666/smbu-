from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ApplicantProfile(BaseModel):
    province: Optional[str] = None
    category: Optional[str] = None
    score: Optional[int] = None
    rank: Optional[int] = None
    preferred_major: Optional[str] = None


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    profile: ApplicantProfile = Field(default_factory=ApplicantProfile)
    enable_web_search: bool = False
    history: List["ChatMessage"] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: str
    content: str


class SourceSnippet(BaseModel):
    source_id: str
    title: str
    url: str
    snippet: str
    score: float = 0.0


class ChatResponse(BaseModel):
    answer: str
    question_type: str
    sources: List[SourceSnippet] = Field(default_factory=list)
    score_rows: List[Dict[str, Any]] = Field(default_factory=list)
    program_rows: List[Dict[str, Any]] = Field(default_factory=list)
    dimension_rows: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ScoreQuery(BaseModel):
    year: Optional[int] = None
    province: Optional[str] = None
    category: Optional[str] = None
    major: Optional[str] = None


class ProgramQuery(BaseModel):
    level: Optional[str] = None
    program: Optional[str] = None
    degree_mode: Optional[str] = None
