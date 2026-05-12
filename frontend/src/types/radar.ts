export interface Paper {
  id: number;
  title: string;
  abstract?: string | null;
  authors: string[];
  institutions: string[];
  publication_date?: string | null;
  venue?: string | null;
  source: string;
  citation_count: number;
  doi?: string | null;
  arxiv_id?: string | null;
  openalex_id?: string | null;
  topic_id?: number | null;
  keywords: string[];
}

export interface TrendPoint {
  period: string;
  paper_count: number;
  citation_count: number;
}

export interface TopicPoint {
  paper_id: number;
  title: string;
  topic_id?: number | null;
  x: number;
  y: number;
  citation_count: number;
}

export interface LeaderboardItem {
  name: string;
  paper_count: number;
  citation_count: number;
}

export interface EmergingKeyword {
  term: string;
  recent_count: number;
  previous_count: number;
  growth_rate: number;
}

export interface DashboardResponse {
  papers: Paper[];
  trends: TrendPoint[];
  topics: TopicPoint[];
  top_authors: LeaderboardItem[];
  top_institutions: LeaderboardItem[];
  emerging_keywords: EmergingKeyword[];
}
