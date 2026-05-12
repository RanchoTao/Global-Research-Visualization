interface SearchBarProps {
  keyword: string;
  isLoading: boolean;
  onKeywordChange: (keyword: string) => void;
  onSearch: () => void;
}

export function SearchBar({ keyword, isLoading, onKeywordChange, onSearch }: SearchBarProps) {
  return (
    <section className="search-card">
      <div>
        <p className="eyebrow">AI / Machine Learning radar</p>
        <h1>Discover fast-moving research fronts</h1>
        <p className="hero-copy">
          Search arXiv and OpenAlex, normalize metadata, cluster papers, and inspect trends from one MVP dashboard.
        </p>
      </div>
      <div className="search-row">
        <input
          value={keyword}
          onChange={(event) => onKeywordChange(event.target.value)}
          onKeyDown={(event) => event.key === 'Enter' && onSearch()}
          placeholder="Try “world model”, “diffusion model”, or “retrieval augmented generation”"
        />
        <button onClick={onSearch} disabled={isLoading || keyword.trim().length === 0}>
          {isLoading ? 'Searching…' : 'Search papers'}
        </button>
      </div>
    </section>
  );
}
