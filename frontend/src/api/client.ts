import type { DashboardResponse } from '../types/radar';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

export async function fetchDashboard(keyword?: string): Promise<DashboardResponse> {
  const params = new URLSearchParams();
  if (keyword) params.set('keyword', keyword);
  const response = await fetch(`${API_BASE_URL}/dashboard?${params.toString()}`);
  if (!response.ok) throw new Error('Unable to load dashboard data');
  return response.json();
}

export async function searchPapers(keyword: string, maxResults = 25): Promise<DashboardResponse> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keyword, max_results: maxResults, include_arxiv: true, include_openalex: true }),
  });
  if (!response.ok) throw new Error('Search failed. Check the backend logs for provider errors.');
  return response.json();
}
