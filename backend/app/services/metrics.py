from collections import Counter, defaultdict
from datetime import date, timedelta

from app.db.models import Paper
from app.schemas import EmergingKeyword, LeaderboardItem, TopicPoint, TrendPoint
from app.services.clustering import project_topics


def build_trends(papers: list[Paper]) -> list[TrendPoint]:
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"paper_count": 0, "citation_count": 0})
    for paper in papers:
        if not paper.publication_date:
            continue
        period = paper.publication_date.strftime("%Y-%m")
        buckets[period]["paper_count"] += 1
        buckets[period]["citation_count"] += paper.citation_count or 0
    return [
        TrendPoint(period=period, paper_count=values["paper_count"], citation_count=values["citation_count"])
        for period, values in sorted(buckets.items())
    ]


def build_topic_points(papers: list[Paper]) -> list[TopicPoint]:
    coordinates = project_topics(papers)
    return [
        TopicPoint(
            paper_id=paper.id,
            title=paper.title,
            topic_id=paper.topic_id,
            x=coordinates.get(paper.id, (0.0, 0.0))[0],
            y=coordinates.get(paper.id, (0.0, 0.0))[1],
            citation_count=paper.citation_count or 0,
        )
        for paper in papers
    ]


def top_authors(papers: list[Paper], limit: int = 10) -> list[LeaderboardItem]:
    return _leaderboard(papers, "authors", limit)


def top_institutions(papers: list[Paper], limit: int = 10) -> list[LeaderboardItem]:
    return _leaderboard(papers, "institutions", limit)


def emerging_keywords(papers: list[Paper], limit: int = 15) -> list[EmergingKeyword]:
    dated = [paper for paper in papers if paper.publication_date]
    if not dated:
        return []
    latest = max(paper.publication_date for paper in dated if paper.publication_date)
    window_start = latest - timedelta(days=365)
    previous_start = latest - timedelta(days=730)
    recent: Counter[str] = Counter()
    previous: Counter[str] = Counter()
    for paper in dated:
        terms = [keyword.term for keyword in paper.keywords]
        if paper.publication_date and paper.publication_date >= window_start:
            recent.update(terms)
        elif paper.publication_date and paper.publication_date >= previous_start:
            previous.update(terms)
    rows = []
    for term, count in recent.items():
        old_count = previous.get(term, 0)
        growth = (count - old_count) / max(old_count, 1)
        rows.append(EmergingKeyword(term=term, recent_count=count, previous_count=old_count, growth_rate=round(growth, 2)))
    return sorted(rows, key=lambda item: (item.growth_rate, item.recent_count), reverse=True)[:limit]


def recent_growth_rate(papers: list[Paper], as_of: date | None = None) -> float:
    if not papers:
        return 0.0
    as_of = as_of or max((paper.publication_date for paper in papers if paper.publication_date), default=date.today())
    recent_start = as_of - timedelta(days=365)
    previous_start = as_of - timedelta(days=730)
    recent_count = sum(1 for paper in papers if paper.publication_date and paper.publication_date >= recent_start)
    previous_count = sum(
        1 for paper in papers if paper.publication_date and previous_start <= paper.publication_date < recent_start
    )
    return round((recent_count - previous_count) / max(previous_count, 1), 2)


def _leaderboard(papers: list[Paper], attr: str, limit: int) -> list[LeaderboardItem]:
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"paper_count": 0, "citation_count": 0})
    for paper in papers:
        for entity in getattr(paper, attr):
            counts[entity.name]["paper_count"] += 1
            counts[entity.name]["citation_count"] += paper.citation_count or 0
    return [
        LeaderboardItem(name=name, paper_count=values["paper_count"], citation_count=values["citation_count"])
        for name, values in sorted(
            counts.items(), key=lambda item: (item[1]["paper_count"], item[1]["citation_count"]), reverse=True
        )[:limit]
    ]
