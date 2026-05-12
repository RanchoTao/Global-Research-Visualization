import importlib.util
import json

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

from app.core.config import get_settings
from app.db.models import Paper


def embed_and_cluster(papers: list[Paper], cluster_count: int | None = None) -> list[Paper]:
    if not papers:
        return []
    texts = [f"{paper.title}. {paper.abstract or ''}" for paper in papers]
    embeddings = _embed_texts(texts)
    n_clusters = min(cluster_count or get_settings().default_cluster_count, len(papers))
    labels = KMeans(n_clusters=max(n_clusters, 1), random_state=42, n_init="auto").fit_predict(embeddings)
    for paper, vector, label in zip(papers, embeddings, labels, strict=True):
        paper.embedding = json.dumps(vector.tolist())
        paper.topic_id = int(label)
    return papers


def project_topics(papers: list[Paper]) -> dict[int, tuple[float, float]]:
    vectors = []
    paper_ids = []
    for paper in papers:
        if paper.embedding:
            vectors.append(json.loads(paper.embedding))
            paper_ids.append(paper.id)
    if not vectors:
        return {}
    matrix = np.array(vectors)
    if len(vectors) == 1:
        return {paper_ids[0]: (0.0, 0.0)}
    projection = PCA(n_components=2, random_state=42).fit_transform(matrix)
    return {paper_id: (float(x), float(y)) for paper_id, (x, y) in zip(paper_ids, projection, strict=True)}


def _embed_texts(texts: list[str]) -> np.ndarray:
    if importlib.util.find_spec("sentence_transformers") is not None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(get_settings().embedding_model_name)
        return np.array(model.encode(texts, normalize_embeddings=True))

    vectorizer = TfidfVectorizer(max_features=384, stop_words="english")
    return vectorizer.fit_transform(texts).toarray()
