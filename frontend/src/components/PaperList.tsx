import type { Paper } from '../types/radar';

export function PaperList({ papers }: { papers: Paper[] }) {
  if (papers.length === 0) {
    return <p className="empty-state">No papers yet. Run a search to populate the radar.</p>;
  }
  return (
    <div className="paper-list">
      {papers.slice(0, 30).map((paper) => (
        <article key={paper.id} className="paper-card">
          <div className="paper-meta">
            <span>{paper.source}</span>
            <span>{paper.publication_date ?? 'Date unknown'}</span>
            <span>{paper.citation_count} citations</span>
            {paper.topic_id !== null && paper.topic_id !== undefined ? <span>Topic {paper.topic_id}</span> : null}
          </div>
          <h3>{paper.title}</h3>
          <p>{paper.abstract?.slice(0, 260) ?? 'No abstract available.'}{paper.abstract && paper.abstract.length > 260 ? '…' : ''}</p>
          <div className="tag-row">
            {paper.keywords.slice(0, 7).map((keyword) => (
              <span key={keyword} className="tag">{keyword}</span>
            ))}
          </div>
          <p className="authors">{paper.authors.slice(0, 5).join(', ')}</p>
        </article>
      ))}
    </div>
  );
}
