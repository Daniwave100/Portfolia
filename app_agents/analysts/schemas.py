from __future__ import annotations
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

# ---------- Shared enums ----------
Rating = Literal["Good", "Neutral", "Bad", "NA"]
Confidence = Literal["Low", "Medium", "High"]
SentimentLabel = Literal["Positive", "Neutral", "Negative"]
Strength = Literal["Low", "Medium", "High"]


# ---------- News models ----------
class Headline(BaseModel):
    title: str
    source: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD
    url: Optional[str] = None


class NewsResult(BaseModel):
    window_days: int
    raw_headlines: List[Headline]

    sentiment_label: SentimentLabel
    sentiment_strength: Strength

    themes: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    key_points: List[str] = Field(default_factory=list)
    key_headlines: List[Headline] = Field(default_factory=list)


# ---------- Valuation models (deterministic) ----------
class ValuationInputs(BaseModel):
    price: Optional[float] = None
    eps_ttm: Optional[float] = None
    revenue_ttm: Optional[float] = None

    market_cap: Optional[float] = None
    shares_outstanding: Optional[float] = None

    total_debt: Optional[float] = None
    total_equity: Optional[float] = None


class ValuationMetrics(BaseModel):
    pe_ttm: Optional[float] = None
    ps_ttm: Optional[float] = None
    debt_to_equity: Optional[float] = None


class ValuationResult(BaseModel):
    inputs: ValuationInputs
    metrics: ValuationMetrics
    ratings: Dict[str, Rating]
    overall_score: int
    quality_flags: List[str] = Field(default_factory=list)


# ---------- Final output (JSON-first) ----------
class Memo(BaseModel):
    headline: str
    summary_bullets: List[str]
    confidence: Confidence


class FinalOutput(BaseModel):
    ticker: str
    as_of: str
    memo: Memo
    dashboard: Dict[str, Any]
    what_to_check_next: List[str]


# ---------- LangGraph state ----------
class GraphState(BaseModel):
    ticker: str
    as_of: str

    valuation: Optional[ValuationResult] = None
    news: Optional[NewsResult] = None
    final: Optional[FinalOutput] = None