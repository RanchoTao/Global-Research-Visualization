import { useEffect, useMemo, useState } from 'react';
import { fetchDashboard, searchPapers } from './api/client';
import { EmergingKeywords } from './components/EmergingKeywords';
import { Leaderboard } from './components/Leaderboard';
import { PaperList } from './components/PaperList';
import { SearchBar } from './components/SearchBar';
import { TopicScatter } from './components/TopicScatter';
import { TrendChart } from './components/TrendChart';
import type { DashboardResponse } from './types/radar';
import './styles.css';

const emptyDashboard: DashboardResponse = {
  papers: [],
  trends: [],
  topics: [],
  top_authors: [],
  top_institutions: [],
  emerging_keywords: [],
};

function App() {
  const [keyword, setKeyword] = useState('world model');
  const [dashboard, setDashboard] = useState<DashboardResponse>(emptyDashboard);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard().then(setDashboard).catch(() => undefined);
  }, []);

  const stats = useMemo(() => {
    const citations = dashboard.papers.reduce((sum, paper) => sum + paper.citation_count, 0);
    const topics = new Set(dashboard.papers.map((paper) => paper.topic_id).filter((topic) => topic !== null && topic !== undefined));
    return { papers: dashboard.papers.length, citations, topics: topics.size };
  }, [dashboard.papers]);

  async function handleSearch() {
    setIsLoading(true);
    setError(null);
    try {
      setDashboard(await searchPapers(keyword.trim(), 25));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected search error');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <SearchBar keyword={keyword} isLoading={isLoading} onKeywordChange={setKeyword} onSearch={handleSearch} />
      {error ? <div className="error-banner">{error}</div> : null}

      <section className="stats-grid">
        <div><span>{stats.papers}</span><p>Papers tracked</p></div>
        <div><span>{stats.citations}</span><p>Total citations</p></div>
        <div><span>{stats.topics}</span><p>Detected topics</p></div>
      </section>

      <section className="dashboard-grid">
        <div className="panel wide">
          <h2>Trend timeline</h2>
          <TrendChart trends={dashboard.trends} />
        </div>
        <div className="panel wide">
          <h2>Topic clusters</h2>
          <TopicScatter topics={dashboard.topics} />
        </div>
      </section>

      <section className="dashboard-grid three-column">
        <Leaderboard title="Top authors" items={dashboard.top_authors} />
        <Leaderboard title="Top institutions" items={dashboard.top_institutions} />
        <EmergingKeywords keywords={dashboard.emerging_keywords} />
      </section>

      <section className="panel">
        <h2>Paper list</h2>
        <PaperList papers={dashboard.papers} />
      </section>
    </main>
  );
}

export default App;
