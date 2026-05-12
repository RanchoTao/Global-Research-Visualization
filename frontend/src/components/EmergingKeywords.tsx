import type { EmergingKeyword } from '../types/radar';

export function EmergingKeywords({ keywords }: { keywords: EmergingKeyword[] }) {
  return (
    <div className="panel">
      <h2>Emerging keywords</h2>
      <table>
        <thead>
          <tr><th>Term</th><th>Recent</th><th>Previous</th><th>Growth</th></tr>
        </thead>
        <tbody>
          {keywords.map((keyword) => (
            <tr key={keyword.term}>
              <td>{keyword.term}</td>
              <td>{keyword.recent_count}</td>
              <td>{keyword.previous_count}</td>
              <td>{Math.round(keyword.growth_rate * 100)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
