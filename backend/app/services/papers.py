from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import Author, Institution, Keyword, Paper
from app.processing.normalization import extract_terms, normalize_name, normalize_title
from app.schemas import PaperCreate, PaperRead


def upsert_paper(db: Session, payload: PaperCreate) -> Paper:
    paper = _find_existing(db, payload)
    if paper is None:
        paper = Paper(source=payload.source, title=normalize_title(payload.title))
        db.add(paper)

    paper.title = normalize_title(payload.title)
    paper.abstract = payload.abstract
    paper.publication_date = payload.publication_date
    paper.venue = payload.venue
    paper.doi = payload.doi
    paper.arxiv_id = payload.arxiv_id
    paper.openalex_id = payload.openalex_id
    paper.citation_count = payload.citation_count or 0

    paper.authors = [_get_or_create_author(db, name) for name in payload.authors if normalize_name(name)]
    paper.institutions = [
        _get_or_create_institution(db, name) for name in payload.institutions if normalize_name(name)
    ]
    terms = payload.keywords or extract_terms(f"{paper.title} {paper.abstract or ''}")
    paper.keywords = [_get_or_create_keyword(db, term) for term in terms]
    db.flush()
    return paper


def bulk_upsert_papers(db: Session, papers: list[PaperCreate]) -> list[Paper]:
    persisted = [upsert_paper(db, paper) for paper in papers]
    db.commit()
    for paper in persisted:
        db.refresh(paper)
    return persisted


def search_local_papers(db: Session, keyword: str | None = None, limit: int = 100) -> list[Paper]:
    stmt = select(Paper).order_by(Paper.publication_date.desc().nullslast(), Paper.citation_count.desc()).limit(limit)
    if keyword:
        pattern = f"%{keyword}%"
        stmt = stmt.where(or_(Paper.title.ilike(pattern), Paper.abstract.ilike(pattern)))
    return list(db.scalars(stmt).unique())


def serialize_paper(paper: Paper) -> PaperRead:
    return PaperRead(
        id=paper.id,
        title=paper.title,
        abstract=paper.abstract,
        authors=[author.name for author in paper.authors],
        institutions=[institution.name for institution in paper.institutions],
        publication_date=paper.publication_date,
        venue=paper.venue,
        source=paper.source,
        citation_count=paper.citation_count,
        doi=paper.doi,
        arxiv_id=paper.arxiv_id,
        openalex_id=paper.openalex_id,
        topic_id=paper.topic_id,
        keywords=[keyword.term for keyword in paper.keywords],
    )


def _find_existing(db: Session, payload: PaperCreate) -> Paper | None:
    conditions = []
    if payload.openalex_id:
        conditions.append(Paper.openalex_id == payload.openalex_id)
    if payload.doi:
        conditions.append(Paper.doi == payload.doi)
    if payload.arxiv_id:
        conditions.append(Paper.arxiv_id == payload.arxiv_id)
    if not conditions:
        return None
    return db.scalar(select(Paper).where(or_(*conditions)))


def _get_or_create_author(db: Session, name: str) -> Author:
    normalized = normalize_name(name) or name
    author = db.scalar(select(Author).where(Author.name == normalized))
    if author is None:
        author = Author(name=normalized)
        db.add(author)
        db.flush()
    return author


def _get_or_create_institution(db: Session, name: str) -> Institution:
    normalized = normalize_name(name) or name
    institution = db.scalar(select(Institution).where(Institution.name == normalized))
    if institution is None:
        institution = Institution(name=normalized)
        db.add(institution)
        db.flush()
    return institution


def _get_or_create_keyword(db: Session, term: str) -> Keyword:
    normalized = term.strip().lower()
    keyword = db.scalar(select(Keyword).where(Keyword.term == normalized))
    if keyword is None:
        keyword = Keyword(term=normalized)
        db.add(keyword)
        db.flush()
    return keyword
