import httpx

from app.core.config import get_settings
from app.processing.normalization import clean_text, normalize_date, normalize_title
from app.schemas import PaperCreate

OPENALEX_API_URL = "https://api.openalex.org/works"
AI_FILTER = "concepts.id:C154945302|C41008148|C119857082"


async def search_openalex(keyword: str, max_results: int = 25) -> list[PaperCreate]:
    settings = get_settings()
    params = {
        "search": keyword,
        "filter": AI_FILTER,
        "per-page": max_results,
        "sort": "publication_date:desc",
    }
    if settings.openalex_mailto:
        params["mailto"] = settings.openalex_mailto
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(OPENALEX_API_URL, params=params)
        response.raise_for_status()
    data = response.json()
    return [_work_to_paper(work) for work in data.get("results", [])]


def _work_to_paper(work: dict) -> PaperCreate:
    authors: list[str] = []
    institutions: list[str] = []
    for authorship in work.get("authorships", []):
        author_name = authorship.get("author", {}).get("display_name")
        if author_name:
            authors.append(author_name)
        for institution in authorship.get("institutions", []):
            name = institution.get("display_name")
            if name and name not in institutions:
                institutions.append(name)
    source = work.get("primary_location", {}).get("source") or {}
    doi = work.get("doi")
    if doi:
        doi = doi.replace("https://doi.org/", "")
    return PaperCreate(
        title=normalize_title(work.get("display_name") or "Untitled"),
        abstract=clean_text(_reconstruct_abstract(work.get("abstract_inverted_index"))),
        authors=authors,
        institutions=institutions,
        publication_date=normalize_date(work.get("publication_date")),
        venue=source.get("display_name") or work.get("type_crossref") or "OpenAlex",
        source="openalex",
        citation_count=work.get("cited_by_count") or 0,
        doi=doi,
        arxiv_id=_extract_arxiv_id(work),
        openalex_id=work.get("id"),
    )


def _reconstruct_abstract(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    positioned: list[tuple[int, str]] = []
    for word, positions in index.items():
        positioned.extend((position, word) for position in positions)
    return " ".join(word for _, word in sorted(positioned))


def _extract_arxiv_id(work: dict) -> str | None:
    for location in work.get("locations", []):
        landing = location.get("landing_page_url") or ""
        if "arxiv.org/abs/" in landing:
            return landing.rsplit("/", 1)[-1]
    return None
