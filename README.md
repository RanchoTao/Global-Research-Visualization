# Global Research Radar

Global Research Radar is an MVP web application for visualizing research trends, key papers, topics, institutions, and emerging frontiers in AI / Machine Learning.

The first release intentionally focuses on two data sources only:

- [arXiv](https://arxiv.org/) for fresh AI/ML preprints.
- [OpenAlex](https://openalex.org/) for broader scholarly metadata, institutions, and citation counts.

## Features

- Keyword search for AI/ML topics such as `world model`, `diffusion model`, `neural SDE`, and `retrieval augmented generation`.
- Metadata ingestion from arXiv and OpenAlex.
- Local SQLite storage for papers, authors, institutions, keywords, citations, identifiers, and topic assignments.
- Metadata normalization and simple keyword extraction.
- Sentence-transformer embeddings with a TF-IDF fallback for local development.
- K-means topic clustering and PCA projection for visual exploration.
- Trend metrics for paper counts, citations, and emerging keywords.
- React + TypeScript dashboard with ECharts visualizations.

## Project structure

```text
/backend
  app/
    api/              FastAPI routes
    core/             configuration
    db/               SQLAlchemy models and session setup
    ingestion/        arXiv and OpenAlex clients
    processing/       cleaning and keyword helpers
    services/         persistence, clustering, and metrics
/frontend
  src/
    api/              browser API client
    components/       dashboard widgets and charts
    types/            shared TypeScript types
/scripts
  init_db.py          create the local schema
  fetch_papers.py     fetch, store, embed, and cluster keyword results
  cluster_papers.py   recompute embeddings and topic clusters
```

## Backend quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Interactive documentation is available at `http://localhost:8000/docs`.

Optional environment variables can be placed in `backend/.env`:

```env
DATABASE_URL=sqlite:///./global_research_radar.db
OPENALEX_MAILTO=you@example.com
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
DEFAULT_CLUSTER_COUNT=6
```

## Frontend quick start

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at `http://localhost:5173` and expects the backend API at `http://localhost:8000/api`. Override this with `VITE_API_BASE_URL` if needed.

## Useful scripts

Run scripts from the repository root with the backend on `PYTHONPATH`:

```bash
PYTHONPATH=backend python scripts/init_db.py
PYTHONPATH=backend python scripts/fetch_papers.py "retrieval augmented generation" --max-results 20
PYTHONPATH=backend python scripts/cluster_papers.py
```

## API endpoints

- `GET /api/health` — health check.
- `POST /api/search` — fetch from arXiv/OpenAlex, store, cluster, and return dashboard data.
- `GET /api/papers?keyword=...` — list locally stored papers.
- `GET /api/dashboard?keyword=...` — return trends, topic points, leaderboards, keywords, and papers from local data.
