from datetime import date

import feedparser
import httpx

from app.processing.normalization import clean_text, normalize_date, normalize_title
from app.schemas import PaperCreate

ARXIV_API_URL = "https://export.arxiv.org/api/query"
AI_CATEGORIES = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV OR cat:stat.ML"


async def search_arxiv(keyword: str, max_results: int = 25) -> list[PaperCreate]:
    query = f"({AI_CATEGORIES}) AND all:{keyword}"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(ARXIV_API_URL, params=params)
        response.raise_for_status()
    feed = feedparser.parse(response.text)
    return [_entry_to_paper(entry) for entry in feed.entries]


def _entry_to_paper(entry: dict) -> PaperCreate:
    arxiv_id = entry.get("id", "").rsplit("/", 1)[-1]
    published: date | None = normalize_date(entry.get("published"))
    doi = None
    for link in entry.get("links", []):
        if link.get("title") == "doi":
            doi = link.get("href", "").replace("https://doi.org/", "")
    return PaperCreate(
        title=normalize_title(entry.get("title", "Untitled")),
        abstract=clean_text(entry.get("summary")),
        authors=[author.get("name") for author in entry.get("authors", []) if author.get("name")],
        institutions=[],
        publication_date=published,
        venue="arXiv",
        source="arxiv",
        citation_count=0,
        doi=doi,
        arxiv_id=arxiv_id,
        openalex_id=None,
    )
