from app.db.session import SessionLocal
from app.services.clustering import embed_and_cluster
from app.services.papers import search_local_papers

if __name__ == "__main__":
    with SessionLocal() as db:
        papers = search_local_papers(db, limit=1000)
        embed_and_cluster(papers)
        db.commit()
        print(f"Clustered {len(papers)} papers.")
