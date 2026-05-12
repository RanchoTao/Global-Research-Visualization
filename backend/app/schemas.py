from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PaperBase(BaseModel):
    title: str
    abstract: str | None = None
    authors: list[str] = Field(default_factory=list)
    institutions: list[str] = Field(default_factory=list)
    publication_date: date | None = None
    venue: str | None = None
    source: str
    citation_count: int = 0
    doi: str | None = None
    arxiv_id: str | None = None
    openalex_id: str | None = None
    topic_id: int | None = None
    keywords: list[str] = Field(default_factory=list)


class PaperCreate(PaperBase):
    pass


class PaperRead(PaperBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SearchRequest(BaseModel):
    keyword: str
    max_results: int = Field(default=25, ge=1, le=100)
    include_arxiv: bool = True
    include_openalex: bool = True


class TrendPoint(BaseModel):
    period: str
    paper_count: int
    citation_count: int


class TopicPoint(BaseModel):
    paper_id: int
    title: str
    topic_id: int | None
    x: float
    y: float
    citation_count: int


class LeaderboardItem(BaseModel):
    name: str
    paper_count: int
    citation_count: int = 0


class EmergingKeyword(BaseModel):
    term: str
    recent_count: int
    previous_count: int
    growth_rate: float


class DashboardResponse(BaseModel):
    papers: list[PaperRead]
    trends: list[TrendPoint]
    topics: list[TopicPoint]
    top_authors: list[LeaderboardItem]
    top_institutions: list[LeaderboardItem]
    emerging_keywords: list[EmergingKeyword]
