from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ingestion.arxiv_client import search_arxiv
from app.ingestion.openalex_client import search_openalex
from app.schemas import DashboardResponse, PaperRead, SearchRequest
from app.services.clustering import embed_and_cluster
from app.services.metrics import (
    build_topic_points,
    build_trends,
    emerging_keywords,
    top_authors,
    top_institutions,
)
from app.services.papers import bulk_upsert_papers, search_local_papers, serialize_paper

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/search", response_model=DashboardResponse)
async def search_papers(request: SearchRequest, db: Session = Depends(get_db)) -> DashboardResponse:
    fetched = []
    if request.include_arxiv:
        fetched.extend(await search_arxiv(request.keyword, request.max_results))
    if request.include_openalex:
        fetched.extend(await search_openalex(request.keyword, request.max_results))
    papers = bulk_upsert_papers(db, fetched)
    embed_and_cluster(papers)
    db.commit()
    return _dashboard_response(papers)


@router.get("/papers", response_model=list[PaperRead])
def list_papers(
    keyword: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[PaperRead]:
    return [serialize_paper(paper) for paper in search_local_papers(db, keyword, limit)]


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(
    keyword: str | None = Query(default=None),
    limit: int = Query(default=250, ge=1, le=1000),
    db: Session = Depends(get_db),
) -> DashboardResponse:
    papers = search_local_papers(db, keyword, limit)
    return _dashboard_response(papers)


def _dashboard_response(papers) -> DashboardResponse:
    return DashboardResponse(
        papers=[serialize_paper(paper) for paper in papers],
        trends=build_trends(papers),
        topics=build_topic_points(papers),
        top_authors=top_authors(papers),
        top_institutions=top_institutions(papers),
        emerging_keywords=emerging_keywords(papers),
    )
