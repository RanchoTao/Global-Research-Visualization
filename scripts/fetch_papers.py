import argparse
import asyncio

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.ingestion.arxiv_client import search_arxiv
from app.ingestion.openalex_client import search_openalex
from app.services.clustering import embed_and_cluster
from app.services.papers import bulk_upsert_papers


async def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch AI/ML papers from arXiv and OpenAlex.")
    parser.add_argument("keyword", help="Search keyword, e.g. 'world model'.")
    parser.add_argument("--max-results", type=int, default=25)
    parser.add_argument("--skip-arxiv", action="store_true")
    parser.add_argument("--skip-openalex", action="store_true")
    args = parser.parse_args()

    init_db()
    fetched = []
    if not args.skip_arxiv:
        fetched.extend(await search_arxiv(args.keyword, args.max_results))
    if not args.skip_openalex:
        fetched.extend(await search_openalex(args.keyword, args.max_results))

    with SessionLocal() as db:
        papers = bulk_upsert_papers(db, fetched)
        embed_and_cluster(papers)
        db.commit()
        print(f"Stored {len(papers)} papers for keyword: {args.keyword}")


if __name__ == "__main__":
    asyncio.run(main())
