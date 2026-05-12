import re
from datetime import date, datetime

_WHITESPACE = re.compile(r"\s+")
_TAGS = re.compile(r"<[^>]+>")


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = _TAGS.sub(" ", value)
    value = _WHITESPACE.sub(" ", value).strip()
    return value or None


def normalize_title(value: str) -> str:
    return clean_text(value) or "Untitled"


def normalize_date(value: str | date | None) -> date | None:
    if value is None or isinstance(value, date):
        return value
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            parsed = datetime.strptime(value[: len(fmt)], fmt)
            return parsed.date()
        except ValueError:
            continue
    return None


def normalize_name(value: str | None) -> str | None:
    cleaned = clean_text(value)
    if not cleaned:
        return None
    return " ".join(part.capitalize() if part.isupper() else part for part in cleaned.split())


def extract_terms(text: str | None, limit: int = 12) -> list[str]:
    if not text:
        return []
    stopwords = {
        "about", "after", "also", "among", "based", "been", "between", "from", "have",
        "into", "more", "paper", "research", "result", "results", "show", "study",
        "that", "their", "these", "this", "using", "with", "model", "models", "method",
        "methods", "learning", "neural", "data", "approach", "performance",
    }
    words = re.findall(r"[a-z][a-z0-9-]{2,}", text.lower())
    counts: dict[str, int] = {}
    for word in words:
        if word not in stopwords:
            counts[word] = counts.get(word, 0) + 1
    return [term for term, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]
